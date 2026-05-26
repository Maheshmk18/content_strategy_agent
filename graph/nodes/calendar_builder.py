from graph.state import AgentState
from llm.chains import content_plan_chain
from agents.calendar_agent import run_calendar_parser
from langsmith import traceable
from datetime import datetime


@traceable(name="calendar_builder_node")
async def calendar_builder_node(state: AgentState) -> AgentState:
    
    """Calendar builder node: generate content plan and structure it."""
    
    research_data = state["research_data"]
    platforms = state["platforms"]
    niche = state["niche"]
    brand_tone = state["brand_tone"]

    # Format research data for the prompt
    trends_text = ", ".join([t.get("topic", "") for t in research_data["trends"][:5]])
    competitor_text = ", ".join([c.get("url", "") for c in research_data["competitor_posts"][:3]])
    top_posts_text = ", ".join([p.get("topic", "") for p in research_data["top_posts"][:3]])
    campaigns_text = ", ".join([c.get("name", "") for c in research_data["campaigns"][:3]])

    # Generate raw content plan
    raw_plan = await _generate_content_plan(
        trends_text,
        competitor_text,
        top_posts_text,
        campaigns_text,
        ", ".join(platforms),
        niche,
        brand_tone,
    )

    state.update({
        "content_plan": raw_plan,
    })

    # Parse into structured calendar
    calendar = run_calendar_parser(raw_plan)

    state.update({
        "calendar": calendar,
        "status": "pending",
        "updated_at": datetime.utcnow().isoformat(),
    })

    return state


@traceable(name="generate_content_plan")
async def _generate_content_plan(
    trends, competitors, top_posts, campaigns, platforms, niche, brand_tone
) -> str:
    """Generate the raw content plan using LLM."""
    try:
        plan = content_plan_chain.invoke({
            "trends": trends or "No specific trends found",
            "competitor_posts": competitors or "No competitor data available",
            "top_posts": top_posts or "No past performance data",
            "campaigns": campaigns or "No active campaigns",
            "platforms": platforms,
            "niche": niche,
            "brand_tone": brand_tone,
        })
        return plan
    except Exception as e:
        print(f"Error generating content plan: {e}")
        return ""
