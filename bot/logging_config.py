import logging
import os

def setup_logging(log_filename="trading_bot.log"):
    """Set up logging to console and file."""
    # Create logger
    logger = logging.getLogger('TradingBot')
    logger.setLevel(logging.DEBUG)

    # Avoid adding handlers multiple times in interactive environments
    if logger.handlers:
        return logger

    # Log format
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File handler
    file_handler = logging.FileHandler(log_filename, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)

    # Console handler (WARNING and above, since CLI uses Rich for regular output)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(log_format)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create a default logger to import elsewhere
logger = setup_logging()
