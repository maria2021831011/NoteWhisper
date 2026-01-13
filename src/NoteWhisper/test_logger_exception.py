# src/NoteWhisper/test_logger_exception.py

from NoteWhisper.logger import logger
from NoteWhisper.exceptions import InvalidURLException

# Example log message
logger.info("This is a test log message from test_logger_exception.py")

# Example of raising and logging a custom exception
try: 
    raise InvalidURLException("This URL is invalid for NoteWhisper!")
except Exception as e:
    logger.error(f"Caught an exception: {e}")
