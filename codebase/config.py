import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def _parse_guild_id() -> int:
    val = (os.getenv("DISCORD_GUILD_ID") or "").strip()
    try:
        return int(val) if val else 0
    except (ValueError, TypeError):
        return 0

@dataclass(frozen=True)
class Settings:
    discord_bot_token: str = (os.getenv("DISCORD_BOT_TOKEN") or "").strip()
    discord_guild_id: int = _parse_guild_id()

    ai_base_url: str = os.getenv("AI_BASE_URL", "https://openrouter.ai/api/v1")
    ai_api_key: str = os.getenv("AI_API_KEY", "")
    ai_model: str = os.getenv("AI_MODEL", "")

    timezone: str = os.getenv("TIMEZONE", "Asia/Ho_Chi_Minh")
    message_limit_per_channel: int = int(os.getenv("MESSAGE_LIMIT_PER_CHANNEL", "40"))
    reminder_minutes_before: int = int(os.getenv("REMINDER_MINUTES_BEFORE", "30"))
    reminder_poll_seconds: int = int(os.getenv("REMINDER_POLL_SECONDS", "20"))

    db_path: str = os.getenv("DB_PATH", "data/assistant.db")
    max_channels_per_summary: int = int(os.getenv("MAX_CHANNELS_PER_SUMMARY", "10"))

settings = Settings()
