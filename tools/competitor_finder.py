from langchain_core.tools import tool
from tavily import TavilyClient
from config.settings import settings
from langsmith import traceable


tavily_client = TavilyClient(api_key=settings.tavily_api_key)


@tool
@traceable(name="find_competitors")
def find_competitors(niche: str) -> list[str]:
    """
    Automatically find top competitors in your niche using web search.
    Returns list of competitor website URLs.
    """
    try:
        # Search for top companies in the niche
        query = f"top companies in {niche} industry 2025"
        response = tavily_client.search(query, max_results=10)

        competitor_urls = []
        for result in response.get("results", []):
            url = result.get("url", "")
            # Extract main domain only (not deep links)
            if url and url.count("/") >= 2:
                # Get domain: https://example.com/blog → https://example.com
                parts = url.split("/")
                domain = f"{parts[0]}//{parts[2]}"
                if domain not in competitor_urls:
                    competitor_urls.append(domain)

        # Return top 5 competitors
        return competitor_urls[:5] if competitor_urls else _get_default_competitors(niche)

    except Exception as e:
        print(f"Error finding competitors: {e}")
        return _get_default_competitors(niche)


@traceable(name="get_default_competitors")
def _get_default_competitors(niche: str) -> list[str]:
    """Fallback: Return default competitors for common niches."""
    defaults = {
        "saas": [
            "https://hubspot.com",
            "https://intercom.com",
            "https://stripe.com",
            "https://slack.com",
            "https://asana.com",
        ],
        "ecommerce": [
            "https://shopify.com",
            "https://bigcommerce.com",
            "https://wix.com",
            "https://squarespace.com",
        ],
        "fitness": [
            "https://nike.com",
            "https://adidas.com",
            "https://peloton.com",
            "https://myfitnesspal.com",
        ],
        "agency": [
            "https://hubspot.com",
            "https://digital-agency.com",
            "https://marketingcloud.com",
        ],
    }

    niche_lower = niche.lower()
    return defaults.get(niche_lower, defaults["saas"])
