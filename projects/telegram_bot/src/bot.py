import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from config import settings
from middlewares import LoggingMiddleware
from routes import router_log_intake, router_profile, router_progress
from texts import general as txt

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.bot_token.get_secret_value())
dp = Dispatcher()
dp.message.middleware(LoggingMiddleware())
dp.include_router(router_profile)
dp.include_router(router_log_intake)
dp.include_router(router_progress)


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await state.set_state(None)
    await message.answer(txt.WELCOME)
    await state.update_data(
        burned_calorie=0,
        current_calorie=0,
        current_water=0,
        water_goal=0,
        calorie_goal=0,
    )


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
