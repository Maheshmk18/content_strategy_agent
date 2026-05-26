from graph.state import AgentState
from langsmith import traceable
from datetime import datetime


@traceable(name="notifier_node")
async def notifier_node(state: AgentState) -> AgentState:
    
    """Notifier node: send email and save to Google Sheets."""
    
    plan_id = state["plan_id"]
    calendar = state["calendar"]
    month = state["month"]

    # Placeholder: in real implementation, this would call output layer functions
    # to send email and save to Google Sheets

    state.update({
        "status": "notification_pending",
        "updated_at": datetime.utcnow().isoformat(),
    })

    return state
