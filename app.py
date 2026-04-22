import streamlit as st
from agent import extract_networking_info
from memory import save_interaction, find_interactions_by_person
from qa_agent import (
    answer_question,
    suggest_followups,
    generate_followup_email,
    prioritize_followups,
    relationship_insights,
)

st.set_page_config(page_title="CareerOps Agent", page_icon="🤝", layout="wide")

st.markdown("""
<style>
    .main {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }

    h1, h2, h3 {
        color: #111827;
        letter-spacing: -0.02em;
    }

    .hero-card {
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 20px;
        padding: 1.5rem 1.5rem 1.2rem 1.5rem;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
        backdrop-filter: blur(10px);
        margin-bottom: 1.2rem;
    }

    .section-card {
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid rgba(255, 255, 255, 0.7);
        border-radius: 18px;
        padding: 1.2rem;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        backdrop-filter: blur(8px);
    }

    .small-muted {
        color: #4b5563;
        font-size: 0.98rem;
    }

    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input {
        border-radius: 14px !important;
        border: 1px solid #dbe4ff !important;
        background: rgba(255, 255, 255, 0.92) !important;
    }

    div.stButton > button {
        border-radius: 14px;
        border: none;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        font-weight: 600;
        padding: 0.6rem 1rem;
        box-shadow: 0 8px 18px rgba(79, 70, 229, 0.25);
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%);
        color: white;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 12px;
        background: rgba(255,255,255,0.72);
        padding-left: 16px;
        padding-right: 16px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-card">
    <h1 style="margin-bottom:0.4rem;">CareerOps Agent</h1>
    <p style="font-size:1.05rem;color:#6b7280;margin-top:-6px;">
        AI Networking Copilot
    </p>
    <p class="small-muted" style="margin-bottom:0.3rem;">
        Your AI networking copilot for turning messy meeting notes into structured relationship memory.
    </p>
    <p class="small-muted">
        Analyze notes, save interactions, search past conversations, ask follow-up questions, and generate outreach drafts.
    </p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "Analyze New Note",
    "Search Past Interactions",
    "Ask the Agent"
])

with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Analyze a New Networking Interaction")
    st.caption("Paste raw notes from a coffee chat, panel, conference, or recruiter conversation.")

    note = st.text_area(
        "Networking Meeting Notes",
        height=220,
        placeholder="Example: Met Daniel from Microsoft at Yale SOM Tech Trek..."
    )

    if st.button("Analyze Note"):
        if not note.strip():
            st.warning("Please paste some meeting notes first.")
        else:
            with st.spinner("Analyzing note..."):
                try:
                    result = extract_networking_info(note)
                    doc_id = save_interaction(result)

                    st.success("Interaction analyzed and saved to memory.")
                    st.json(result)
                    st.caption(f"Saved document ID: {doc_id}")

                except Exception as e:
                    st.error(f"Something went wrong: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Search Relationship Memory")
    st.caption("Look up previous interactions by person name.")

    search_name = st.text_input(
        "Enter a person's name",
        placeholder="Daniel"
    )

    if st.button("Search"):
        if not search_name.strip():
            st.warning("Please enter a name first.")
        else:
            try:
                results = find_interactions_by_person(search_name)

                if results:
                    st.success(f"Found {len(results)} interaction(s) for {search_name}")
                    for i, item in enumerate(results, start=1):
                        st.markdown(f"### Interaction {i}")
                        st.json(item)
                else:
                    st.info(f"No past interactions found for {search_name}")

            except Exception as e:
                st.error(f"Something went wrong: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Ask the Agent")
    st.caption("Ask questions across your stored networking history.")

    question = st.text_input(
        "Ask a question about your networking memory",
        placeholder="What should I do next after meeting Daniel?"
    )

    if st.button("Ask"):
        if not question.strip():
            st.warning("Please enter a question first.")
        else:
            with st.spinner("Thinking..."):
                try:
                    answer = answer_question(question)
                    st.success("Answer ready!")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    st.divider()
    st.subheader("Suggested Follow-ups")
    st.caption("Let the agent scan your memory and recommend next actions.")

    if st.button("What follow-ups should I do?"):
        with st.spinner("Analyzing interactions..."):
            try:
                result = suggest_followups()
                st.success("Here are your recommended follow-ups:")
                st.write(result)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

    st.divider()
    st.subheader("Priority Actions")
    st.caption("Let the agent rank the highest-value follow-ups for this week.")

    if st.button("Who should I prioritize this week?"):
        with st.spinner("Prioritizing follow-ups..."):
            try:
                result = prioritize_followups()
                st.success("Here are your top priorities:")
                st.write(result)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

    st.divider()
    st.subheader("Relationship Insights")
    st.caption("Let the agent proactively surface relationship opportunities and networking patterns.")

    if st.button("Scan my networking memory"):
        with st.spinner("Scanning relationship memory..."):
            try:
                result = relationship_insights()
                st.success("Here are your relationship insights:")
                st.write(result)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

    st.divider()
    st.subheader("Generate Follow-up Email")
    st.caption("Draft a professional outreach email based on stored interaction history.")

    email_name = st.text_input(
        "Enter the person's name for the email draft",
        placeholder="Daniel"
    )

    if st.button("Generate Email Draft"):
        if not email_name.strip():
            st.warning("Please enter a person's name first.")
        else:
            with st.spinner("Drafting email..."):
                try:
                    email_draft = generate_followup_email(email_name)
                    st.success("Email draft ready!")
                    st.text_area("Draft Email", value=email_draft, height=260)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
    