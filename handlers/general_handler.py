from aiogram.dispatcher.webhook import SendMessage
from aiogram import types
from datetime import date
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from misc import dp
import keyboards as kb
from database_fun import add_new_user
@dp.message_handler(commands=['start','menu'])
async def send_welcome(message: types.Message):
    if message.text == "/start":
        await message.reply( """Привіт я бот нагадувач, буду тобі нагадувати про щось що ти мусиш робити кожен день або декілька разів в день.
        Також я можу вести статистику, наприклад нагадувати тобі присідати а після записувати скільки ти зробив разів. Якщо зацікавив жми /menu""")
        d = date.today()
        print(message.from_user.id)
        print(message.from_user.full_name)
        print(d.isoformat())
        print(message.from_user.language_code)
        print(message.from_user.username)
        add_new_user(message.from_user.id, message.from_user.username, message.from_user.first_name, d.isoformat(), message.from_user.language_code, timezone)
    elif message.text == "/menu":
        await message.reply("Виберіть, що Вас цікавить.",reply_markup=kb.menu_markup())



