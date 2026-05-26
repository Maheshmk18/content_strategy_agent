from tools.trend_scraper import scrape_trends
from tools.competitor_finder import find_competitors
from tools.competitor_scraper import scrape_competitors
from tools.analytics_reader import read_analytics
from tools.campaign_checker import check_campaigns
from langsmith import traceable
import asyncio


@traceable(name="run_research")
async def run_research(niche: str, month: str) -> dict:
    """
    Research agent: runs all 4 research tools in parallel.
    Automatically finds competitors based on niche.
    Returns consolidated research data.
    """
    try:
        # Step 1: Find competitors automatically based on niche
        competitor_urls = await asyncio.to_thread(
            find_competitors.invoke, {"niche": niche}
        )

        # Step 2: Run all 4 tools in parallel
        trends, competitors, analytics, campaigns = await asyncio.gather(
            asyncio.to_thread(scrape_trends.invoke, {"niche": niche, "month": month}),
            asyncio.to_thread(
                scrape_competitors.invoke, {"urls": competitor_urls}
            ),
            asyncio.to_thread(read_analytics.invoke, {}),
            asyncio.to_thread(check_campaigns.invoke, {}),
        )

    except Exception as e:
        print(f"Error in research agent: {e}")
        trends = [{"topic": "Error", "description": str(e)}]
        competitors = [{"url": "Error"}]
        analytics = []
        campaigns = []

    # Normalize data (ensure lists)
    trends = trends if isinstance(trends, list) else [trends]
    competitors = competitors if isinstance(competitors, list) else [competitors]
    analytics = analytics if isinstance(analytics, list) else [analytics]
    campaigns = campaigns if isinstance(campaigns, list) else [campaigns]

    return {
        "trends": trends,
        "competitor_posts": competitors,
        "top_posts": analytics,
        "campaigns": campaigns,
    }
