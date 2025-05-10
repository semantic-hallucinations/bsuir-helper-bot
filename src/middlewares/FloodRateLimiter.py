import time
from typing import Dict, Tuple

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.types import Message


# TODO: подумать как бот будет реагировать или не регаировать на флуд
class FloodRateLimiter(BaseMiddleware):
    def __init__(self, bot_username: str, timeout: int = 5):
        super().__init__()
        self.timeout = timeout
        self.bot_username = bot_username.lower()
        self.last_triggered: Dict[Tuple[int, int], float] = {}

    async def __call__(self, handler, event: Message, data: dict):
        if event.chat.type not in {"group", "supergroup"}:
            return await handler(event, data)

        if not event.entities or not event.text:
            return await handler(event, data)

        mentioned = any(
            e.type == "mention" and f"@{self.bot_username}" in event.text.lower()
            for e in event.entities
        )
        if not mentioned:
            return await handler(event, data)

        key = (event.chat.id, event.from_user.id)
        now = time.time()

        for k, timestamp in list(self.last_triggered.items()):
            if now - timestamp > 3600:
                del self.last_triggered[k]

        last = self.last_triggered.get(key)
        if last and now - last < self.timeout:
            await event.reply("⏳ Подождите немного перед следующим упоминанием.")
            raise CancelHandler()

        self.last_triggered[key] = now
        return await handler(event, data)
