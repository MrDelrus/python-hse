from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from core.validation import log_intake
from states import LogFoodForm
from texts import log_intake as txt

router = Router(name="intake logger")


@router.message(Command("log_water"), StateFilter(None))
async def cmd_log_water(
    message: Message, state: FSMContext, command: CommandObject
) -> None:
    if command.args is None:
        await message.answer(text=txt.ASK_WATER_NO_ARGS)
        return

    msg = str(command.args).strip()
    try:
        consumed_water_ml = log_intake.validate_water(msg)
    except ValueError:
        await message.answer(txt.ASK_WATER_NO_ARGS)
        return

    data = await state.get_data()
    current_consumed_water_ml = data["current_water"]
    current_consumed_water_ml += consumed_water_ml

    await state.update_data(current_water=current_consumed_water_ml)

    left_to_consume_water_ml = data["water_goal"] - current_consumed_water_ml

    if left_to_consume_water_ml <= 0:
        await message.answer(text=txt.WATER_GOAL_REACHED)
        return

    answer_msg = txt.WATER_LEFT.format(left_to_consume_water_ml)
    await message.answer(answer_msg)


@router.message(Command("log_food"), StateFilter(None))
async def cmd_log_food_product_name(
    message: Message, state: FSMContext, command: CommandObject
) -> None:
    data = await state.get_data()
    if "food_client" not in data:
        await message.answer(txt.NO_API_KEY_FOUND)
        return

    if command.args is None:
        await message.answer(text=txt.ASK_FOOD_NO_ARGS)
        return

    msg = str(command.args).strip()
    try:
        product_name = log_intake.validate_product_name(msg)
    except ValueError:
        await message.answer(txt.FOOD_NOT_FOUND)
        return

    await state.set_state(LogFoodForm.ask_gramms)
    await state.update_data(last_product_name=product_name)
    await message.answer(txt.ASK_FOOD_GRAMMS)


@router.message(StateFilter(LogFoodForm.ask_gramms))
async def cmd_log_food_gramms(
    message: Message,
    state: FSMContext,
) -> None:
    msg = message.text.strip()
    eaten_g = log_intake.validate_product_g(msg)
    data = await state.get_data()

    client = data["food_client"]
    product_name = data["last_product_name"]
    try:
        consumed_calorie = client.get_calories(product_name, eaten_g)
        current_consumed_calorie = data["current_calorie"]
        current_consumed_calorie += consumed_calorie
        await state.update_data(current_calorie=current_consumed_calorie)
        answer_msg = txt.FOOD_CONSUMED.format(consumed_calorie)
        await message.answer(answer_msg)
    except Exception:
        await message.answer(txt.CLIENT_ERROR)

    await state.set_state(None)


@router.message(Command("log_workout"), StateFilter(None))
async def cmd_log_workout(
    message: Message, state: FSMContext, command: CommandObject
) -> None:
    if command.args is None:
        await message.answer(text=txt.ASK_WORKOUT_NO_ARGS)
        return

    msg = str(command.args).strip()
    try:
        activity_time = log_intake.validate_activity(msg)
    except ValueError:
        await message.answer(text=txt.ASK_WORKOUT_NO_ARGS)
        return

    burned_calorie = 200 * activity_time / 30
    data = await state.get_data()
    current_burned_calorie = data["burned_calorie"]
    current_burned_calorie += burned_calorie

    await state.update_data(burned_calorie=current_burned_calorie)
    await message.answer(txt.ANSWER_WORKOUT)
