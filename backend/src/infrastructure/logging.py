"""
Logging configuration using Loguru.

Sets up structured logging for the application with appropriate levels and formatting.
"""

import sys
from loguru import logger

# Configure logger
__all__ = ["logger"]


def setup_logging():
    """
    Configure Loguru logger for the application.
    
    Sets up:
    - Console output with formatting
    - Appropriate log levels
    - Structured logging format
    """
    # Remove default logger
    logger.remove()
    
    # Add console logger with custom format
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True,
    )
    
    # Add file logger for persistent logs
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="10 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
    )
    
    return logger


# Create logger instance
logger = setup_logging()