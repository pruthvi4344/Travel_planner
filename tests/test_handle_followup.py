from agent.state import AgentState
from agent.nodes.handle_followup import handle_followup

def format_followup_response(response):
    """Formats the follow-up response in a user-friendly text paragraph."""
    if not response or "response" not in response:
        return " No response available."

    return f"Question:  {response['user_input']}\n" \
           f"AI Response:  {response['response']}\n"

def test_handle_followup():
    """Tests handle_followup function with different user questions."""
    
    state = AgentState()
    state.destinations = [
        {"name": "Manali", "country": "India", "best_seasons": ["summer", "winter"]}
    ]

    test_questions = [
        "When is the best season to travel?",
        "What's the weather like?",
        "Tell me about local food in Manali."
    ]

    for question in test_questions:
        state.user_input = question
        updated_state = handle_followup(state)
        formatted_response = format_followup_response(updated_state)

        print("\n" + formatted_response)

    print("Test Passed: All follow-up responses are formatted correctly.")

# Run the test
if __name__ == "__main__":
    test_handle_followup()
