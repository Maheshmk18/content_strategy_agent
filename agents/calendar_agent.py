from llm.chains import calendar_parser_chain
from graph.state import DayEntry
from langsmith import traceable
import json


@traceable(name="run_calendar_parser")
def run_calendar_parser(raw_plan: str) -> list[DayEntry]:
    
    """
    Calendar agent: parses raw content plan into structured 30-day entries.
    """
    
    try:
        result = calendar_parser_chain.invoke({"raw_plan": raw_plan})

        if isinstance(result, str):
            result = json.loads(result)

        calendar = []
        for entry in result:
            if isinstance(entry, dict) and "day" in entry:
                day_entry: DayEntry = {
                    "day": entry.get("day", 0),
                    "date": entry.get("date", ""),
                    "platform": entry.get("platform", ""),
                    "content_type": entry.get("content_type", ""),
                    "topic": entry.get("topic", ""),
                    "notes": entry.get("notes", ""),
                }
                calendar.append(day_entry)

        return calendar if calendar else _get_fallback_calendar()

    except Exception as e:
        print(f"Error parsing calendar: {e}")
        return _get_fallback_calendar()


@traceable(name="get_fallback_calendar")
def _get_fallback_calendar() -> list[DayEntry]:
    
    """Return a minimal fallback calendar."""
    
    calendar = []
    platforms = ["LinkedIn", "Instagram", "YouTube", "Facebook"]
    content_types = ["Post", "Reel", "Blog", "Ad", "Carousel"]

    for day in range(1, 31):
        platform = platforms[(day - 1) % len(platforms)]
        content_type = content_types[(day - 1) % len(content_types)]

        day_entry: DayEntry = {
            "day": day,
            "date": f"2025-06-{day:02d}",
            "platform": platform,
            "content_type": content_type,
            "topic": f"Content for Day {day}",
            "notes": "Generated from fallback",
        }
        calendar.append(day_entry)

    return calendar
