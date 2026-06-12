import logging
from pathlib import Path

import whisper

from app.config.settings import settings
from app.transcription.schemas import TranscriptionResult

logger = logging.getLogger(__name__)


class WhisperService:
    """Service for transcribing audio using Whisper."""

    def __init__(self):
        self.model = whisper.load_model(settings.WHISPER_MODEL)
        logger.info(f"Whisper model '{settings.WHISPER_MODEL}' loaded successfully")

    def transcribe(self, audio_path: str) -> TranscriptionResult:
        """
        Transcribe an audio file to text.

        Args:
            audio_path: Path to the audio file

        Returns:
            TranscriptionResult with text and paths
        """
        logger.info(f"Transcribing audio: {audio_path}")

        result = self.model.transcribe(audio_path)
        text = result["text"].strip()

        # Generate transcript filename from audio filename
        audio_file = Path(audio_path)
        transcript_filename = f"{audio_file.stem}.txt"
        transcript_path = settings.TRANSCRIPTS_DIR / transcript_filename

        # Save transcript to file
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(text)

        logger.info(f"Transcription saved to: {transcript_path}")

        return TranscriptionResult(
            text=text,
            audio_path=str(audio_path),
            transcript_path=str(transcript_path),
            language=result.get("language", "en"),
        )