from loguru import logger

from experimentai_api.configs.settings import (EXPERIMENTAI_ERROR_LOGS_FILE,
                                               EXPERIMENTAI_LOGS_FILE)


def info_response_latency_only(record):
    """Helper function to filter out all levels except for INFO, RESPONSE, and LATENCY.
    This is used to control which messages are passed to the sink.
    """
    return record["level"].name in ["INFO", "RESPONSE", "LATENCY"]


def set_logger_configs() -> None:
    """Set custom logger configurations. Add sinks to record logs in specific files.
    Create levels for Response and Latency where each level has a name,
    a severity number (larger is more severe), and a color.
    """
    try:
        logger.level("RESPONSE", no=15, color="<green><bold>")
        logger.level("LATENCY", no=15, color="<blue><bold>")
    except ValueError as e:
        logger.warning(f'Level already exists: {e}')

    logger.add(EXPERIMENTAI_LOGS_FILE, filter=info_response_latency_only)
    logger.add(EXPERIMENTAI_ERROR_LOGS_FILE, level=30)  # WARNING, ERROR, and CRITICAL
