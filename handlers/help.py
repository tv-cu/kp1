from aiogram import types
from aiogram.filters import Command

from bot import dp


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Доступные команды:\n"
        "/start — начать работу с ботом\n"
        "/help — вывести это сообщение\n"
        "/weather — получить прогноз погоды по маршруту\n\n"
        "Использование /weather:\n"
        "1. Введите начальную точку.\n"
        "2. Введите конечную точку.\n"
        "3. По желанию добавьте промежуточные точки.\n"
        "4. Выберите временной интервал (до 5 дней).\n"
        "5. Получите прогноз погоды!"
    )
