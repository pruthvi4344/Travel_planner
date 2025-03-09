import os
import json
import re
import requests
from agent.state import AgentState
from agent.nodes.extract_preferences import extract_preferences
from agent.nodes.find_destinations import find_destinations
from agent.nodes.create_itinerary import create_itinerary
from agent.nodes.handle_followup import handle_followup  # ✅ Import follow-up handling

def process_user_choice(state: AgentState):
    """
    Handles user's choice after getting recommendations or an itinerary.
    """
    while True:
        user_choice = input("\n👉 Enter 1 for new recommendations, 2 to choose a destination for itinerary, 3 to exit: ")

        if user_choice == "1":
            print("\n🔄 Getting new recommendations...")
            return main()

        elif user_choice == "2":
            if not state.destinations:
                print("⚠️ No destinations available to choose from!")
                continue

            print("\n🌍 Please choose a destination for your itinerary:")
            for idx, dest in enumerate(state.destinations, start=1):
                print(f"{idx}️⃣ {dest['name']} ({dest['country']})")

            while True:
                try:
                    selection = int(input("\n👉 Enter the number of your preferred destination: ")) - 1
                    if 0 <= selection < len(state.destinations):
                        selected_destination = state.destinations[selection]
                        print(f"\n✅ You selected: {selected_destination['name']}, {selected_destination['country']}")

                        print("\n📅 Generating your personalized itinerary...\n")
                        state.destinations = [selected_destination]
                        itinerary_response = create_itinerary(state)

                        print(f"\n📍 **Itinerary for {selected_destination['name']}**\n")
                        for day in itinerary_response.get("itinerary", {}).get("plan", []):
                            print(f"🗓️ **Day {day['day']}**: {day['title']}")
                            print(f"   {day['description']}\n")

                        handle_post_itinerary_options(state)
                        return
                    else:
                        print("⚠️ Invalid selection. Please choose a valid number.")
                except ValueError:
                    print("⚠️ Please enter a valid number.")

        elif user_choice == "3":
            print("\n👋 Exiting Travel Planner. Have a great day!")
            exit(0)
        else:
            print("⚠️ Invalid input. Please enter 1, 2, or 3.")

def handle_post_itinerary_options(state: AgentState):
    """Handles user choices after itinerary generation, including follow-ups."""
    while True:
        user_input = input("\n👉 Enter 1 for new recommendations, 2 for follow-up questions, 3 to exit: ").strip()

        if user_input == "1":
            print("\n🔄 Restarting for new recommendations...")
            return main()

        elif user_input == "2":
            user_question = input("\n💬 Ask your follow-up question: ")
            state.user_input = user_question
            followup_response = handle_followup(state)  # ✅ Call follow-up handler
            print("\n🤖 AI Response:", followup_response.get("response", "No response received."))

        elif user_input == "3":
            print("\n👋 Thank you for using the Travel Planner AI Agent! Have a great trip! ✈️")
            exit(0)
        else:
            print("❌ Invalid input. Please enter 1, 2, or 3.")

def main():
    print("\n🚀 Welcome to the Travel Planner AI Agent!")
    state = AgentState()
    user_input = input("\n📝 Tell me about your trip (budget, duration, interests): ")
    state.user_input = user_input

    print("\n🔍 Extracting Preferences...")
    state = extract_preferences(state)

    # ✅ Handle greeting responses
    if state.response:
        print("\n🤖 AI Response:", state.response)
        return  # Stops execution if it's just a greeting

    # ✅ Check if preferences were extracted
    if not state.preferences or not any(state.preferences.values()):
        print("⚠️ No valid travel details found! Please provide budget, duration, and interests.")
        return main()

    print("✅ Preferences Extracted:", state.preferences)

    print("\n🔍 Finding Suitable Destinations...")
    state_dict = find_destinations(state)
    destination_message = state_dict.get("destination_message", "No recommendations found.")
    print("\n📢 Travel Recommendations:\n")
    print(destination_message)
    state.destinations = state_dict.get("destinations", [])

    process_user_choice(state)

if __name__ == "__main__":
    main()
