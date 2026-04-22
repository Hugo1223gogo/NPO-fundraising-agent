from memory import test_connection, save_interaction

print(test_connection())

sample = {
    "person_name": "Amy",
    "company": "Cisco",
    "topics_discussed": ["AgenticOps", "Cisco Wireless"],
    "suggested_connections": ["James"],
    "follow_up_action": "Follow up next week"
}

doc_id = save_interaction(sample)
print("Saved document ID:", doc_id)
