from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

commands_router = Router()
commands_router.message.filter(F.chat.type == ChatType.PRIVATE)


@commands_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=(
            "Я - бот-ассистент Белорусского государственного"
            " университета информатики и радиоэлектроники.\n"
            "Готов ответить на все вопросы об университете!"
        )
    )


@commands_router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(
        text=(
            "Вы можете задать мне любой интересующий вас вопрос"
            " по поводу поступления или учебы в БГУИР."
            " Напишите мне сообщение."
        )
    )
