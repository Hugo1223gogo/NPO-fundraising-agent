import streamlit as st

from data_loader import load_roster_from_csv
from memory import (
    get_feedback,
    get_recommendations,
    get_roster,
    save_feedback,
    save_recommendation,
    seed_roster_if_empty,
)
from recommender import recommend

st.set_page_config(
    page_title="U4H Donor Recommendation Agent",
    page_icon="💙",
    layout="wide",
)

st.markdown(
    """
<style>
    .block-container { max-width: 1050px; padding-top: 2rem; }
    h1, h2, h3 { letter-spacing: -0.01em; }
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input {
        border-radius: 10px !important;
    }
    div.stButton > button {
        border-radius: 10px;
        background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
        color: white;
        font-weight: 600;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def _initial_seed() -> int:
    return seed_roster_if_empty(load_roster_from_csv())


_ = _initial_seed()

st.title("U4H Donor Recommendation Agent")
st.caption(
    "For a given fundraising need, recommend who to contact, through which pathway, "
    "and why — grounded in U4H's roster and past outreach outcomes."
)

tab_rec, tab_roster, tab_history = st.tabs(
    ["Get Recommendations", "Browse Roster", "Feedback & History"]
)

# ----- Tab: Get Recommendations -----
with tab_rec:
    st.subheader("Describe your fundraising need")
    need = st.text_area(
        "What are you fundraising for?",
        height=160,
        placeholder=(
            "Example: We're launching a maternal health outreach pilot in Lagos "
            "and need to raise $300K by Q3. Who should I approach?"
        ),
    )

    col1, col2 = st.columns(2)
    with col1:
        region = st.text_input("Target region (optional)", placeholder="e.g., West Africa")
    with col2:
        industry = st.text_input("Industry focus (optional)", placeholder="e.g., Pharma, Consulting")

    if st.button("Get recommendations", type="primary"):
        if not need.strip():
            st.warning("Enter a fundraising need first.")
        else:
            filters = {k: v.strip() for k, v in {"region": region, "industry": industry}.items() if v.strip()}
            with st.spinner("Asking the agent..."):
                try:
                    result = recommend(need, filters=filters or None)
                    rec_id = save_recommendation(result)

                    st.success("Recommendations ready.")
                    summary = result.get("summary", "")
                    if summary:
                        st.markdown(f"**Strategy:** {summary}")
                    st.divider()

                    candidates = result.get("candidates", [])
                    if not candidates:
                        st.info("No strong matches in the current roster.")
                    for c in candidates:
                        score = c.get("helpfulness_score", "?")
                        st.markdown(f"### {c.get('name', '?')} — {score}/100")
                        st.markdown(f"**Pathway:** {c.get('pathway', '')}")
                        st.markdown(f"**Why:** {c.get('why', '')}")
                        st.markdown(f"**How to approach:** {c.get('how_to_approach', '')}")
                        st.markdown(f"**Suggested next step:** {c.get('suggested_next_step', '')}")
                        st.divider()

                    st.caption(f"Recommendation ID: `{rec_id}` — record outcomes on the Feedback tab.")
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

# ----- Tab: Browse Roster -----
with tab_roster:
    st.subheader("Roster")
    roster = get_roster()
    st.caption(f"{len(roster)} people loaded from the demo CSV.")

    q = st.text_input("Filter (matches any field)")
    if q:
        ql = q.lower()
        roster = [p for p in roster if ql in " ".join(str(v).lower() for v in p.values())]
        st.caption(f"{len(roster)} matches")

    for p in roster:
        header = f"{p.get('name', '?')} — {p.get('nonprofit_affiliation', '')}"
        with st.expander(header):
            st.json(p)

# ----- Tab: Feedback & History -----
with tab_history:
    st.subheader("Past recommendations")
    recs = get_recommendations(limit=25)
    if not recs:
        st.info("No recommendations recorded yet. Generate one on the first tab.")

    for r in recs:
        rec_id = str(r["_id"])
        need_txt = r.get("need", "(no need recorded)")
        title = need_txt if len(need_txt) <= 90 else need_txt[:90] + "..."
        with st.expander(title):
            if r.get("summary"):
                st.markdown(f"**Strategy:** {r['summary']}")
            names = [c.get("name") for c in r.get("candidates", []) if c.get("name")]
            st.markdown(f"**Candidates:** {', '.join(names) if names else '(none)'}")
            st.caption(f"Recommendation ID: `{rec_id}` · Created: {r.get('created_at', '?')}")

            st.markdown("##### Record an outcome")
            with st.form(f"fb_form_{rec_id}"):
                who = st.selectbox(
                    "Who did you contact?",
                    names or ["(no candidates on this recommendation)"],
                    key=f"fb_who_{rec_id}",
                )
                outcome = st.selectbox(
                    "Outcome",
                    ["success", "no_response", "declined"],
                    key=f"fb_out_{rec_id}",
                )
                note = st.text_area("Note (optional)", key=f"fb_note_{rec_id}")
                submitted = st.form_submit_button("Save feedback")
                if submitted:
                    if not names:
                        st.warning("No candidates on this recommendation to give feedback on.")
                    else:
                        save_feedback(rec_id, who, outcome, note)
                        st.success("Feedback saved. The agent will factor this into future recommendations.")

    st.divider()
    st.subheader("All recorded outcomes")
    fbs = get_feedback(limit=100)
    if not fbs:
        st.caption("No feedback yet.")
    for fb in fbs:
        line = f"- **{fb.get('person_name', '?')}** — {fb.get('outcome', '?')}"
        if fb.get("note"):
            line += f" — _{fb['note']}_"
        st.markdown(line)
