from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from llm.client import llm
from llm.prompts import (
    SUPERVISOR_PROMPT,
    PLANNER_PROMPT,
    CONTENT_PLAN_PROMPT,
    DECISION_PROMPT,
    CALENDAR_PARSER_PROMPT,
)

# Supervisor Chain
supervisor_chain = (
    SUPERVISOR_PROMPT
    | llm
    | StrOutputParser()
)

# Planner Chain
planner_chain = (
    PLANNER_PROMPT
    | llm
    | StrOutputParser()
)

# Content Plan Chain (generates raw 30-day plan)
content_plan_chain = (
    CONTENT_PLAN_PROMPT
    | llm
    | StrOutputParser()
)

# Decision Chain (evaluates quality)
decision_chain = (
    DECISION_PROMPT
    | llm
    | JsonOutputParser()
)

# Calendar Parser Chain (converts raw plan to JSON)
calendar_parser_chain = (
    CALENDAR_PARSER_PROMPT
    | llm
    | JsonOutputParser()
)
