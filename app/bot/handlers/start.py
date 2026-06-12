import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hello {user.first_name}! 👋\n\n"
        "I'm your Cognitive Engine assistant. Send me a voice message "
        "and I'll transcribe it to text for you."
    )
    logger.info(f"User {user.id} started the bot")