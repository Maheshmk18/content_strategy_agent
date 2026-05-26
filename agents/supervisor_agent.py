from llm.chains import supervisor_chain
from config.settings import settings
from langsmith import traceable


@traceable(name="run_supervisor")
def run_supervisor(month: str) -> dict:
    """Supervisor agent: understands user goal and mission."""
    mission = supervisor_chain.invoke({
        "niche": settings.niche,
        "platforms": ", ".join(settings.platforms),
        "brand_tone": settings.brand_tone,
        "month": month,
    })

    return {
        "mission": mission,
        "niche": settings.niche,
        "platforms": settings.platforms,
        "brand_tone": settings.brand_tone,
    }
