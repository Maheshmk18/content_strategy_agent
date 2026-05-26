from langgraph.graph import StateGraph, START, END
from langsmith import traceable
from graph.state import AgentState
from graph.nodes.supervisor import supervisor_node
from graph.nodes.planner import planner_node
from graph.nodes.research_node import research_node
from graph.nodes.decision import decision_node
from graph.nodes.calendar_builder import calendar_builder_node
from graph.nodes.notifier import notifier_node


@traceable(name="build_graph")
def build_graph():
    
    """Build the LangGraph workflow."""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("research", research_node)
    workflow.add_node("decision", decision_node)
    workflow.add_node("calendar_builder", calendar_builder_node)
    workflow.add_node("notifier", notifier_node)

    # Define edges
    workflow.add_edge(START, "supervisor")
    workflow.add_edge("supervisor", "planner")
    workflow.add_edge("planner", "research")
    workflow.add_edge("research", "decision")
    

    # Conditional edge from decision
    def route_decision(state: AgentState):
        next_action = state.get("next_action", "continue")
        if next_action == "retry":
            return "research"
        else:
            return "calendar_builder"


    workflow.add_conditional_edges(
        "decision",
        route_decision,
        {"research": "research", "calendar_builder": "calendar_builder"},
    )


    workflow.add_edge("calendar_builder", "notifier")
    workflow.add_edge("notifier", END)

    return workflow.compile()


# create the compiled graph

graph = build_graph()
