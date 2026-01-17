from aiogram.fsm.state import State, StatesGroup

class LogFoodForm(StatesGroup):
    ask_gramms = State()
