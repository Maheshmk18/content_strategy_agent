from typing import TypedDict, Optional, Any
from datetime import datetime


class ResearchData(TypedDict):
    trends: list[dict]
    competitor_posts: list[dict]
    top_posts: list[dict]
    campaigns: list[dict]


class DayEntry(TypedDict):
    day: int
    date: str
    platform: str
    content_type: str
    topic: str
    notes: str


class AgentState(TypedDict):
    # Core metadata
    month: str
    niche: str
    platforms: list[str]
    brand_tone: str
    plan_id: str

    # Research phase
    research_tasks: list[str]
    research_data: ResearchData

    # Planning phase
    content_plan: str

    # Calendar phase
    calendar: list[DayEntry]

    # Quality & status
    quality_score: int
    status: str  # pending | approved | rejected
    retry_count: int
    max_retries: int

    # Error handling
    error: Optional[str]

    # Timestamps
    created_at: str
    updated_at: str
