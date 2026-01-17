from aiogram.fsm.state import State, StatesGroup

class ProfileForm(StatesGroup):
    ask_weight_kg: State = State()
    ask_height_cm: State = State()
    ask_age: State = State()
    ask_daily_exercise_time_m: State = State()
    ask_city: State = State()
    ask_owm_api_key: State = State()
    ask_calories_goal: State = State()
    ask_food_api_key: State = State()
