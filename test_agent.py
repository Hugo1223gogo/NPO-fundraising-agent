from agent import extract_networking_info

note = """
Coffee chat with Helen from Cisco.
We talked about AgenticOps and Cisco Wireless.
She suggested I connect with James on the wireless team.
I should follow up next week and thank her for the advice.
"""

result = extract_networking_info(note)

print(result)
