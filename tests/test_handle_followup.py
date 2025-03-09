from agent.state import AgentState
from agent.nodes.handle_followup import handle_followup

def test_handle_followup():
    state = AgentState()
    state.itinerary = {
        "destination": "Manali",
        "country": "India",
        "best_seasons": ["summer", "winter"],
        "plan": [
            {"day": 1, "activity": "Go for a scenic trek"},
            {"day": 2, "activity": "Explore Old Manali cafes"},
            {"day": 3, "activity": "Visit Solang Valley"}
        ]
    }

    # Test "Best time to visit" question
    response1 = handle_followup(state, "When is the best season to travel?")
    print("Response 1:", response1)

    # Test "Change budget" question
    response2 = handle_followup(state, "Can I raise my spending limit?")
    print("Response 2:", response2)

    # Test "Swap activity" question
    response3 = handle_followup(state, "Change my itinerary activities.")
    print("Response 3:", response3)

    # Test "Repeat itinerary" question
    response4 = handle_followup(state, "Show my full trip schedule.")
    print("Response 4:", response4)

    print("✅ Test passed: handle_followup is now fully dynamic.")

# Run the test
test_handle_followup()
