from aiogram.fsm.state import State, StatesGroup


class ProcessReqest(StatesGroup):
    waiting = State()
    ignore = State()
