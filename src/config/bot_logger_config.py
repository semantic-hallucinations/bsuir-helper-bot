import logging
import os
from logging.handlers import RotatingFileHandler

from environs import Env

LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

env = Env()
env.read_env()


def setup_logger(name, log_file, console_level=logging.INFO, file_level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Устанавливаем минимальный уровень

    formatter = logging.Formatter(
        (
            "%(filename)s:%(lineno)d #%(levelname)-8s "
            "[%(asctime)s] - %(name)s - %(message)s"
        )
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)
    console_handler.stream.reconfigure(encoding="utf-8", errors="replace")
    logger.addHandler(console_handler)

    # File handler
    file_handler = RotatingFileHandler(
        os.path.join(LOGS_DIR, log_file),
        maxBytes=10 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def setup_bot_logging():
    return setup_logger("bot", "bot.log")


def setup_aiogram_logging():
    log_level = env.log_level("AIOGRAM_LOGGER_LEVEL", "WARNING")
    setup_logger("aiogram", "aiogram.log", log_level, log_level)


def setup_handlers_logging():
    return setup_logger("bot.handlers", "handlers.log", console_level=logging.WARNING)


def setup_services_logging():
    return setup_logger("bot.services", "services.log", console_level=logging.WARNING)
