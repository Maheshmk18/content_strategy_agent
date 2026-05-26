from graph.state import AgentState
from agents.decision_agent import run_decision
from langsmith import traceable
from datetime import datetime


@traceable(name="decision_node")
async def decision_node(state: AgentState) -> AgentState:
    """Decision node: evaluate research quality and decide next step."""
    research_data = state["research_data"]
    retry_count = state["retry_count"]

    decision_result = run_decision(research_data, retry_count)

    quality_score = decision_result.get("score", 5)
    decision = decision_result.get("decision", "continue")

    # Increment retry count
    new_retry_count = retry_count + 1

    # Force continue if max retries exceeded
    if new_retry_count >= state["max_retries"]:
        decision = "continue"

    state.update({
        "quality_score": quality_score,
        "retry_count": new_retry_count,
        "updated_at": datetime.utcnow().isoformat(),
        "next_action": decision,  # "continue" or "retry"
    })

    return state
