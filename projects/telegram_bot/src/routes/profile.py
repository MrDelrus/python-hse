from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from core import compute_target_calorie, compute_target_water_ml
from core.validation import profile
from states import ProfileForm
from texts import profile as txt

router = Router(name="profile setter")


@router.message(Command("set_profile"))
async def cmd_set_profile_entry(message: Message, state: FSMContext) -> None:
    await message.answer(text=txt.ASK_WEIGHT)
    await state.set_state(ProfileForm.ask_weight_kg)


# Weight
@router.message(ProfileForm.ask_weight_kg)
async def cmd_set_profile_weight(message: Message, state: FSMContext) -> None:
    msg = message.text.strip()
    try:
        weight_kg = profile.validate_weight(msg)
    except ValueError:
        await message.answer(text=txt.VALIDATION_ERROR)
        return
    await state.update_data(weight=weight_kg)
    await state.set_state(ProfileForm.ask_height_cm)
    await message.answer(text=txt.ASK_HEIGHT)


# Height
@router.message(ProfileForm.ask_height_cm)
async def cmd_set_profile_height(message: Message, state: FSMContext) -> None:
    msg = message.text.strip()
    try:
        height_cm = profile.validate_height(msg)
    except ValueError:
        await message.answer(text=txt.VALIDATION_ERROR)
        return
    await state.update_data(height=height_cm)
    await state.set_state(ProfileForm.ask_age)
    await message.answer(text=txt.ASK_AGE)


# Age
@router.message(ProfileForm.ask_age)
async def cmd_set_profile_age(message: Message, state: FSMContext) -> None:
    msg = message.text.strip()
    try:
        age = profile.validate_age(msg)
    except ValueError:
        await message.answer(text=txt.VALIDATION_ERROR)
        return
    await state.update_data(age=age)
    await state.set_state(ProfileForm.ask_daily_exercise_time_m)
    await message.answer(text=txt.ASK_DAILY_EXERCISE_TIME)


# Daily exercise time
@router.message(ProfileForm.ask_daily_exercise_time_m)
async def cmd_set_profile_daily_exercise_time(
    message: Message, state: FSMContext
) -> None:
    msg = message.text.strip()
    try:
        daily_exercise_time_m = profile.validate_daily_exercise_time(msg)
    except ValueError:
        await message.answer(text=txt.VALIDATION_ERROR)
        return
    await state.update_data(daily_exercise_time=daily_exercise_time_m)
    await state.set_state(ProfileForm.ask_city)
    await message.answer(text=txt.ASK_CITY)


# City
@router.message(ProfileForm.ask_city)
async def cmd_set_profile_city(message: Message, state: FSMContext) -> None:
    msg = message.text.lower().strip()
    if msg != "-":
        try:
            city = profile.validate_city(msg)
        except ValueError:
            await message.answer(text=txt.VALIDATION_ERROR)
            return
        await state.update_data(city=city)
        await state.set_state(ProfileForm.ask_owm_api_key)
        await message.answer(text=txt.ASK_OWM_API_KEY)
        return

    await state.update_data(temperature=None)
    await state.set_state(ProfileForm.ask_calories_goal)
    await message.answer(text=txt.ASK_CALORIES_GOAL)


# OWM Api key
@router.message(ProfileForm.ask_owm_api_key)
async def cmd_set_profile_owm_api_key(message: Message, state: FSMContext) -> None:
    msg = message.text.lower().strip()
    if msg != "-":
        try:
            client = profile.create_async_weather_client(msg)
            data = await state.get_data()
            city = data["city"]
            temperature = await client.get_temperature(city)
        except Exception:
            await message.answer(text=txt.OWM_FAILURE)
            return
        await state.update_data(temperature=temperature)

    await state.update_data(temperature=None)
    await state.set_state(ProfileForm.ask_calories_goal)
    await message.answer(text=txt.ASK_CALORIES_GOAL)


# Calories goal
@router.message(ProfileForm.ask_calories_goal)
async def cmd_set_profile_calories_goal(message: Message, state: FSMContext) -> None:
    msg = message.text.strip()
    data = await state.get_data()
    if msg != "-":
        try:
            calories_goal = profile.validate_calories_goal(msg)
        except ValueError:
            await message.answer(text=txt.VALIDATION_ERROR)
            return
    else:
        calories_goal = compute_target_calorie(
            data["weight"],
            data["height"],
            data["age"],
            data["daily_exercise_time"],
        )

    water_goal = compute_target_water_ml(
        data["weight"], data["daily_exercise_time"], data["temperature"]
    )

    await state.update_data(calorie_goal=calories_goal, water_goal=water_goal)
    await state.set_state(ProfileForm.ask_food_api_key)
    await message.answer(text=txt.ASK_FOOD_API_KEY)


# Food client
@router.message(ProfileForm.ask_food_api_key)
async def cmd_set_profile_food_api_key(message: Message, state: FSMContext) -> None:
    msg = message.text.strip()
    if msg != "-":
        try:
            client = profile.create_async_food_client(msg)
            await state.update_data(food_client=client)
        except Exception:
            await message.answer(text=txt.VALIDATION_ERROR)

    await state.set_state(None)
    await message.answer(text=txt.END)
