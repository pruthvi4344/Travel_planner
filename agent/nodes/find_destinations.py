import json
from agent.state import AgentState

def load_destinations(file_path: str = "data/destinations.json") -> list:
    """Load destinations from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading destinations: {e}")
        return []

def find_destinations(state: AgentState) -> dict:
    """
    Find suitable destinations based on user preferences and return structured data.

    Args:
        state (AgentState): Current state of the agent.

    Returns:
        dict: Updated state with matched destinations and structured details.
    """

    preferences = state.preferences
    destinations = load_destinations()

    if not isinstance(destinations, list):
        destinations = []

    matched_destinations = []
    alternative_destinations = []

    print(f"🔍 Debug: Received Preferences in find_destinations.py: {preferences}")

    for destination in destinations:
        # Extract user preferences
        user_budget = preferences.get("budget", 0)
        user_duration = preferences.get("duration", 0)
        user_tags = preferences.get("tags", [])
        user_country = preferences.get("country", "").lower()
        user_name = preferences.get("name", "").lower()

        # Extract destination attributes
        destination_budget = destination.get("budget_range", [0, 999999])
        ideal_duration = destination.get("ideal_duration", [0, 999])
        destination_tags = destination.get("tags", [])
        destination_country = destination.get("country", "").lower()
        destination_name = destination.get("name", "").lower()

        # Matching criteria  
        budget_match = destination_budget[0] <= user_budget <= destination_budget[1]
        duration_match = ideal_duration[0] <= user_duration <= ideal_duration[1]
        tag_match = bool(set(user_tags) & set(destination_tags))
        country_match = user_country and user_country == destination_country
        name_match = user_name and user_name == destination_name

        # Flexible criteria
        flexible_budget = destination_budget[0] * 0.8 <= user_budget <= destination_budget[1] * 1.2
        flexible_duration = ideal_duration[0] * 0.8 <= user_duration <= ideal_duration[1] * 1.2
        partial_tag_match = bool(set(user_tags) & set(destination_tags)) or not user_tags

        # ✅ Strong match (Exact match)
        if budget_match and duration_match and tag_match and country_match:
            matched_destinations.append(destination)
        # ✅ Alternative match (Flexible match)
        elif flexible_budget and flexible_duration and partial_tag_match:
            alternative_destinations.append(destination)

    # ✅ If no perfect match, return alternative recommendations
    if not matched_destinations:
        matched_destinations = alternative_destinations

    # ✅ Store structured data
    structured_destinations = []
    for dest in matched_destinations:
        structured_destinations.append({
            "name": dest["name"],
            "country": dest["country"],
            "budget": f"₹{dest['budget_range'][0]} - ₹{dest['budget_range'][1]}",
            "duration": f"{dest['ideal_duration'][0]}-{dest['ideal_duration'][1]} days",
            "activities": dest.get("tags", []),
            "best_time": dest.get("best_time", "N/A")
        })

    # ✅ Generate a user-friendly message  
    if structured_destinations:
        response_message = "🌍 Based on your preferences, here are some great destinations:\n\n"
        for idx, dest in enumerate(structured_destinations, start=1):
            response_message += (
                f"{idx}️⃣ **{dest['name']}**, {dest['country']}\n"
                # f"   🌤 Best Time: {dest['best_time']}\n"
                f"   🎯 Activities: {', '.join(dest['activities'])}\n"
                f"   💰 Budget: {dest['budget']}\n"
                f"   📅 Recommended Duration: {dest['duration']}\n\n"
            )
    else:
        response_message = "❌ Sorry, no exact matches found! Try different preferences."

    # ✅ Store response in `destination_message`
    state.destinations = structured_destinations
    state_dict = state.model_dump()  
    state_dict["destination_message"] = response_message  

    return state_dict  
