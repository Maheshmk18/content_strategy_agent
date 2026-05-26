"""
Tool to import your company's past post data into MongoDB.
This helps the agent learn what content works best for YOUR audience.
"""

from db.mongo.client import get_db
from datetime import datetime
import uuid


async def import_company_analytics(analytics_data: list[dict]) -> dict:
    """
    Import your company's past post analytics into MongoDB.

    Args:
        analytics_data: List of dicts with:
        {
            "topic": "10 SaaS Tools",
            "engagement": 2000,
            "platform": "LinkedIn",
            "content_type": "Post",
            "date": "2025-05-01",
            "notes": "List format performs well"
        }

    Returns:
        {"status": "success", "count": 5, "collection": "company_analytics"}
    """
    try:
        db = get_db()
        collection = db["company_analytics"]

        for item in analytics_data:
            doc = {
                "id": str(uuid.uuid4()),
                "topic": item.get("topic", ""),
                "engagement": item.get("engagement", 0),
                "platform": item.get("platform", ""),
                "content_type": item.get("content_type", ""),
                "date": item.get("date", ""),
                "notes": item.get("notes", ""),
                "imported_at": datetime.utcnow(),
            }
            await collection.insert_one(doc)

        return {
            "status": "success",
            "count": len(analytics_data),
            "message": f"Imported {len(analytics_data)} analytics records"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


async def import_company_campaigns(campaigns_data: list[dict]) -> dict:
    """
    Import your active campaigns into MongoDB.

    Args:
        campaigns_data: List of dicts with:
        {
            "name": "Summer Sale",
            "start_date": "2025-06-01",
            "end_date": "2025-06-30",
            "focus": "Promotional content"
        }
    """
    try:
        db = get_db()
        collection = db["campaigns"]

        for item in campaigns_data:
            doc = {
                "id": str(uuid.uuid4()),
                "name": item.get("name", ""),
                "start_date": item.get("start_date", ""),
                "end_date": item.get("end_date", ""),
                "focus": item.get("focus", ""),
                "imported_at": datetime.utcnow(),
            }
            await collection.insert_one(doc)

        return {
            "status": "success",
            "count": len(campaigns_data),
            "message": f"Imported {len(campaigns_data)} campaign records"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


async def get_top_performing_content(platform: str = None, limit: int = 5) -> list[dict]:
    """
    Retrieve your top performing past content.
    Agent uses this to create similar content.

    Args:
        platform: Filter by platform (LinkedIn, Instagram, etc)
        limit: How many records to return
    """
    try:
        db = get_db()
        collection = db["company_analytics"]

        query = {}
        if platform:
            query["platform"] = platform

        # Sort by engagement (descending) and limit
        results = await collection.find(query).sort("engagement", -1).limit(limit).to_list(None)
        return results if results else []

    except Exception as e:
        print(f"Error getting top content: {e}")
        return []
