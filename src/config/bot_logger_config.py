import logging
import os
from logging.handlers import RotatingFileHandler

LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

_LOGGER_CONFIGS = {
    "bot": {
        "file": "bot.log",
        "console_level": logging.INFO,
        "file_level": logging.DEBUG,
    },
    "aiogram": {
        "file": "aiogram.log",
        "console_level": logging.WARNING,
        "file_level": logging.WARNING,
    },
    "bot.handlers": {
        "file": "handlers.log",
        "console_level": logging.INFO,
        "file_level": logging.DEBUG,
    },
    "bot.services": {
        "file": "services.log",
        "console_level": logging.INFO,
        "file_level": logging.DEBUG,
    },
}


def init_logging():
    formatter = logging.Formatter(
        (
            "%(filename)s:%(lineno)d #%(levelname)-8s "
            "[%(asctime)s] - %(name)s - %(message)s"
        )
    )

    for name, config in _LOGGER_CONFIGS.items():
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # prevent adding handlers multiple times
        if logger.handlers:
            continue

        logger.propagate = False

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(config["console_level"])
        console_handler.setFormatter(formatter)
        console_handler.stream.reconfigure(encoding="utf-8", errors="replace")
        logger.addHandler(console_handler)

        # File handler
        file_handler = RotatingFileHandler(
            os.path.join(LOGS_DIR, config["file"]),
            maxBytes=1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(config["file_level"])
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
