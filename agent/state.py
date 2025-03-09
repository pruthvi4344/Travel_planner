from pydantic import BaseModel
from typing import Dict, List, Any,Optional

class AgentState(BaseModel):
    user_input: str = ""  # Stores the latest user input
    preferences: Dict[str, Any] = {}  # Stores user preferences
    destinations: List[Dict[str, Any]] = []  # List of matched destinations
    itinerary: Dict[str, Any] = {}  # Stores the planned itinerary
    destination_message: Optional[str] = None  # ✅ Add this field
    history: List[Dict[str, str]] = []  # Stores conversation history
    response: str = ""  # Stores response for follow-ups

    def update_preferences(self, new_preferences: Dict[str, Any]):
        """Update user preferences."""
        self.preferences.update(new_preferences)

    def add_destination(self, destination: Dict[str, Any]):
        """Add a recommended destination."""
        self.destinations.append(destination)

    def set_itinerary(self, itinerary: Dict[str, Any]):
        """Set itinerary details."""
        self.itinerary = itinerary

    # ✅ Fix compatibility with Pydantic v1 and v2
    def to_dict(self):
        if hasattr(self, "model_dump"):  # ✅ Pydantic v2 support
            return self.model_dump()
        return self.dict()  # ✅ Pydantic v1 fallback
