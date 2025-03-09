import time
from agent.state import AgentState
from agent.nodes.extract_preferences import extract_preferences

def test_extract_preferences():
    """Test the extract_preferences function with actual API calls."""

    test_cases = [
        ("I want to visit a mountain and want do some hiking with photogrphy and also some shopping destination in India with a budget of 15000 for 6 days.", 
         {"tags": ["mountain"], "duration": 6, "budget": 15000, "country": "India"}),

        ("Plan a 5-day trip to Paris within $2000.", 
         {"tags": [], "duration": 5, "budget": 2000, "country": "France", "name": "Paris"}),

        ("Looking for an adventure, luxuru, technology trip in the USA for 10 days with a budget of $5000.", 
         {"tags": ["adventure"], "duration": 10, "budget": 5000, "country": "USA"}),

        ("Hello!", {})  # Greeting should not extract preferences
    ]

    for user_input, expected_preferences in test_cases:
        state = AgentState(user_input=user_input)  

        #  Retry mechanism in case of rate limit errors
        for attempt in range(3):  
            updated_state = extract_preferences(state)  #  Hit the real API
            if "Requests rate limit exceeded" in updated_state.response:
                print("Rate limit exceeded. Retrying in 5 seconds...")
                time.sleep(5)  # Wait before retrying
            else:
                break  # Exit retry loop if successful

        print("\n Test Input:", user_input)
        print(" Extracted Preferences:", updated_state.preferences)

        # Validation
        if expected_preferences:  # If we expect preferences, check they exist
            assert "tags" in updated_state.preferences, " Tags missing in preferences!"
            assert isinstance(updated_state.preferences.get("duration", 0), int), " Duration should be an integer!"
            assert isinstance(updated_state.preferences.get("budget", 0), int), " Budget should be an integer!"
        else:  # For greetings, the response should be non-empty
            assert updated_state.response.startswith("Hello!"), " Greeting response incorrect!"

# Run the test
if __name__ == "__main__":
    test_extract_preferences()
