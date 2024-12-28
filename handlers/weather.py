from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot import dp
from services.weather_service import get_weather_forecast
from utils.exceptions import WeatherServiceError


class WeatherForm(StatesGroup):
    start_point = State()
    end_point = State()
    intermediate_points = State()
    interval = State()


@dp.message(Command("weather"))
async def cmd_weather(message: types.Message, state: FSMContext):
    await message.answer("Введите начальную точку маршрута (город, адрес и т.д.):")
    await state.set_state(WeatherForm.start_point)


@dp.message(WeatherForm.start_point)
async def process_start_point(message: types.Message, state: FSMContext):
    start = message.text.strip()
    if not start:
        await message.answer("Пожалуйста, введите корректную начальную точку.")
        return
    await state.update_data(start_point=start)
    await message.answer("Введите конечную точку маршрута:")
    await state.set_state(WeatherForm.end_point)


@dp.message(WeatherForm.end_point)
async def process_end_point(message: types.Message, state: FSMContext):
    end = message.text.strip()
    if not end:
        await message.answer("Пожалуйста, введите корректную конечную точку.")
        return
    await state.update_data(end_point=end)
    await message.answer(
        "Введите промежуточные точки маршрута через запятую или отправьте \"-\" если их нет:"
    )
    await state.set_state(WeatherForm.intermediate_points)


@dp.message(WeatherForm.intermediate_points)
async def process_intermediate_points(message: types.Message, state: FSMContext):
    text = message.text.strip()
    if text == "-":
        points = []
    else:
        points = [p.strip() for p in text.split(",") if p.strip()]
    await state.update_data(intermediate_points=points)
    await message.answer("На сколько дней вперёд показать прогноз? Выберите:",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text=f"{i}", callback_data=f"interval_{i}") for i in
                              range(1, 6)]
                         ]))
    await state.set_state(WeatherForm.interval)


@dp.callback_query(lambda c: c.data.startswith("interval_"), WeatherForm.interval)
async def process_interval(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    interval_str = callback_query.data.split("_")[1]
    try:
        interval = int(interval_str)
        if interval < 1 or interval > 5:
            raise ValueError("Число дней должно быть от 1 до 5.")
    except ValueError:
        await callback_query.message.answer("Ошибка при выборе интервала. Повторите запрос.")
        return

    await state.update_data(interval=interval)
    data = await state.get_data()
    await state.clear()

    start = data["start_point"]
    end = data["end_point"]
    inter = data["intermediate_points"]
    interval_days = data["interval"]

    try:
        forecast = get_weather_forecast(start, end, inter, interval_days)
    except WeatherServiceError as e:
        await callback_query.message.answer(f"Произошла ошибка при получении данных о погоде: {e}")
        return
    except Exception as ex:
        await callback_query.message.answer(f"Непредвиденная ошибка: {ex}")
        return

    message_text = "Прогноз погоды по маршруту:\n\n"
    for location_data in forecast:
        message_text += f"<b>{location_data['point']}</b>\n"
        for day_data in location_data["days"]:
            message_text += (
                f"Дата: {day_data['date']}\n"
                f"Минимум: {day_data['temp_min']} °C\n"
                f"Максимум: {day_data['temp_max']} °C\n"
                f"Вероятность осадков: {day_data['precip']}%\n\n"
            )
        message_text += "\n"

    await callback_query.message.answer(message_text.strip())
