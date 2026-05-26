from langchain_core.tools import tool
from langsmith import traceable
import yaml
from pathlib import Path


@tool
@traceable(name="check_campaigns")
def check_campaigns(config_file: str = None) -> list[dict]:
    """
    Check active campaigns and product launches for the current month.
    Returns a list of campaigns to consider in the content plan.
    """
    if config_file and Path(config_file).exists():
        try:
            with open(config_file, "r") as f:
                data = yaml.safe_load(f)
                campaigns = data.get("campaigns", [])
                return campaigns if campaigns else _get_fallback_campaigns()

        except Exception as e:
            return [{"error": str(e), "fallback": True}]

    return _get_fallback_campaigns()


@traceable(name="get_fallback_campaigns")
def _get_fallback_campaigns() -> list[dict]:
    return [
        {
            "name": "Summer Sale",
            "start_date": "2025-06-01",
            "end_date": "2025-06-30",
            "focus": "Promotional content",
        },
        {
            "name": "New Product Launch",
            "start_date": "2025-06-15",
            "end_date": "2025-06-30",
            "focus": "Educational + promotional",
        },
        {
            "name": "Webinar Series",
            "start_date": "2025-06-10",
            "end_date": "2025-06-30",
            "focus": "Educational content",
        },
    ]
