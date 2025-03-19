🌍 **Travel Planner AI Agent**  
An AI-powered travel planning assistant that extracts user preferences, finds suitable destinations, generates itineraries, and provides follow-up support. Built using LangChain and LangGraph.

---

## ✨ **Current Features**

**✅ Smart Destination Search** – Finds destinations based on at least two user-provided parameters (e.g., budget, duration).  
✅ **Itinerary Generation** – Creates detailed and personalized trip plans based on selected destinations.  
✅ **Follow-Up Support** – Users can refine their plans or get additional travel details seamlessly.  
✅ **Structured Workflow with LangGraph** – Ensures a systematic and scalable approach to travel planning.  
✅ **Comprehensive Testing** – Unit tests verify the correctness and reliability of various components.  

---

## 🔮 **Future Improvements**

### 🔹 **Enhancing Destination Discovery**
- If a user provides only one parameter (e.g., budget), the system will prompt for additional details (such as interests or preferred activities) to improve recommendations.

### 🔹 **Memory & Session Handling**
- Use a **Vector Database** to store previous chat interactions, enabling the model to recall past user preferences.
- Example: If a user asks, _"Where did I travel last time?"_, the system should retrieve and respond with past trip details.
- Implement **chat session management**, ensuring seamless conversation history retention.

### 🔹 **User Information Storage**
- Maintain a **user profile database** to store personal preferences (e.g., favorite travel destinations, frequently visited places, travel history).
- Example: If a user frequently visits beach destinations, the system can **recommend tropical locations** in future searches.

### 🔹 **Improved Error Handling**
- Enhance response accuracy when users ask location-related questions (e.g., _"Where is Manali located?"_).
- Implement a **question-handling module** using:
  1. **Pre-trained AI models** (e.g., OpenAI models for general knowledge queries).
  2. **Custom-trained model** on specific travel-related queries.

### 🔹 **Additional Features**
- **Flight Search Integration**: Use **Google Flights / Skyscanner API** to show real-time flight prices.
- **Hotel Recommendations**: Integrate hotel APIs to suggest accommodations.
- **Visa & Travel FAQ**: Train the model on frequently asked questions about **visa requirements**, travel regulations, and best travel seasons per country.

---

## 📂 **Project Structure**
```
travel_planner/
├── main.py                  # Entry point for the application
├── agent/
│   ├── graph.py             # LangGraph implementation
│   ├── nodes/               # Node implementations
│   │   ├── extract_preferences.py  # Extracts user preferences
│   │   ├── find_destination.py     # Finds the best travel destination
│   │   ├── create_itinerary.py     # Generates a travel itinerary
│   │   ├── handle_followup.py      # Handles follow-up questions
│   ├── tools/               # External tool connections (APIs, weather, etc.)
│   └── state.py             # State management
├── data/
│   └── destinations.json    # Mock destination database
├── tests/                   # Test suite
│   ├── test_create_itinerary.py   # Tests itinerary generation
│   ├── test_find_destination.py   # Tests destination search
│   ├── test_extract_preferences.py # Tests preference extraction
│   ├── test_handle_followup.py     # Tests follow-up questions
├── req.txt                  # Required Python dependencies
└── README.md                # Documentation
```

---

## ⚙️ **Installation**

Clone the repository:
```bash
git clone https://github.com/pruthvi4344/Travel_planner.git
cd travel_planner
```

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

Install dependencies:
```bash
pip install -r req.txt
```

---

## 🔑 **API Keys for Evaluation**
For the evaluation team, the **Mistral API Key** and **Weather API Key** have been included in the repository.  
These keys are provided **only for testing purposes** and cannot be used in production.

⚠️ **Important:**
- These keys might be revoked after the evaluation process.
- For future use, consider storing API keys securely in an **.env** file.

---

## 🚀 **Usage**

Run the main script:
```bash
python main.py
```

---

## 🧪 **Running Tests**

Run individual test files using:
```bash
python -m tests.test_create_itinerary
python -m tests.test_find_destination
python -m tests.test_extract_preferences
python -m tests.test_handle_followup
```

---

## 🛠️ **What Do These Tests Verify?**

| Test File                      | Purpose                                               |
|--------------------------------|------------------------------------------------------|
| test_create_itinerary.py       | Checks if itinerary generation is working correctly. |
| test_find_destination.py       | Verifies if the destination search is accurate.      |
| test_extract_preferences.py    | Ensures user preferences are correctly extracted.    |
| test_handle_followup.py        | Tests follow-up question handling.                   |

---

## 🤝 **Contributing**

Feel free to fork the project, make improvements, and submit a pull request.

---

## 📧 **Contact**

For any questions, reach out via **pruthvirathod2002@gmail.com**.

