from aiogram.dispatcher.webhook import SendMessage
from aiogram import types
from datetime import date, time
from aiogram.dispatcher.filters.state import State, StatesGroup
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from calculate_functions import calc_timezone, do_register
from misc import dp
import keyboards as kb
from database_fun import add_new_user, send_time_text

class TimezoneInfo(StatesGroup):
    current_user_time = State()

@dp.message_handler(commands=['start','menu'])
async def send_welcome(message: types.Message):
    if message.text == "/start":
        await message.reply( """Привіт я бот нагадувач, буду тобі нагадувати про щось що ти мусиш робити кожен день або декілька разів в день.
        Також я можу вести статистику, наприклад нагадувати тобі присідати а після записувати скільки ти зробив разів. Якщо зацікавив жми /menu""")
        if check_register:
            await message.reply("Якщо зацікавив жми /menu")
        else:
            await bot.send_message(message.from_user.id, "Але для початку потрібно вказати яка у вас година, нажміть на варіант ...")
            await bot.send_message(message.from_user.id, do_register())
            await TimezoneInfo.current_user_time.set()
    elif message.text == "/menu":
        await message.reply("Виберіть, що Вас цікавить.",reply_markup=kb.menu_markup())

@dp.message_handler(state=TimezoneInfo.current_user_time, content_types=types.ContentTypes.TEXT)
async def do_register(message: types.Message, state: FSMContext):
    if message.text not in send_time_text("list"):
        await message.reply("Будь ласка вибери годину зі списку")
        return
    await state.update_data(reminder_periodisity=message.text)
    async d = date.today()
    async time_zone = calc_timezone(message_text[1:3])
    async add_new_user(message.from_user.id, message.from_user.username, message.from_user.first_name, d.isoformat(), message.from_user.language_code, time_zone)
    async message.reply(f"Ваша часова зона {time_zone}. Жми /menu щоб продовжити.")
    await state.finish()
