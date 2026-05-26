from db.mongo.client import get_db
from datetime import datetime
import uuid


class ResultRepository:
    def __init__(self):
        self.collection_name = "results"

    async def save_calendar(self, plan_id: str, calendar_data: list, quality_score: int) -> str:
        db = get_db()
        calendar_id = str(uuid.uuid4())
        calendar = {
            "calendar_id": calendar_id,
            "plan_id": plan_id,
            "days": calendar_data,
            "quality_score": quality_score,
            "status": "draft",
            "created_at": datetime.utcnow(),
        }
        await db["calendars"].insert_one(calendar)
        return calendar_id

    async def get_calendar(self, plan_id: str) -> dict:
        db = get_db()
        calendar = await db["calendars"].find_one({"plan_id": plan_id})
        return calendar

    async def save_result(self, plan_id: str, sheet_url: str, notification_email: str) -> str:
        db = get_db()
        result_id = str(uuid.uuid4())
        result = {
            "result_id": result_id,
            "plan_id": plan_id,
            "sheet_url": sheet_url,
            "email_sent": True,
            "notification_email": notification_email,
            "sent_at": datetime.utcnow(),
        }
        await db["results"].insert_one(result)
        return result_id
