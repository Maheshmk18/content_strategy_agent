from llm.chains import planner_chain
from config.settings import settings
from langsmith import traceable


@traceable(name="run_planner")
def run_planner(mission: str) -> list[str]:
    """Planner agent: breaks mission into research tasks."""
    task_text = planner_chain.invoke({
        "mission": mission,
        "niche": settings.niche,
        "platforms": ", ".join(settings.platforms),
    })

    tasks = [line.strip() for line in task_text.split("\n") if line.strip() and line[0].isdigit()]
    return tasks if tasks else ["Research trends", "Scrape competitors", "Read analytics", "Check campaigns"]
