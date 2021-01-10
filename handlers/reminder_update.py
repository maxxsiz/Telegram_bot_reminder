from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from misc import dp, bot
from database_fun import reminder_edit, all_reminders, all_reminders_list, reminder_freeze, check_reminder_status
import keyboards as kb

#reminder delete 

class ReminderId(StatesGroup):
    waiting_for_reminder_id = State()
    waiting_for_check = State()

@dp.callback_query_handler(lambda c: c.data == "delete_reminder", state = "*")
async def delete_reminder_step_1(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await bot.send_message(chat_id, "Вибери нагадування яке хочеш видалити")
    await bot.send_message(chat_id, all_reminders(chat_id,"all","withslash"))
    await ReminderId.waiting_for_reminder_id.set()

@dp.message_handler(state=ReminderId.waiting_for_reminder_id, content_types=types.ContentTypes.TEXT)
async def delete_reminder_step_2(message: types.Message, state: FSMContext):
    if message.text[1:] in all_reminders_list(message.from_user.id, "all") :
        await message.reply("Вибери номер зі списку")
        return
    await state.update_data(reminder_id=message.text[1:])
    await ReminderId.next()
    await message.answer(f"Ви дійсно хочете видалити нагадування {message.text}",reply_markup=kb.yes_no_markup())

@dp.message_handler(lambda c: c.data == "answer_yes" or c.data == "answer_no" , state=ReminderId.waiting_for_check)
async def delete_reminder_step_3(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    user_data = await state.get_data()
    if callback_query.data == "answer_yes":
        reminder_edit('', user_data['reminder_id'], '', '', '', '', '', '')
        await bot.send_message(callback_query.from_user.id, f"Нагадування {user_data['reminder_id']} успішно видалено.")
    elif callback_query.data == "answer_no":
        await bot.send_message(callback_query.from_user.id, "Видалення було відмінено")
    await state.finish()

#freeze reminder
@dp.callback_query_handler(lambda c: c.data == "freeze_reminder", state = "*")
async def freeze_reminder_step_1(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await bot.send_message(chat_id, all_reminders(chat_id,"all","withslash"))
    await ReminderId.waiting_for_reminder_id.set()

@dp.message_handler(state=ReminderId.waiting_for_reminder_id, content_types=types.ContentTypes.TEXT)
async def freeze_reminder_step_2(message: types.Message, state: FSMContext):
    if message.text[1:] in all_reminders_list(message.from_user.id, "all") :
        await message.reply("Вибери номер зі списку")
        return
    rm_status = check_reminder_status(message.text[1:])
    await state.update_data(reminder_id=message.text[1:], reminder_status = lambda rm_status: 0 if rm_status == 1 else 0)
    if rm_status:
        await message.answer(f"Ви дійсно хочете дезактивувати нагадування {message.text}",reply_markup=kb.yes_no_markup())
    else: 
        await message.answer(f"Ви дійсно хочете активувати нагадування {message.text}",reply_markup=kb.yes_no_markup())
    await ReminderId.next()

@dp.message_handler(lambda c: c.data == "answer_yes" or c.data == "answer_no" , state=ReminderId.waiting_for_check)
async def freeze_reminder_step_3(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    user_data = await state.get_data()
    if callback_query.data == "answer_yes":
        reminder_freeze(user_data['reminder_id'], user_data['reminder_status'])
        await bot.send_message(callback_query.from_user.id, f"Нагадування {user_data['reminder_id']} успішно видалено.")
    elif callback_query.data == "answer_no":
        await bot.send_message(callback_query.from_user.id, "Видалення було відмінено")
    await state.finish()