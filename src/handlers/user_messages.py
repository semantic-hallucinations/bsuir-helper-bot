from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from config import setup_handlers_logging
from services.api_service import ApiService

from .fsm_states import ProcessReqest

usr_msg_router = Router()
logger = setup_handlers_logging()


@usr_msg_router.message(F.text, StateFilter(default_state))
async def process_text_message(message: Message, state: FSMContext):
    await state.set_state(ProcessReqest.waiting)
    try:
        response: str = await ApiService.get_response(message.text)
        await message.answer(response)
        logger.info(f"Successfuly handling user {message.from_user.id} request")
    except RuntimeError as e:
        await message.answer("Извините, сервис временно недоступен. Попробуйте позже.")
        logger.error(f"Handling responce error: {e}")
    finally:
        await state.clear()


@usr_msg_router.message(StateFilter(ProcessReqest.waiting))
async def waiting_response_notify(message: Message, state: FSMContext):
    logger.debug(
        f"Waiting state while handling response user {message.from_user.id}'s request"
    )
    await message.reply(
        "Пожалуйста, дождитесь завершения обработки предыдущего запроса."
    )
    await state.set_state(ProcessReqest.ignore)


@usr_msg_router.message(StateFilter(ProcessReqest.ignore))
async def ignore_while_processing(message: Message):
    logger.debug(f"Ignore state while handling user {message.from_user.id}'s request")


@usr_msg_router.message(~F.text)
async def process_non_text_message(message: Message):
    await message.answer(
        text="На данный момент бот не работает только с текстовыми запросами."
    )
