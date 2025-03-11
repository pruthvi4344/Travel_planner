🌍 **Travel Planner AI Agent**  
An AI-powered travel planning assistant that extracts user preferences, finds suitable destinations, generates itineraries, and provides follow-up support. Built using LangChain and LangGraph.

---

### ✨ **Features**
✅ Extracts user preferences from input  
✅ Finds the best travel destinations  
✅ Generates complete itineraries  
✅ Handles follow-up questions  
✅ Uses LangGraph for structured workflow  
✅ Includes unit tests to verify node functionality  

---

### 📂 **Project Structure**
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

### ⚙️ **Installation**
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

### 🔑 **API Keys for Evaluation**
For the evaluation team, the **Mistral API Key** and **Weather API Key** have been included in the repository.  
These keys are provided **only for testing purposes** and can **not be used in production**.  

⚠️ **Important:**
- These keys might be revoked after the evaluation process.
- For future use, consider storing API keys securely in an `.env` file.

---

### 🚀 **Usage**
Run the main script:  
```bash
python main.py
```

---

### 🧪 **Running Tests**
To ensure that the nodes are working correctly, run the test suite:

Run all tests:
```bash
pytest tests/
```
Run individual test files using:
```bash
python -m tests.test_create_itinerary
python -m tests.test_find_destination
python -m tests.test_extract_preferences
python -m tests.test_handle_followup
```

---

### 🛠️ **What Do These Tests Verify?**
| Test File                     | Purpose                                      |
|-------------------------------|----------------------------------------------|
| `test_create_itinerary.py`    | Checks if itinerary generation is working correctly. |
| `test_find_destination.py`    | Verifies if the destination search returns relevant locations. |
| `test_extract_preferences.py` | Tests whether user preferences are correctly extracted. |
| `test_handle_followup.py`     | Ensures follow-up questions are handled properly. |

---

### 🤝 **Contributing**
Feel free to fork the project, make improvements, and submit a pull request.

---

### 📧 **Contact**
For any questions, reach out via [pruthvirathod2002@gmail.com](mailto:pruthvirathod2002@gmail.com).

