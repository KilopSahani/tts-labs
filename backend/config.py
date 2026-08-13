"""Production-ready configuration for TTS Labs using Pydantic Settings."""

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration using Pydantic Settings.
    
    Environment variables can override any of these defaults by using the
    setting name in uppercase (e.g., APP_NAME, SAMPLE_RATE, etc.)
    """

    # Application settings
    app_name: str = "TTS Labs"
    
    # Audio processing settings
    sample_rate: int = 24000
    default_model: str = "kokoro"
    default_voice: str = "narrator_v1"
    
    # Output settings
    output_directory: Path = Path("outputs")
    
    class Config:
        """Pydantic Settings configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def __init__(self, **data):
        """Initialize settings and create output directory if it doesn't exist."""
        super().__init__(**data)
        self.output_directory.mkdir(parents=True, exist_ok=True)


# Create a singleton instance for application-wide use
settings = Settings()
