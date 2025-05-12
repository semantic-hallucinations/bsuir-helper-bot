import asyncio

from aiogram import Bot, Dispatcher

# from aiogram.client.default import DefaultBotProperties
# from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config, get_logger, init_logging, load_config
from handlers import commands_router, grp_msg_router, usr_msg_router

init_logging()
logger = get_logger("bot")


async def main() -> None:
    logger.info("Starting bot")
    config: Config = load_config()

    bot = Bot(
        token=config.tg_Bot.token,
        # default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )

    mem_storage = MemoryStorage()
    dp = Dispatcher(storage=mem_storage)
    dp.include_routers(commands_router, usr_msg_router, grp_msg_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
