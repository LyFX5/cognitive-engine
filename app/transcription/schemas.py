from pydantic import BaseModel


class TranscriptionResult(BaseModel):
    """Schema for transcription result."""

    text: str
    audio_path: str
    transcript_path: str
    language: str = "en"