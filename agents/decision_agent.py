from llm.chains import decision_chain
from graph.state import ResearchData
from langsmith import traceable


@traceable(name="run_decision")
def run_decision(research_data: ResearchData, retry_count: int) -> dict:
    
    """
    Decision agent: evaluates research quality and decides next step.
    Returns: {"score": int, "decision": str, "reason": str}
    """
    
    data_summary = f"Trends: {len(research_data.get('trends', []))} items, Competitors: {len(research_data.get('competitor_posts', []))} posts, Top posts: {len(research_data.get('top_posts', []))} items, Campaigns: {len(research_data.get('campaigns', []))} campaigns"

    try:
        result = decision_chain.invoke({
            "research_data": data_summary,
            "retry_count": f"{retry_count}",
        })
        return result

    except Exception as e:
        return {
            "score": 7,
            "decision": "continue",
            "reason": f"Error in decision making, proceeding anyway: {str(e)}",
        }
