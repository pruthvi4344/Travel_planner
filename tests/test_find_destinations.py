from agent.state import AgentState
from agent.nodes.find_destinations import find_destinations

def test_find_destinations():
    state = AgentState()
    state.preferences = {
        "budget": 40000,
        "duration": 5,
        "tags": ["hiking", "photography"]
    }

    updated_state = find_destinations(state)

    print("\nMatched Destinations:", updated_state.destinations)  # Debug output

    assert len(updated_state.destinations) > 0, "No destinations found"
    
    for destination in updated_state.destinations:
        assert destination["budget_range"][0] <= state.preferences["budget"] <= destination["budget_range"][1], "Budget mismatch"
        assert any(tag in destination["tags"] for tag in state.preferences["tags"]), "Interest mismatch"

    print("✅ Test passed: find_destinations correctly finds matching destinations.")

# Run the test
test_find_destinations()
