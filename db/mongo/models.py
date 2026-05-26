from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime


class DayModel(BaseModel):
    day: int
    date: str
    platform: str
    content_type: str
    topic: str
    notes: str


class ResearchDataModel(BaseModel):
    research_id: str
    plan_id: str
    trends: List[dict] = Field(default_factory=list)
    competitor_posts: List[dict] = Field(default_factory=list)
    top_posts: List[dict] = Field(default_factory=list)
    campaigns: List[dict] = Field(default_factory=list)
    gathered_at: datetime


class PlanModel(BaseModel):
    plan_id: str
    month: str
    niche: str
    platforms: List[str]
    status: str             # pending | approved | rejected
    created_at: datetime
    approved_at: Optional[datetime] = None


class CalendarModel(BaseModel):
    calendar_id: str
    plan_id: str
    days: List[DayModel]
    quality_score: int
    status: str         # draft | approved | published
    created_at: datetime


class ResultModel(BaseModel):
    result_id: str
    plan_id: str
    sheet_url: Optional[str] = None
    email_sent: bool
    notification_email: str
    sent_at: datetime
