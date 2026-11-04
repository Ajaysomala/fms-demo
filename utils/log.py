import logging
import os
from pathlib import Path


def get_logger(name):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    Path("logs").mkdir(exist_ok=True)
    for handler in (logging.StreamHandler(), logging.FileHandler("logs/automation.log", encoding="utf-8")):
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    logger.propagate = False
    return logger
