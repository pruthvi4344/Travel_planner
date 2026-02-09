import requests
import json, os
from agent.state import AgentState
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API keys securely
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("❌ MISTRAL_API_KEY is missing. Set it in your environment variables.")

# Mistral API URL
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def generate_itinerary_mistral(destination: str, duration: int) -> list:
    """
    Generate a day-by-day itinerary for the given destination using Mistral API.

    Args:
        destination (str): The selected travel destination.
        duration (int): The number of days for the trip.

    Returns:
        List[Dict]: A list of itinerary items.
    """

    # Constructing the prompt for Mistral
    # imprvoed the prompt
    prompt = f"""
    You are a travel expert. Create a detailed {duration}-day itinerary for a trip to {destination}.
    Include daily activities, recommended places to visit, and local experiences.
    
    Format the output as a structured JSON list:
    [
        {{"day": 1, "title": "Arrival and City Tour", "description": "Arrive in the city, check in to the hotel, and explore nearby attractions."}},
        {{"day": 2, "title": "Adventure and Sightseeing", "description": "Visit popular landmarks and enjoy a cultural experience."}}
    ]
    Only return a valid JSON list, nothing else.
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-small-latest",  # Choose an appropriate model
        "messages": [{"role": "user", "content": prompt}],  # ✅ Use user role
        "temperature": 0.7
    }

    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise error for bad response
        itinerary_data = response.json()

        # Debugging: Print full API response
        # print("🔍 Debug: Mistral API Response:", json.dumps(itinerary_data, indent=2))

        # Extract content from the response
        itinerary_text = itinerary_data["choices"][0]["message"]["content"].strip()

        # ✅ Fix: Remove triple backticks if they exist
        if itinerary_text.startswith("```json"):
            itinerary_text = itinerary_text[7:]  # Remove ```json
        if itinerary_text.endswith("```"):
            itinerary_text = itinerary_text[:-3]  # Remove closing ```

        # Convert response to JSON list
        try:
            itinerary_list = json.loads(itinerary_text)  # Convert JSON string to Python list
        except json.JSONDecodeError:
            print("❌ Error: Mistral API returned invalid JSON format.")
            return []

        if not itinerary_list:
            print("⚠️ Warning: Empty itinerary received from API.")
            return []

        return itinerary_list

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching itinerary from Mistral API: {e}")
        return []

def create_itinerary(state: AgentState) -> dict:
    """
    Create a detailed itinerary for the selected destination using Mistral API.

    Args:
        state (AgentState): Current state of the agent.

    Returns:
        dict: Updated state with the generated itinerary.
    """

    if not state.destinations:
        print("❌ No destinations selected. Cannot create an itinerary.")
        return state.model_dump()

    selected_destination = state.destinations[0]["name"]  # Get destination name
    duration = state.preferences.get("duration", 3)  # Default to 3 days if not specified

    print(f"\n📅 Generating itinerary for {selected_destination} for {duration} days...")  # ✅ Debugging

    # Fetch itinerary from Mistral API
    itinerary_plan = generate_itinerary_mistral(selected_destination, duration)

    if not itinerary_plan:
        print("⚠️ Warning: No itinerary generated. Returning empty plan.")
        return state.model_dump()

    state.itinerary = {
        "destination": selected_destination,
        "plan": itinerary_plan
    }

    print("\n✅ Itinerary successfully generated!\n")  # ✅ Confirmation
    return state.model_dump()  # Return updated state as a dictionary
