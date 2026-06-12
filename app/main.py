import logging
import asyncio

from app.bot.bot import create_bot_application
from app.config.logging import setup_logging
from app.config.settings import settings
from app.transcription.whisper_service import WhisperService

logger = logging.getLogger(__name__)


def main() -> None:
    """Main entry point for the application."""
    # Setup logging
    setup_logging()
    logger.info("Starting Cognitive Engine...")

    # Create necessary directories
    settings.create_directories()
    logger.info("Data directories created")

    # Initialize Whisper service
    logger.info("Initializing Whisper service...")
    whisper_service = WhisperService()

    # Create bot application
    logger.info("Creating bot application...")
    application = create_bot_application(whisper_service)

    # Start the bot
    logger.info("Starting bot polling...")
    application.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()