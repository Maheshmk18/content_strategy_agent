from graph.state import AgentState
from agents.planner_agent import run_planner
from langsmith import traceable
from datetime import datetime


@traceable(name="planner_node")
async def planner_node(state: AgentState) -> AgentState:
    
    """Planner node: break mission into tasks."""
    
    mission = state.get("mission", "Generate a 30-day content plan")

    research_tasks = run_planner(mission)

    state.update({
        "research_tasks": research_tasks,
        "updated_at": datetime.utcnow().isoformat(),
    })

    return state
