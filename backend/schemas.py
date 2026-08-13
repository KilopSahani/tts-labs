"""Pydantic schemas for TTS Labs API using Pydantic v2."""

from pydantic import BaseModel, Field


class TTSRequest(BaseModel):
    """Request schema for text-to-speech synthesis.
    
    Attributes:
        text: The text to synthesize (must not be empty).
        voice: The voice identifier to use for synthesis.
        speed: Speech rate multiplier (0.5x to 2.0x).
        emotion: Emotional tone for the synthesis.
        stream: Whether to stream the audio response.
    """

    text: str = Field(
        ...,
        min_length=1,
        description="Text to synthesize (must not be empty)"
    )
    voice: str = Field(
        default="narrator_v1",
        description="Voice identifier for synthesis"
    )
    speed: float = Field(
        default=1.0,
        ge=0.5,
        le=2.0,
        description="Speech rate multiplier (0.5 to 2.0)"
    )
    emotion: str = Field(
        default="neutral",
        description="Emotional tone for synthesis"
    )
    stream: bool = Field(
        default=False,
        description="Whether to stream the audio response"
    )


class TTSResponse(BaseModel):
    """Response schema for text-to-speech synthesis results.
    
    Attributes:
        success: Whether the synthesis was successful.
        audio_file: Path or URL to the generated audio file.
        duration_seconds: Length of the generated audio in seconds.
        sample_rate: Sample rate of the audio in Hz.
        voice: The voice used for synthesis.
        model: The model used for synthesis.
    """

    success: bool = Field(
        description="Whether the synthesis was successful"
    )
    audio_file: str = Field(
        description="Path or URL to the generated audio file"
    )
    duration_seconds: float = Field(
        ge=0,
        description="Duration of the generated audio in seconds"
    )
    sample_rate: int = Field(
        gt=0,
        description="Sample rate of the audio in Hz"
    )
    voice: str = Field(
        description="The voice used for synthesis"
    )
    model: str = Field(
        description="The model used for synthesis"
    )


class HealthResponse(BaseModel):
    """Response schema for health check endpoint.
    
    Attributes:
        status: Current health status of the service.
        model: Currently loaded TTS model.
        sample_rate: Current audio sample rate in Hz.
    """

    status: str = Field(
        description="Current health status (e.g., 'healthy', 'degraded')"
    )
    model: str = Field(
        description="Currently loaded TTS model"
    )
    sample_rate: int = Field(
        gt=0,
        description="Current audio sample rate in Hz"
    )


class VoiceInfo(BaseModel):
    """Information about an available voice.
    
    Attributes:
        name: Unique identifier for the voice.
        language: Language code (e.g., 'en', 'fr').
        gender: Gender presentation of the voice ('male', 'female', 'neutral').
        premium: Whether this is a premium voice requiring special access.
    """

    name: str = Field(
        description="Unique identifier for the voice"
    )
    language: str = Field(
        description="Language code (e.g., 'en', 'fr')"
    )
    gender: str = Field(
        description="Gender presentation ('male', 'female', 'neutral')"
    )
    premium: bool = Field(
        default=False,
        description="Whether this is a premium voice"
    )


class VoiceListResponse(BaseModel):
    """Response schema for listing available voices.
    
    Attributes:
        voices: List of available voice information objects.
    """

    voices: list[VoiceInfo] = Field(
        description="List of available voices"
    )
