"""Production-ready FastAPI application for TTS Labs."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.schemas import (
    HealthResponse,
    TTSRequest,
    TTSResponse,
    VoiceInfo,
    VoiceListResponse,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("=" * 50)
    logger.info(f"Starting {settings.app_name}")
    logger.info(f"Sample Rate: {settings.sample_rate} Hz")
    logger.info(f"Default Model: {settings.default_model}")
    logger.info(f"Output Directory: {settings.output_directory}")
    logger.info("=" * 50)
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")


# Create FastAPI app
app = FastAPI(
    title="TTS Labs API",
    version="0.1.0",
    description="High-quality neural text-to-speech API",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint providing service information.
    
    Returns:
        Dictionary with service name, version, and status.
    """
    return {
        "service": "TTS Labs",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Health check endpoint.
    
    Returns:
        HealthResponse with current service status and configuration.
    """
    return HealthResponse(
        status="healthy",
        model=settings.default_model,
        sample_rate=settings.sample_rate,
    )


@app.get("/v1/voices", response_model=VoiceListResponse)
async def list_voices() -> VoiceListResponse:
    """Get list of available voices.
    
    Returns:
        VoiceListResponse containing available voice information.
    """
    return VoiceListResponse(
        voices=[
            VoiceInfo(
                name="narrator_v1",
                language="en",
                gender="neutral",
                premium=True,
            )
        ]
    )


@app.post("/v1/tts", response_model=TTSResponse)
async def synthesize(request: TTSRequest) -> TTSResponse:
    """Synthesize text to speech.
    
    Args:
        request: TTSRequest containing text and synthesis parameters.
        
    Returns:
        TTSResponse with synthesized audio information.
    """
    # Placeholder implementation
    return TTSResponse(
        success=True,
        audio_file="outputs/demo.wav",
        duration_seconds=0.0,
        sample_rate=settings.sample_rate,
        voice=request.voice,
        model=settings.default_model,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
