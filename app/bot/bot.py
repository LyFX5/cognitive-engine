import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from app.bot.handlers.start import start
from app.bot.handlers.voice import handle_voice
from app.bot.handlers.text import handle_text
from app.config.settings import settings
from app.transcription.whisper_service import WhisperService

logger = logging.getLogger(__name__)


def create_bot_application(whisper_service: WhisperService) -> Application:
    """Create and configure the Telegram bot application."""
    
    # Create the application
    application = (
        Application.builder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .build()
    )

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VOICE, lambda update, context: handle_voice(update, context, whisper_service)))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Bot application created successfully")
    return application