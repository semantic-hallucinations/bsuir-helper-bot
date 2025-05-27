from collections import defaultdict
from typing import Any, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.types import Message

from config import BOT_USERNAME, get_logger

logger = get_logger("bot.handlers")


class GroupChatMsgTrottler(BaseMiddleware):
    def __init__(self):
        self.busy_users: Dict[int, bool] = defaultdict(lambda: False)
        self.warned_users: Dict[int, bool] = defaultdict(lambda: False)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Any],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        logger.info("IN GROUP MSG MIDDLEWARE")
        if event.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            return await handler(event, data)

        user_id = event.from_user.id

        bot_mentioned = event.text and BOT_USERNAME in event.text

        if not bot_mentioned:
            logger.info("BOT NOT MENTIONED")
            return
        if self.busy_users[user_id]:
            if not self.warned_users[user_id]:
                self.warned_users[user_id] = True
                await event.reply(
                    f"🔄 {event.from_user.first_name}, дождитесь ответа на предыдущий запрос."
                )
            return
        else:
            logger.info("BOT MENTIONED AND NUST ANSWER")
            self.busy_users[user_id] = True
            self.warned_users[user_id] = False
            try:
                return await handler(event, data)
            finally:
                self.busy_users[user_id] = False
