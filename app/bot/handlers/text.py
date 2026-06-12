import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages."""
    message = update.message
    user = update.effective_user

    logger.info(f"Received text message from user {user.id}: {message.text}")

    # For now, just echo back the text (placeholder for future functionality)
    await message.reply_text(f"You said: {message.text}")