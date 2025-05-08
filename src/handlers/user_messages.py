from aiogram import F, Router
from aiogram.types import Message

from config import setup_handlers_logging
from services.api_service import ApiService

usr_msg_router = Router()
logger = setup_handlers_logging()


@usr_msg_router.message(F.text)
async def process_text_message(message: Message):
    try:
        response = await ApiService.get_response(message.text)
        await message.answer(response)
        logger.info("Successfuly handling user request")
    except RuntimeError as e:
        await message.answer("Извините, сервис временно недоступен. Попробуйте позже.")
        logger.error(f"Handling responce error: {e}")


@usr_msg_router.message()
async def process_non_text_message(message: Message):
    await message.answer(
        text="На данный момент бот не работает только с текстовыми запросами."
    )
