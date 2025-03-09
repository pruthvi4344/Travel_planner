from langgraph.graph import StateGraph
from agent.state import AgentState
from agent.nodes.extract_preferences import extract_preferences
from agent.nodes.find_destinations import find_destinations
from agent.nodes.create_itinerary import create_itinerary
from agent.nodes.handle_followup import handle_followup

def build_travel_agent():
    """
    Create a LangGraph workflow for the Travel Planner AI Agent.

    Returns:
        A compiled LangGraph workflow.
    """

    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("extract_preferences", extract_preferences)
    workflow.add_node("find_destinations", find_destinations)
    workflow.add_node("create_itinerary", create_itinerary)
    workflow.add_node("handle_followup", handle_followup)

    # Define an explicit END node
    workflow.add_node("end", lambda state: state)  # Empty lambda function to stop execution

    # Define edges (workflow steps)
    workflow.add_edge("extract_preferences", "find_destinations")
    workflow.add_edge("find_destinations", "create_itinerary")

    # Conditional transition: If follow-up is required, go to handle_followup; otherwise, end
    def next_step(state):
        return "handle_followup" if state.history else "end"  # Now pointing to 'end' instead of None

    workflow.add_conditional_edges("create_itinerary", next_step)
    workflow.add_edge("handle_followup", "end")  # Explicitly ending at 'end'

    # Set entry point
    workflow.set_entry_point("extract_preferences")

    return workflow.compile()
