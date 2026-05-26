from langchain_anthropic import ChatAnthropic
from config.settings import settings

llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    api_key=settings.anthropic_api_key,
    temperature=0.7,
    max_tokens=4096,
)
