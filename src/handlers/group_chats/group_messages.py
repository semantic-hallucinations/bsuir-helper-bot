from aiogram import F, Router
from aiogram.types import Message

from config import BOT_USERNAME, get_logger
from services.api_service import ApiService

grp_msg_router = Router()
grp_msg_router.message.filter(F.chat.type.in_({"group", "supergroup"}))
logger = get_logger("bot.handlers")


@grp_msg_router.message(F.text)
async def process_text_message(message: Message):
    if message.text.startswith(f"@{BOT_USERNAME}"):
        query = (
            message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
        )
        if not query:
            await message.reply("Чтобы задать вопрос, напишите его после тега бота.")
            return

        try:
            response = await ApiService.get_response(query)
            await message.reply(response)
            logger.info(f"Successfuly handling user {message.from_user.id} request")
        except RuntimeError as e:
            await message.reply("Извините, бот временно недоступен. Попробуйте позже.")
            logger.error(f"Handling responce error: {e}")
