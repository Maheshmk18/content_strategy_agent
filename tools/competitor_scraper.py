from langchain_core.tools import tool
from config.settings import settings
from langsmith import traceable


@tool
@traceable(name="scrape_competitors")
def scrape_competitors(urls: list[str] = None) -> list[dict]:
    """Scrape competitor sites for recent content (last 30 days)."""
    if not urls:
        urls = settings.competitor_urls or []

    if not urls:
        return [{"url": "No competitor URLs configured", "posts": []}]

    return _get_mock_competitor_data(urls)


@traceable(name="get_mock_competitor_data")
def _get_mock_competitor_data(urls: list[str]) -> list[dict]:
    """Return mock competitor data."""
    mock_posts = [
        {"title": "Latest SaaS trends for 2025", "excerpt": "Discover the top trends shaping the SaaS industry this year"},
        {"title": "How to scale your startup", "excerpt": "Expert tips on scaling from 10 to 100 employees"},
        {"title": "Best practices in product design", "excerpt": "What separates great products from good ones"},
        {"title": "AI integration guide", "excerpt": "How to leverage AI in your business operations"},
        {"title": "Customer retention strategies", "excerpt": "Proven tactics to reduce churn and boost lifetime value"},
    ]

    return [{"url": url, "posts": mock_posts} for url in urls]
