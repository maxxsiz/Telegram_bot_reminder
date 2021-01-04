from aiogram.dispatcher.webhook import SendMessage
import keyboards as kb
from main import dp, bot
from aiogram import types


@dp.message_handler(commands=['start', 'help', 'menu'])
async def send_welcome(message: types.Message):
    if message.text == "/start" or message.text == "/help" :
        await message.reply( """Привіт я бот нагадувач, буду тобі нагадувати про щось що ти мусиш робити кожен день або декілька разів в день.
        Також я можу вести статистику, наприклад нагадувати тобі присідати а після записувати скільки ти зробив разів. Якщо зацікавив жми /menu""")
    elif message.text == "/menu":
        await bot.send_message(message.from_user.id, "Виберіть, що Вас цікавить.",reply_markup=kb.menu_markup())