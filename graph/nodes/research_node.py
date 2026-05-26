from graph.state import AgentState, ResearchData
from agents.research_agent import run_research
from langsmith import traceable
from datetime import datetime


@traceable(name="research_node")
async def research_node(state: AgentState) -> AgentState:
    
    """Research node: run all 4 tools in parallel via research agent."""
    
    month = state["month"]
    niche = state["niche"]

    # Call research agent
    research_data = await run_research(niche, month)

    # Convert to ResearchData TypedDict
    research_data_typed: ResearchData = {
        "trends": research_data.get("trends", []),
        "competitor_posts": research_data.get("competitor_posts", []),
        "top_posts": research_data.get("top_posts", []),
        "campaigns": research_data.get("campaigns", []),
    }

    state.update({
        "research_data": research_data_typed,
        "updated_at": datetime.utcnow().isoformat(),
    })

    return state
