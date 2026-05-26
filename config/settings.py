from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
import json


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    # LLM
    anthropic_api_key: str = Field(..., alias="ANTHROPIC_API_KEY")

    # Web Research
    tavily_api_key: str = Field(..., alias="TAVILY_API_KEY")

    # Database
    mongodb_uri: str = Field(..., alias="MONGODB_URI")

    # Google Sheets
    google_service_account_json: Optional[str] = Field(None, alias="GOOGLE_SERVICE_ACCOUNT_JSON")

    # Email (SMTP)
    smtp_server: str = Field("smtp.gmail.com", alias="SMTP_SERVER")
    smtp_port: int = Field(587, alias="SMTP_PORT")
    smtp_email: str = Field(..., alias="SMTP_EMAIL")
    smtp_password: str = Field(..., alias="SMTP_PASSWORD")
    notification_email: str = Field(..., alias="NOTIFICATION_EMAIL")

    # Brand Config
    niche: str = Field("SaaS", alias="NICHE")
    platforms: list[str] = Field(["LinkedIn", "Instagram"], alias="PLATFORMS")
    brand_tone: str = Field("Professional", alias="BRAND_TONE")
    competitor_urls: Optional[list[str]] = Field(None, alias="COMPETITOR_URLS")

    # Logging
    log_level: str = Field("INFO", alias="LOG_LEVEL")

    def get_google_service_account(self) -> dict:
        if self.google_service_account_json:
            try:
                return json.loads(self.google_service_account_json)
            except json.JSONDecodeError:
                raise ValueError("Invalid Google service account JSON")
        return {}


settings = Settings()
