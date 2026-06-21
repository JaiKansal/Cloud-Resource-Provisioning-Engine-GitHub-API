import logging
import os
from datetime import datetime


def get_logger(name):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    os.makedirs("logs", exist_ok=True)
    log_filename = f"logs/execution_{datetime.now().strftime('%Y-%m-%d')}.log"

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
