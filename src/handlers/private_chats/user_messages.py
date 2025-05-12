from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.types import Message

from config import get_logger
from middlewares import PrivateChatMsgTrottler
from services.api_service import ApiService

usr_msg_router = Router()
usr_msg_router.message.middleware(PrivateChatMsgTrottler())
usr_msg_router.message.filter(F.chat.type == ChatType.PRIVATE)
logger = get_logger("bot.handlers")


@usr_msg_router.message(F.reply_to_message, F.text)
async def process_text_reply_message(message: Message):
    try:
        logger.debug("REPLY HANDLER PRIVATE CHAT")
        replied_text = message.reply_to_message.text
        query = replied_text + " " + message.text
        response: str = await ApiService.get_response(query)
        await message.answer(response)
        logger.info(f"Successfuly handling user {message.from_user.id} request")
    except RuntimeError as e:
        await message.answer("Извините, бот временно недоступен. Попробуйте позже.")
        logger.error(f"Handling responce error: {e}")


@usr_msg_router.message(F.text)
async def process_text_message(message: Message):
    try:
        logger.debug("ANSWER HANDLER PRIVATE CHAT")
        response: str = await ApiService.get_response(message.text)
        await message.answer(response)
        logger.info(f"Successfuly handling user {message.from_user.id} request")
    except RuntimeError as e:
        await message.answer("Извините, бот временно недоступен. Попробуйте позже.")
        logger.error(f"Handling responce error: {e}")


@usr_msg_router.message(~F.text)
async def process_non_text_message(message: Message):
    await message.answer(
        text="На данный момент бот не работает только с текстовыми запросами."
    )
