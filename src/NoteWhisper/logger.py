# src/NoteWhisper/logger.py

import os
import sys
import logging

# -----------------------------
# Logging configuration
# -----------------------------
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)

# Log file path
log_filepath = os.path.join(log_dir, "running_logs.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout),
    ],
)

# Logger instance
logger = logging.getLogger("NoteWhisper")

# Example usage
if __name__ == "__main__":
    logger.info("Logger initialized for NoteWhisper package.")
