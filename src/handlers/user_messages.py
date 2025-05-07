from aiogram import F, Router
from aiogram.types import Message

from services.api_service import ApiService
from config import setup_handlers_logging
# Инициализация сервиса
api_service = ApiService()

usr_msg_router = Router()
logger = setup_handlers_logging()

@usr_msg_router.message(F.text)
async def process_text_message(message: Message):
    try:
        response = await ApiService.get_response(message.text)
        await message.answer(response)
    except RuntimeError as e:
        await message.answer("Извините, сервис временно недоступен. Попробуйте позже.")
        logger.error(f"Handling responce error: {e}")


@usr_msg_router.message()
async def process_non_text_message(message: Message):
    await message.answer(
        text="На данный момент бот не работает только с текстовыми запросами."
    )


# @default_router.message(F.text.lower().contains("грузин"))
# async def process_message(message: Message):
#     model_answer = await api_service.get_response(message.text)
#     if isinstance(model_answer, io.BytesIO):
#         await message.answer_photo(
#             caption="Ассистент занят. Посмотрите на грузина:",
#             photo=BufferedInputFile(
#                 model_answer.getvalue(),
#                 filename="gruzin.jpg"
#             )
#         )
#     else:
#         await message.answer(text=model_answer)

# @default_router.message()
# async def process_message(message: Message):
#     await message.answer(text="Ничем не могу помочь:(. Но если написать 'грузин'...")
