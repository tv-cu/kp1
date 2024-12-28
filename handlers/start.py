from aiogram import types
from aiogram.filters import CommandStart

from bot import dp


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот прогноза погоды по маршруту.\n"
        "Отправь /help чтобы узнать о моих возможностях."
    )
