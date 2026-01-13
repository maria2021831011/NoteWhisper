# NoteWhisper package init
"""
NoteWhisper - Convert lecture audio to structured notes with keypoints, summary, and quizzes
"""

__version__ = "0.1.0"
__author__ = "maria2021831011"
__email__ = "ritukhan534@gmail.com"

import logging

# Configure package logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# Import main components
from .cli import main, cli
from .transcribe import Transcriber
from .keypoints import KeypointExtractor
from .summarize import Summarizer
from .quiz import QuizGenerator
from .utils import (
    AudioProcessor,
    FileHandler,
    ConfigManager,
    NoteFormatter,
    download_sample_audio,
)

__all__ = [
    "main",
    "cli",
    "Transcriber",
    "KeypointExtractor",
    "Summarizer",
    "QuizGenerator",
    "AudioProcessor",
    "FileHandler",
    "ConfigManager",
    "NoteFormatter",
    "download_sample_audio",
    "__version__",
]