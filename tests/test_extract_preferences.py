from agent.state import AgentState
from agent.nodes.extract_preferences import extract_preferences

def test_extract_preferences():
    state = AgentState()

    user_input = input("Enter your travel request: ")  # Get user input dynamically
    updated_state = extract_preferences(state, user_input)

    print("\n✅ Final Extracted Preferences:", updated_state.preferences)
    print("✅ Final Extracted Tags:", updated_state.preferences.get("tags", []))

# Run the test
test_extract_preferences()
