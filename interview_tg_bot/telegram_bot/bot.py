import logging

from interview_tg_bot.settings import TOKEN, BOT_USERNAME

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .handlers import register_handlers


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Configure logging
logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print('Bot is online.')


def run_bot():
    # Initialize bot and dispatcher
    executor.start_polling(register_handlers(dp), skip_updates=False, on_startup=on_startup)
