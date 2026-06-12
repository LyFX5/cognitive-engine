import logging

from telegram import Update
from telegram.ext import ContextTypes

from app.transcription.whisper_service import WhisperService

logger = logging.getLogger(__name__)


async def handle_voice(
    update: Update, context: ContextTypes.DEFAULT_TYPE, whisper_service: WhisperService
) -> None:
    """Handle voice messages."""
    message = update.message
    user = update.effective_user

    # Get the voice file
    voice_file = await message.voice.get_file()
    logger.info(f"Received voice message from user {user.id}")

    # Download the voice file
    audio_path = f"{voice_file.file_unique_id}.ogg"
    await voice_file.download_to_drive(audio_path)
    logger.info(f"Voice message saved to: {audio_path}")

    # Send acknowledgment
    await message.reply_text("🎤 Transcribing your voice message...")

    try:
        # Transcribe the audio
        result = whisper_service.transcribe(audio_path)
        logger.info(f"Transcription completed for user {user.id}")

        # Return the transcribed text
        await message.reply_text(f"📝 *Transcription:*\n\n{result.text}", parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error transcribing voice message: {e}")
        await message.reply_text(
            "❌ Sorry, I encountered an error while transcribing your message. Please try again."
        )