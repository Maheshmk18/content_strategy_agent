from graph.state import AgentState
from agents.supervisor_agent import run_supervisor
from langsmith import traceable
from datetime import datetime


@traceable(name="supervisor_node")
async def supervisor_node(state: AgentState) -> AgentState:
    """Supervisor node: understand the mission."""
    month = state["month"]

    result = run_supervisor(month)

    state.update({
        "mission": result["mission"],
        "niche": result["niche"],
        "platforms": result["platforms"],
        "brand_tone": result["brand_tone"],
        "updated_at": datetime.utcnow().isoformat(),
    })

    return state
