import asyncio

from bot import dp, bot


async def main():
    await dp.start_polling(bot, skip_updates=False)


if __name__ == "__main__":
    print("Бот запущен...")
    asyncio.run(main())
