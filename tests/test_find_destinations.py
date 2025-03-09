from agent.state import AgentState
from agent.nodes.find_destinations import find_destinations

def test_find_destinations():
    """Test find_destinations function with different preferences."""

    test_cases = [
        #  Valid case: Should find destinations
        ({
            "budget": 40000,
            "duration": 5,
            "tags": ["hiking", "photography"],
            "country": "India"
        }, True),

        #  invlaid case: No match should be found
        ({
            "budget": 1000,  # Too low budget
            "duration": 2,
            "tags": ["luxury", "spa"],
            "country": "USA"
        }, False)
    ]

    for preferences, should_find_destinations in test_cases:
        state = AgentState()
        state.preferences = preferences
        state.destinations = []  # Reset before each test

        updated_state = find_destinations(state)

        print("\n Test Preferences:", preferences)
        # print(" Extracted Destinations:", updated_state["destinations"])
        print(" Response Message:\n", updated_state["destination_message"])

        if should_find_destinations:
            assert len(updated_state["destinations"]) > 0, " No destinations found when expected!"
            for destination in updated_state["destinations"]:
                assert "name" in destination, " Destination missing 'name' field!"
                assert "budget" in destination, " Destination missing 'budget' field!"
                assert "duration" in destination, " Destination missing 'duration' field!"
        else:
            assert len(updated_state["destinations"]) == 0, " Destinations found when none should match!"
            assert "no exact matches found" in updated_state["destination_message"].lower(), " Incorrect response for no match!"

        print("Test Passed")

# Run the test
if __name__ == "__main__":
    test_find_destinations()
