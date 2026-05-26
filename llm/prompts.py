from langchain_core.prompts import PromptTemplate


# Supervisor: Understand user intent and read config
SUPERVISOR_PROMPT = PromptTemplate(
    input_variables=["niche", "platforms", "brand_tone", "month"],
    template="""You are the Supervisor node of a content strategy agent. Your job is to understand the mission and prepare the team.

The user wants a 30-day content calendar for {month}.

Niche: {niche}
Platforms: {platforms}
Brand Tone: {brand_tone}

Summarize the mission in 1-2 sentences. What research should the team prioritize?
""",
)


# Planner: Break mission into research tasks
PLANNER_PROMPT = PromptTemplate(
    input_variables=["mission", "niche", "platforms"],
    template="""You are the Planner. Break this mission into specific, actionable research tasks:

Mission: {mission}

Niche: {niche}
Platforms: {platforms}

List 4-5 research tasks. Examples:
1. Search for trending topics in [{niche}] this month
2. Scrape competitor social pages (last 30 days of posts)
3. Analyze our past post performance (top-performing topics)
4. Check active campaigns and product launches
5. Identify seasonal events or industry news for [{niche}]

Return as a numbered list.
""",
)


# Main Content Plan: Generate 30-day calendar
CONTENT_PLAN_PROMPT = PromptTemplate(
    input_variables=[
        "trends",
        "competitor_posts",
        "top_posts",
        "campaigns",
        "platforms",
        "niche",
        "brand_tone",
    ],
    template="""You are a content strategist. Generate a 30-day content calendar based on research data.

RESEARCH DATA:
Trending Topics: {trends}
Competitor Content: {competitor_posts}
Our Top Performing Topics: {top_posts}
Active Campaigns: {campaigns}

REQUIREMENTS:
Platforms: {platforms}
Niche: {niche}
Brand Tone: {brand_tone}

For EACH of the 30 days, suggest:
- Platform (one of: {platforms})
- Content Type (Post, Reel, Blog, Ad, Carousel, Story, Video)
- Topic/Title
- Brief notes or hook

Format as:
Day 1: Platform=LinkedIn, Type=Post, Topic=..., Notes=...
Day 2: Platform=Instagram, Type=Reel, Topic=..., Notes=...
[continue for all 30 days]

Ensure variety in platforms, content types, and topics. Align with trends and campaigns.
""",
)


# Decision: Evaluate research quality
DECISION_PROMPT = PromptTemplate(
    input_variables=["research_data", "retry_count"],
    template="""You are a quality evaluator. Rate the research data quality (1-10) and decide next step.

Research Data Summary:
- Trends found: {research_data}
- Retry count: {retry_count}/3

Rate the quality:
- Score 8-10: Excellent data, proceed with calendar
- Score 5-7: Decent data, could improve but acceptable
- Score 1-4: Poor data, recommend retry

Return JSON:
{{"score": <int>, "decision": "<continue|retry>", "reason": "<brief reason>"}}
""",
)


# Calendar Parser: Convert raw plan to structured format
CALENDAR_PARSER_PROMPT = PromptTemplate(
    input_variables=["raw_plan"],
    template="""Parse this raw content plan into structured JSON format.

Raw Plan:
{raw_plan}

Return a JSON array of 30 objects:
[
  {{"day": 1, "date": "2025-06-01", "platform": "LinkedIn", "content_type": "Post", "topic": "...", "notes": "..."}},
  {{"day": 2, "date": "2025-06-02", "platform": "Instagram", "content_type": "Reel", "topic": "...", "notes": "..."}}
  ...
]

Ensure all 30 days are present. Use valid platform names and content types.
""",
)
