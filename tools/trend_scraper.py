from langchain_core.tools import tool
from tavily import TavilyClient
from config.settings import settings
from langsmith import traceable

tavily_client = TavilyClient(api_key=settings.tavily_api_key)


@tool
@traceable(name="scrape_trends")
def scrape_trends(niche: str, month: str) -> list[dict]:
    """
    Search the web for trending topics in a given niche for the current month.
    Returns top 10 trending topics.
    """
    try:
        query = f"{niche} trends {month} 2025"
        response = tavily_client.search(query, max_results=10)

        trends = []
        for result in response.get("results", []):
            trends.append({
                "topic": result.get("title", ""),
                "description": result.get("content", ""),
                "source": result.get("url", ""),
            })

        return trends if trends else [{"topic": "No specific trends found", "description": "", "source": ""}]

    except Exception as e:
        return [{"topic": "Error fetching trends", "description": str(e), "source": ""}]
