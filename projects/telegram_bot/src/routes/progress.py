from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from texts import progress as txt

router = Router(name="progress checker")


@router.message(Command("check_progress"), StateFilter(None))
async def cmd_check_progress(
    message: Message,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    consumed_water = data["current_water"]
    goal_water = data["water_goal"]

    consumed_calorie = data["current_calorie"]
    goal_calorie = data["calorie_goal"]

    burned_calorie = data["burned_calorie"]

    answer_msg = txt.PROGRESS.format(
        consumed_water,
        goal_water,
        goal_water - consumed_water,
        consumed_calorie,
        goal_calorie,
        goal_calorie - consumed_calorie,
        burned_calorie,
        consumed_calorie - burned_calorie,
    )
    await message.answer(answer_msg)
