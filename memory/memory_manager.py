from memory.vector_store import save_plan_to_memory, query_similar_content
from graph.state import DayEntry


class MemoryManager:
    def __init__(self):
        pass

    async def save_approved_plan(self, calendar: list[DayEntry], month: str, niche: str):
        """Save an approved plan to vector memory."""
        save_plan_to_memory(calendar, month, niche)

    async def get_similar_past_content(self, query: str, niche: str) -> list[dict]:
        """Retrieve similar past content from memory."""
        return query_similar_content(query, niche)
