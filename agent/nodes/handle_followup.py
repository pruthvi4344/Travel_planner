import requests
import json
import os
from agent.state import AgentState  # ✅ Import AgentState model

# Ensure API Key is set
api_key = os.environ["MISTRAL_API_KEY"] = "Rj6ZSCOL065j9Aj8xlOTjXhVOJehMX1l"
WEATHER_API_KEY = os.environ["WEATHER_API_KEY"] = "84547c88296d4b1eb8073747250903"


if not api_key:
    raise ValueError("❌ MISTRAL_API_KEY is missing. Set it in your environment variables.")

if not WEATHER_API_KEY:
    raise ValueError("❌ WEATHER_API_KEY is missing. Set it in your environment variables.")

# ✅ API URLs
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
WEATHER_API_URL = "http://api.weatherapi.com/v1/forecast.json"

def get_weather(destination_name):
    """
    Fetches a 3-day weather forecast for the given destination.
    
    Args:
        destination_name (str): Name of the city.

    Returns:
        str: Weather forecast summary.
    """
    params = {
        "key": WEATHER_API_KEY,
        "q": destination_name,  # ✅ WeatherAPI requires city name, NOT lat/lon
        "days": 3,  # ✅ Free plan allows only 3 days
        "aqi": "no",
        "alerts": "no"
    }

    response = requests.get(WEATHER_API_URL, params=params)
    
    if response.status_code != 200:
        print("❌ WEATHER API ERROR:", response.text)  # ✅ Debugging
        return "⚠️ Unable to fetch weather forecast. Please try again."

    data = response.json()
    
    if "forecast" not in data:
        print("❌ WEATHER API RESPONSE MISSING FORECAST DATA:", data)  # ✅ Debugging
        return "⚠️ No weather data available."

    forecast_days = data["forecast"]["forecastday"]
    forecast_message = f"📅 **Weather Forecast for {destination_name} (Next 3 Days):**\n"

    for day in forecast_days:
        date = day["date"]
        temp = day["day"]["avgtemp_c"]
        condition = day["day"]["condition"]["text"]
        forecast_message += f"🗓️ {date}: {condition}, 🌡️ {temp}°C\n"

    return forecast_message

def handle_followup(state: AgentState) -> dict:
    """
    Handles user follow-up questions and integrates weather data.

    Args:
        state (AgentState): Current state of the agent.

    Returns:
        dict: Updated state with response.
    """
    user_question = state.user_input.lower().strip()

    if not state.destinations:
        state.response = "⚠️ No selected destination. Please choose a destination first."
        return state.model_dump()

    selected_destination = state.destinations[0]
    destination_name = selected_destination.get("name", "Unknown Location")

    # ✅ Get weather info
    weather_info = get_weather(destination_name)
    print("\n✅ DEBUG: Weather Info Fetched Successfully!\n", weather_info)  # ✅ Debugging

    # ✅ Mistral AI prompt modification
    system_prompt = f"""
    The user has selected {destination_name} as their travel destination.
    {weather_info}

    Provide a specific and relevant response for {destination_name} to the following question:
    If not found, respond appropriately for whatever the user has asked.
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

    # ✅ Send request to Mistral API
# ✅ Send request to Mistral API
    response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
     response_data = response.json()
     ai_response = response_data["choices"][0]["message"]["content"]
    
    # ✅ Only include AI response (not repeating weather_info)
     state.response = f"🤖 AI: {ai_response}"
    else:
     print("❌ Mistral API Error:", response.text)
     state.response = "I'm having trouble processing your request. Please try again."

    return state.model_dump()