from collections import defaultdict
from typing import Any, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.types import Message

from config import get_logger

logger = get_logger("bot.handlers")


class PrivateChatMsgTrottler(BaseMiddleware):
    def __init__(self):
        self.busy_users: Dict[int, bool] = defaultdict(lambda: False)
        self.warned_users: Dict[int, bool] = defaultdict(lambda: False)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Any],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        logger.info("IN PRIVATE CHAT MIDDLEWARE")
        if event.chat.type != ChatType.PRIVATE:
            logger.info("SEND MSG TO HANDLERS")
            return await handler(event, data)

        user_id = event.from_user.id
        if self.busy_users[user_id]:
            if not self.warned_users[user_id]:
                self.warned_users[user_id] = True
                await event.reply(
                    "⏳ Пожалуйста, дождитесь завершения предыдущего запроса."
                )
            return
        else:
            self.busy_users[user_id] = True
            self.warned_users[user_id] = False
            try:
                return await handler(event, data)
            finally:
                self.busy_users[user_id] = False
