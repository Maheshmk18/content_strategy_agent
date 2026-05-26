from langchain_core.tools import tool
from langsmith import traceable
import csv
from pathlib import Path

@tool
@traceable(name="read_analytics")
def read_analytics(csv_file: str = None) -> list[dict]:
    
    """
    Read past post performance data from a CSV file or fallback data.
    Returns top 5 performing content topics.
    """
    if csv_file and Path(csv_file).exists():
        try:
            top_posts = []
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i >= 5:
                        break
                    top_posts.append({
                        "topic": row.get("topic", ""),
                        "engagement": row.get("engagement", "0"),
                        "platform": row.get("platform", ""),
                        "type": row.get("content_type", ""),
                    })
            return top_posts if top_posts else _get_fallback_data()

        except Exception as e:
            return [{"error": str(e), "fallback": True}]

    return _get_fallback_data()


@traceable(name="get_fallback_analytics")
def _get_fallback_data() -> list[dict]:
    return [
        {
            "topic": "How-to guides",
            "engagement": "High",
            "platform": "LinkedIn",
            "type": "Post",
        },
        {
            "topic": "Industry tips",
            "engagement": "High",
            "platform": "Instagram",
            "type": "Carousel",
        },
        {
            "topic": "Case studies",
            "engagement": "Medium",
            "platform": "LinkedIn",
            "type": "Article",
        },
        {
            "topic": "Behind the scenes",
            "engagement": "Medium",
            "platform": "Instagram",
            "type": "Reel",
        },
        {
            "topic": "Product updates",
            "engagement": "Medium",
            "platform": "LinkedIn",
            "type": "Post",
        },
    ]
