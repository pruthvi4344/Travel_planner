import requests
import json
import os
from agent.state import AgentState  # ✅ Import AgentState model

# Ensure API Key is set
api_key = os.environ["MISTRAL_API_KEY"] = "Rj6ZSCOL065j9Aj8xlOTjXhVOJehMX1l"
if not api_key:
    raise ValueError("❌ MISTRAL_API_KEY is missing. Set it in your environment variables.")

# Mistral API URL
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def handle_followup(state: AgentState) -> dict:
    """
    Sends user follow-up questions to Mistral API and returns the response.

    Args:
        state (AgentState): Current state of the agent.

    Returns:
        dict: Updated state with the response.
    """

    user_question = state.user_input.lower().strip()  # ✅ Fix: Get input from state
    
    # ✅ Check if a destination is selected
    if not state.destinations:
        state.response = "⚠️ No selected destination. Please choose a destination first."
        return state.model_dump()
    
    selected_destination = state.destinations[0]  # Get first selected destination
    destination_name = selected_destination.get("name", "Unknown Location")

    # ✅ Modify the system prompt to include the selected destination
    system_prompt = f"""
    The user has selected {destination_name} as their travel destination.
    Provide a specific and relevant response for {destination_name} to the following question:

    If not found respond appropriate for whatever the user has asked 
    """

    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # ✅ Send request
    response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response_data = response.json()
        state.response = response_data["choices"][0]["message"]["content"]
    else:
        state.response = "I'm having trouble processing your request. Please try again."
        print("❌ Mistral API Error:", response.text)

    return state.model_dump()  # ✅ FIX: Always return a dictionary
