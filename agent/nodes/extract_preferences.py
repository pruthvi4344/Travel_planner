
import requests
import json
import os
import re
from agent.state import AgentState  # ✅ Import AgentState model

# Ensure API Key is set
api_key = os.environ["MISTRAL_API_KEY"] = "Rj6ZSCOL065j9Aj8xlOTjXhVOJehMX1l"
if not api_key:
    raise ValueError("❌ MISTRAL_API_KEY is missing. Set it in your environment variables.")

# Mistral API URL
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def extract_preferences(state: AgentState) -> AgentState:
    """Extracts travel-related preferences from user input using Mistral API."""

    user_input = state.user_input  # Get input from AgentState

    system_prompt = """
    Extract travel-related preferences from the given text in JSON format with keys:
    "tags" (interest-based locations like shopping, nightlife),
    "duration" (number of days as an integer),
    "budget" (amount as an integer).
    "country"(if country is mentioned add field in output.)
    "name"(if any city is mentioned give it as a output of name)

    Example output:
    {
        "tags": ["shopping", "nightlife"],
        "duration": 5,
        "budget": 20000,
        "country": India,
        "name": Jaipur,
    }
    """

    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
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
        extracted_text = response_data["choices"][0]["message"]["content"]

        # ✅ Remove Markdown code block (```json ... ```)
        extracted_text = re.sub(r"```json\n(.*?)\n```", r"\1", extracted_text, flags=re.DOTALL)

        try:
            preferences = json.loads(extracted_text)  # Convert to dictionary
            print(preferences)
            # ✅ Fix: Ensure duration is  an integer
            if "duration" in preferences and isinstance(preferences["duration"], list):
                duration_str = preferences["duration"][0]  # Extract first element
                preferences["duration"] = int(re.sub(r"\D", "", duration_str))  # Remove non-numeric characters

            # ✅ Fix: Ensure budget is an integer
            if "budget" in preferences and isinstance(preferences["budget"], list):
                preferences["budget"] = int(preferences["budget"][0])  # Convert string to int

        except json.JSONDecodeError:
            print("⚠️ JSON Parsing Failed. Response might not be in correct format.")
            preferences = {"tags": [], "duration": 0, "budget": 0}

        # ✅ Update state with extracted preferences
        state.update_preferences(preferences)

    else:
        print("❌ API Error:", response.text)

    return state  # Return updated state
