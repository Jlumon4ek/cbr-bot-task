import asyncio
from aiogram import Bot, Dispatcher
from handlers.command import register_command_handlers
from handlers.callback import RegisterQueryHandler
from utils.config import TOKEN
from utils.currency import fetch_currencies
import loguru 
import sys

loguru.logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def periodic_fetch():
    loguru.logger.info("Starting periodic fetch...")
    while True:
        await fetch_currencies()
        await asyncio.sleep(12 * 3600)

async def main():
    loguru.logger.info("Starting bot...")
    await register_command_handlers(dp, bot)
    await RegisterQueryHandler(dp, bot)

    loguru.logger.info("Starting periodic fetch task...")
    asyncio.create_task(periodic_fetch())

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
