from db.mongo.client import get_db
from db.mongo.models import PlanModel
from datetime import datetime
import uuid


class PlanRepository:
    def __init__(self):
        self.collection_name = "plans"

    async def save_plan(self, month: str, niche: str, platforms: list, status: str = "pending") -> str:
        db = get_db()
        plan_id = str(uuid.uuid4())
        plan = {
            "plan_id": plan_id,
            "month": month,
            "niche": niche,
            "platforms": platforms,
            "status": status,
            "created_at": datetime.utcnow(),
            "approved_at": None,
        }
        await db[self.collection_name].insert_one(plan)
        return plan_id

    async def get_plan(self, plan_id: str) -> dict:
        db = get_db()
        plan = await db[self.collection_name].find_one({"plan_id": plan_id})
        return plan

    async def update_status(self, plan_id: str, status: str):
        db = get_db()
        update_data = {"status": status}
        if status == "approved":
            update_data["approved_at"] = datetime.utcnow()

        await db[self.collection_name].update_one(
            {"plan_id": plan_id},
            {"$set": update_data},
        )

    async def get_by_month(self, month: str) -> list:
        db = get_db()
        plans = await db[self.collection_name].find({"month": month}).to_list(None)
        return plans
