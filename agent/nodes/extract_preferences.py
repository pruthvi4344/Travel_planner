
import requests
import json
import os
import re
from dotenv import load_dotenv

from agent.state import AgentState  # Import AgentState model

# Load environment variables
load_dotenv()

# Fetch API keys securely
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError(" MISTRAL_API_KEY is missing. Set it in your environment variables.")

# Mistral API URL
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def extract_preferences(state: AgentState) -> AgentState:
    """Extracts travel-related preferences from user input using Mistral API.
       Also handles greetings and asks for travel details if missing.
    """

    user_input = state.user_input.strip().lower()  #  Normalize input

    system_prompt = """
    You are a smart travel assistant. Your task is to do two things:
    
    1. If the user is greeting (like "Hello", "Hi", "Good morning"), respond with:
       "Hello! I can help you plan a trip. Tell me your budget, duration, and interests, and I'll suggest the best places!"
       
    2. If the user asks about a trip, extract travel preferences in **strict JSON format**:
    {
        "tags": ["shopping", "nightlife"],
        "duration": 5,
        "budget": 20000,
        "country": "India",
        "name": "Jaipur"
    }

    - **Always return a valid JSON.**  
    - **Do NOT wrap the response in markdown code blocks (` ```json ... ``` `).**
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

    response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response_data = response.json()
        extracted_text = response_data["choices"][0]["message"]["content"].strip()

        # Check if response is a greeting or JSON
        if extracted_text.startswith("{") and extracted_text.endswith("}"):
            try:
                preferences = json.loads(extracted_text)  # Convert to dictionary
                
                #  Ensure duration is an integer
                if "duration" in preferences:
                    preferences["duration"] = int(re.sub(r"\D", "", str(preferences["duration"])))

                #  Ensure budget is an integer
                if "budget" in preferences:
                    preferences["budget"] = int(re.sub(r"\D", "", str(preferences["budget"])))

                #  Update state with extracted preferences
                state.update_preferences(preferences)

            except json.JSONDecodeError:
                # print(" JSON Parsing Failed. Response might not be in correct format.")
                state.response = "I'm having trouble processing your request. Please try again."
        
        else:
            #  Handle greetings or non-JSON responses
            state.response = extracted_text

    else:
        print(" API Error:", response.text)
        state.response = "There was an issue with processing your request."

    return state  # Return updated state