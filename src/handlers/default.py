from aiogram import Router
from aiogram.types import Message
from services.api_service import ApiService
import io
from aiogram.types import BufferedInputFile
from aiogram import F

# Инициализация сервиса
api_service = ApiService()

default_router = Router()


@default_router.message()
async def process_message(message: Message):
    model_answer = await api_service.get_response(message.text)

    if model_answer.startswith("Ассистент недоступен сейчас. Посмотрите на картинку кота:"):
        image_url = model_answer.split("\n")[-1]  
        await message.answer_photo(
            caption=model_answer.split("\n")[0],
            photo=image_url
        )
    else:
        await message.answer(
            text=model_answer
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