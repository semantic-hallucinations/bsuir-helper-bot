from dataclasses import dataclass

from environs import Env


@dataclass
class BsuirAssistantBot:
    token: str


@dataclass
class Config:
    tg_Bot: BsuirAssistantBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_Bot=BsuirAssistantBot(token=env("BOT_TOKEN")))


env = Env()
env.read_env()
BOT_USERNAME = env("BOT_USERNAME")
