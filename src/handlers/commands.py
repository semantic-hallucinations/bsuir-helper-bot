from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

commands_router = Router()


@commands_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=(
            "Бот-ассистент Белорусского государственного"
            " университета информатики и радиоэлектроники."
        )
    )


@commands_router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(
        text="Вы можете задать любой интересующий вас вопрос по поводу поступления или учебы в БГУИР."
    )
