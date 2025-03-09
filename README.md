# Travel Planner AI Agent

An AI-powered travel planning assistant that extracts user preferences, finds suitable destinations, generates itineraries, and provides follow-up support. Built using **LangChain** and **LangGraph**.

## Features
- Extracts user preferences from input
- Finds the best travel destinations
- Generates complete itineraries
- Handles follow-up questions
- Uses LangGraph for structured workflow

## Project Structure
```
travel_planner/
├── main.py                  # Entry point for the application
├── agent/
│   ├── graph.py             # LangGraph implementation
│   ├── nodes/               # Node implementations (extract, find destination, etc.)
│   ├── tools/               # External tool connections
│   └── state.py             # State management
├── data/
│   └── destinations.json    # Mock destination database
├── req.txt                  # Required Python dependencies
└── README.md                # Documentation
```

## Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/pruthvi4344/Travel_planner.git
   cd travel_planner
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r req.txt
   ```

## Usage
Run the main script:
```bash
python main.py
```


## Contributing
Feel free to fork the project, make improvements, and submit a pull request.


## Contact
For any questions, reach out via [pruthvirathod2002@gmail.com].

