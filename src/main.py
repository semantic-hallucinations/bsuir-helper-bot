import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import Config, load_config, setup_aiogram_logging, setup_bot_logging
from handlers import commands_router, usr_msg_router

setup_aiogram_logging()
logger = setup_bot_logging()


async def main() -> None:
    # Выводим в консоль информацию о начале запуска бота
    logger.info("Starting bot")
    # set bot configuration
    config: Config = load_config()

    # bot initialization
    bot = Bot(
        token=config.tg_Bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
    )
    dp = Dispatcher()
    dp.include_routers(commands_router, usr_msg_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
