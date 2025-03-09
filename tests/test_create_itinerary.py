from agent.state import AgentState
from agent.nodes.create_itinerary import create_itinerary

def test_create_itinerary():
    state = AgentState()
    state.preferences = {"duration": 5}  # User wants a 5-day trip
    state.destinations = [
        {
            "name": "Manali",
            "country": "India",
            "tags": ["mountain", "adventure", "hiking", "photography"],
            "budget_range": [20000, 60000],
            "ideal_duration": [3, 7],
            "best_seasons": ["summer", "winter"]
        }
    ]

    updated_state = create_itinerary(state)

    print("\nGenerated Itinerary:", updated_state.itinerary)  # Debug output

    assert "destination" in updated_state.itinerary
    assert len(updated_state.itinerary["plan"]) == 5  # Check correct number of days
    assert "activity" in updated_state.itinerary["plan"][0]  # Check activity presence

    print("✅ Test passed: create_itinerary generates a correct itinerary.")

# Run the test
test_create_itinerary()
