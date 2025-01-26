import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Configures logging for the app."""
    # Create a logger
    logger = logging.getLogger('my_app')
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Create a file handler for logging
    file_handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    file_handler.setLevel(logging.INFO)

    # Create a console handler for debugging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create a formatter and attach it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
