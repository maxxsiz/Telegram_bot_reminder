from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from misc import dp, bot
from database_fun import reminder_edit, all_reminders, all_reminders_list
import keyboards as kb

class ReminderId(StatesGroup):
    waiting_for_reminder_id = State()
    waiting_for_check = State()

@dp.callback_query_handler(lambda c: c.data == "delete_reminder", state = "*")
async def delete_reminder(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await bot.send_message(chat_id, all_reminders(chat_id,"all","withslash"))
    await ReminderId.waiting_for_reminder_id.set()

@dp.message_handler(state=ReminderId.waiting_for_reminder_id, content_types=types.ContentTypes.TEXT)
async def add_reminder_step_3(message: types.Message, state: FSMContext):
    if message.text in all_reminders_list(message.from_user.id, "all") :
        await message.reply("Вибери номер зі списку")
        return
    await state.update_data(reminder_id=message.text)
    await ReminderInfo.next()  # для простых шагов можно не указывать название состояния, обходясь next()
    await message.answer(f"Ви дійсно хочете видалити нагадування {message.text}",reply_markup=kb.add_reminder_markup())

@dp.message_handler(state=ReminderId.waiting_for_reminder_break_time, content_types=types.ContentTypes.TEXT)
async def add_reminder_step_5(message: types.Message, state: FSMContext):
    if len(message.text.lower()) > 20:
        await message.reply("Нажаль ви не коректно ввели, повторіть знову")
        return
    user_data = await state.get_data()
    reminder_count = check_reminder_count(message.from_user.id)
    if reminder_count == False:
        await message.reply("В вас максимальна кількість нагадувань вже")
    else:
        add_new_reminder(message.from_user.id, str(message.from_user.id) + str(reminder_count), user_data['reminder_name'], user_data['reminder_description'], "simple", user_data['reminder_periodisity'], message.text, True)
        await message.answer(f"Ви створили просте нагадування: {user_data['reminder_name']}.\n"
                         f"Опис: {user_data['reminder_description']}\n"
                         f"Повторення кожних {user_data['reminder_periodisity']} \n"
                         f"Перерва: {message.text}\n")
        await state.finish()