import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Bot configuration
    TELEGRAM_BOT_TOKEN: str = ""

    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_AUDIO_DIR: Path = DATA_DIR / "raw"
    TRANSCRIPTS_DIR: Path = DATA_DIR / "transcripts"

    # Whisper configuration
    WHISPER_MODEL: str = "base"

    class Config:
        env_file = ".env"
        extra = "ignore"

    def create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.RAW_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        self.TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)


settings = Settings()