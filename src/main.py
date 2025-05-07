import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import load_config, Config
from config import setup_bot_logging, setup_aiogram_logging
from handlers import commands_router, default_router

setup_aiogram_logging()
logger = setup_bot_logging()

async def main() -> None:
    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')
    #set bot configuration
    config : Config = load_config()

    #bot initialization
    bot = Bot(
        token=config.tg_Bot.token
    )
    dp = Dispatcher()
    dp.include_routers(commands_router, default_router) 

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())