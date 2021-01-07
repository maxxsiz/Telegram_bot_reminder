import logging
from aiogram import Bot, Dispatcher
from settings import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)



"""
import logging
from aiogram import Bot, types
from settings import TOKEN
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import handlers

API_TOKEN = TOKEN

# webhook settings
WEBHOOK_HOST = 'https://your.domain'
WEBHOOK_PATH = '/path/to/api'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 3001

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())



if __name__ == '__main__':
    executor.start_polling(dp)

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
    """