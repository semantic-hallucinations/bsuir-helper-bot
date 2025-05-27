from aiogram import F, Router
from aiogram.enums import ChatType, ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from config import BOT_USERNAME, get_logger
from middlewares import GroupChatMsgTrottler
from services.api_service import ApiService
from services.message_formatter import strip_markdown

grp_msg_router = Router()
grp_msg_router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))
grp_msg_router.message.middleware(GroupChatMsgTrottler())
logger = get_logger("bot.handlers")


@grp_msg_router.message(F.reply_to_message, F.text)
async def process_text_reply_message(message: Message):
    if message.text.startswith(f"@{BOT_USERNAME}"):
        logger.debug("REPLY HANDLER GROUP CHAT")
        query = (
            message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
        )
        if not query:
            await message.reply("Чтобы задать вопрос, напишите его после тега бота.")
            return
        try:
            replied_text = message.reply_to_message.text
            query = replied_text + " " + query
            response = await ApiService.get_response(query)

            try:
                await message.answer(response, parse_mode=ParseMode.MARKDOWN)
            except TelegramBadRequest as e:
                logger.error("Parsemode error for response: " + response)
                logger.error(e.message)
                await message.answer(strip_markdown(response))
                return

            logger.info(f"Successfuly handling user {message.from_user.id} request")
        except RuntimeError as e:
            await message.reply("Извините, бот временно недоступен. Попробуйте позже.")
            logger.error(f"Handling responce error: {e}")


@grp_msg_router.message(F.text)
async def process_text_message(message: Message):
    if message.text.startswith(f"@{BOT_USERNAME}"):
        logger.debug("ANSWER HANDLER GROUP CHAT")
        query = (
            message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
        )
        if not query:
            await message.reply("Чтобы задать вопрос, напишите его после тега бота.")
            return
        try:
            response = await ApiService.get_response(query)
            try:
                await message.answer(response, parse_mode=ParseMode.MARKDOWN)
            except TelegramBadRequest as e:
                logger.error("Parsemode error for response: " + response)
                logger.error(e.message)
                await message.answer(strip_markdown(response))
                return
            logger.info(f"Successfuly handling user {message.from_user.id} request")
        except RuntimeError as e:
            await message.reply("Извините, бот временно недоступен. Попробуйте позже.")
            logger.error(f"Handling responce error: {e}")


@grp_msg_router.message(~F.text)
async def process_non_text_message(message: Message):
    await message.answer(
        text="На данный момент бот не работает только с текстовыми запросами."
    )
