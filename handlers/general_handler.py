from aiogram.dispatcher.webhook import SendMessage
from aiogram import types

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from misc import dp
import keyboards as kb

@dp.message_handler(commands=['start', 'help', 'menu'])
async def send_welcome(message: types.Message):
    if message.text == "/start" or message.text == "/help" :
        await message.reply( """Привіт я бот нагадувач, буду тобі нагадувати про щось що ти мусиш робити кожен день або декілька разів в день.
        Також я можу вести статистику, наприклад нагадувати тобі присідати а після записувати скільки ти зробив разів. Якщо зацікавив жми /menu""")
    elif message.text == "/menu":
        await message.reply("Виберіть, що Вас цікавить.",reply_markup=kb.menu_markup())



