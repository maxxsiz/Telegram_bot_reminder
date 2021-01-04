import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from settings import TOKEN
import keyboards as kb

API_TOKEN = TOKEN
"""
# webhook settings
WEBHOOK_HOST = 'https://your.domain'
WEBHOOK_PATH = '/path/to/api'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 3001
"""
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
    
@dp.message_handler(commands=['start', 'help', 'menu'])
async def send_welcome(message: types.Message):
    if message.text == "/start" or message.text == "/help" :
        await message.reply( """Привіт я бот нагадувач, буду тобі нагадувати про щось що ти мусиш робити кожен день або декілька разів в день.
        Також я можу вести статистику, наприклад нагадувати тобі присідати а після записувати скільки ти зробив разів. Якщо зацікавив жми /menu""")
    elif message.text == "/menu":
        await bot.send_message(message.from_user.id, "Виберіть, що Вас цікавить.",reply_markup=kb.menu_markup())

@dp.message_handler()
async def log_fun(message: types.Message):
    return print(message.text) 

@dp.callback_query_handler(lambda c: c.data)
async def process_all_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    if callback_query.data == "add_remider":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id,"Виберіть, що Вас цікавить.", reply_markup=kb.add_remider_markup())
    elif callback_query.data == "edit_remider":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id,"Виберіть, що Вас цікавить.", reply_markup=kb.edit_remider_markup())
    elif callback_query.data == "show_stat":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id, "Виберіть, що Вас цікавить.", reply_markup=kb.show_stat_markup())
    elif callback_query.data == "other":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id, "В розробці")
    #add_remider
    elif callback_query.data == "add_remider":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id, "Виберіть, що Вас цікавить.")
    elif callback_query.data == "add_remider_with_bd":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id,"Виберіть, що Вас цікавить.") 
    #edit_remider
    elif callback_query.data == "edit_name":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(callback_query.data.message.chat.id, "Введіть нову назву нагадування ( максимальна довжина 20 знаків ) ")
    elif callback_query.data == "edit_periodicity":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(callback_query.data.id, "Введіть час повтороно нагадування /n в годинах: 3h або ж в хвилинах 30m")
    elif callback_query.data == "edit_break_time":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id, "Введіть період в 24 годинному форматі /n  наприклад: /21:00-6:00 ")
    #show_stat
    elif callback_query.data == "graf_some_period":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id, "В розробці")
    elif callback_query.data == "stat_all_time":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id, "В розробці")
    elif callback_query.data == "analyze_stat":
        await bot.send_message(chat_id, "В розробці")

if __name__ == '__main__':
    executor.start_polling(dp)

"""if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )"""
    