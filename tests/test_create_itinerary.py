from agent.state import AgentState
from agent.nodes.create_itinerary import create_itinerary

def format_itinerary_text(itinerary):
    """Convert itinerary into a user-friendly text paragraph."""
    if not itinerary or "plan" not in itinerary:
        return " No itinerary available."

    text_message = f"📍 Your {len(itinerary['plan'])}-day itinerary for *{itinerary['destination']}*:\n\n"
    
    for day in itinerary["plan"]:
        text_message += (
            f"📅 *Day {day['day']}: {day['title']}*\n"
            f"👉 {day['description']}\n"
            f"🎯 Activities: {', '.join(day.get('activities', []))}\n\n"
        )
    
    return text_message.strip()

def test_create_itinerary():
    """Test create_itinerary function with different inputs."""

    test_cases = [
        #  Valid case: Should generate an itinerary
        ({
            "duration": 5,
        }, [ {
      "name": "Tokyo",
      "country": "Japan",
      "tags": ["technology", "culture", "food", "shopping"],
      "budget_range": [120000, 250000],
      "ideal_duration": [5, 10],
      "best_seasons": ["spring", "fall"]
  }], True),

        # invalid case: No destination provided (should return empty itinerary)
        ({
            "duration": 4,
        }, [], False)
    ]

    for preferences, destinations, should_generate in test_cases:
        state = AgentState()
        state.preferences = preferences
        state.destinations = destinations  # Set destination list dynamically

        updated_state = create_itinerary(state)
        itinerary_text = format_itinerary_text(updated_state.get("itinerary", {}))

        print("\n Test Preferences:", preferences)
        print("📜 **Generated Itinerary Message:**\n", itinerary_text)

        if should_generate:
            assert "destination" in updated_state["itinerary"], "Missing 'destination' in itinerary!"
            assert len(updated_state["itinerary"]["plan"]) == preferences["duration"], " Incorrect number of days!"
            assert "title" in updated_state["itinerary"]["plan"][0], " Missing 'title' in first day!"
            assert "description" in updated_state["itinerary"]["plan"][0], " Missing 'description' in first day!"
        else:
            assert "itinerary" not in updated_state or not updated_state["itinerary"], " Itinerary should be empty!"

        print(" Test Passed!")

# Run the test
if __name__ == "__main__":
    test_create_itinerary()
