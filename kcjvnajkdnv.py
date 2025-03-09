import requests
import json
import os

# Using the API key as per your setup
api_key = os.environ["MISTRAL_API_KEY"] = "Rj6ZSCOL065j9Aj8xlOTjXhVOJehMX1l"

# Mistral API URL
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def extract_locations_with_mistral(user_input: str):
    """
    Uses Mistral API to extract only location-related keywords from user input.
    """

    system_prompt = """
                    from the below given sentence give me the tags that are used for location interests like this 
                    "tags": ["values"],
                    "duration" : ["values"],
                    "budget" : ["values"]
                    """
    

    payload = {
        "model": "mistral-small-latest",  # Replace with the correct model name
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
        extracted_text = response_data["choices"][0]["message"]["content"]
       

        try:
            preferences = json.loads(extracted_text)  # Convert to dictionary
        except json.JSONDecodeError:
            preferences = {"locations": []}  # Handle cases where response is not JSON


        
        return preferences  # Returning the structured response
    else:
        print("❌ Error:", response.text)
        return None

# Take user input from terminal
if __name__ == "__main__":
    user_input = input("Enter your travel preferences: ")
    extracted_data = extract_locations_with_mistral(user_input)
