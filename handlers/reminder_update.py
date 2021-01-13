from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from misc import dp, bot
from database_fun import reminder_edit, all_reminders, all_reminders_list, reminder_freeze, check_reminder_status, reminder_edit, single_reminder
import keyboards as kb

#reminder delete 

class ReminderDelete(StatesGroup):
    waiting_for_reminder_id = State()
    waiting_for_check = State()

@dp.callback_query_handler(lambda c: c.data == "delete_reminder", state = "*")
async def delete_reminder_step_1(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await bot.send_message(chat_id, "Вибери нагадування яке хочеш видалити")
    await bot.send_message(chat_id, all_reminders(chat_id,"all","withslash"))
    await ReminderDelete.waiting_for_reminder_id.set()

@dp.message_handler(state=ReminderDelete.waiting_for_reminder_id, content_types=types.ContentTypes.TEXT)
async def delete_reminder_step_2(message: types.Message, state: FSMContext):
    if message.text[1:] in all_reminders_list(message.from_user.id, "all") :
        await message.reply("Вибери номер зі списку")
        return
    await state.update_data(reminder_id=message.text[1:])
    await ReminderDelete.next()
    await message.answer(f"Ви дійсно хочете видалити нагадування {message.text}",reply_markup=kb.yes_no_markup())

@dp.message_handler(lambda c: c.data == "answer_yes" or c.data == "answer_no" , state=ReminderDelete.waiting_for_check)
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

class ReminderFreeze(StatesGroup):
    waiting_for_reminder_id = State()
    waiting_for_check = State()

@dp.callback_query_handler(lambda c: c.data == "freeze_reminder", state = "*")
async def freeze_reminder_step_1(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await bot.send_message(chat_id, all_reminders(chat_id,"all","withslash"))
    await ReminderFreeze.waiting_for_reminder_id.set()

@dp.message_handler(state=ReminderFreeze.waiting_for_reminder_id, content_types=types.ContentTypes.TEXT)
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
    await ReminderFreeze.next()

@dp.message_handler(lambda c: c.data == "answer_yes" or c.data == "answer_no" , state=ReminderFreeze.waiting_for_check)
async def freeze_reminder_step_3(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    user_data = await state.get_data()
    if callback_query.data == "answer_yes":
        reminder_freeze(user_data['reminder_id'], user_data['reminder_status'])
        await bot.send_message(callback_query.from_user.id, f"Нагадування {user_data['reminder_id']} успішно видалено.")
    elif callback_query.data == "answer_no":
        await bot.send_message(callback_query.from_user.id, "Видалення було відмінено")
    await state.finish()


#reminder edit

class ReminderEdit(StatesGroup):
    waiting_for_reminder_id = State()
    waiting_for_choose = State()
    answer_about_more = State()
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_periodisity = State()
    waiting_for_breaktime = State()

@dp.callback_query_handler(lambda c: c.data == "edit_reminder", state = "*") # first step send reminders_list
async def edit_reminder_step_1(callback_query: types.CallbackQuery):
    print('ok')
    chat_id = callback_query.from_user.id
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await bot.send_message(chat_id, all_reminders(chat_id,"all","withslash"))
    await ReminderEdit.waiting_for_reminder_id.set()

@dp.message_handler(state=ReminderEdit.waiting_for_reminder_id, content_types=types.ContentTypes.TEXT) # choose reminder, and send edit inlinebutton
async def edit_reminder_step_2(message: types.Message, state: FSMContext):
    if message.text[1:] in all_reminders_list(message.from_user.id, "all") :
        await message.reply("Вибери номер зі списку")
        return
    await state.update_data(reminder_id=message.text[1:])
    datas = single_reminder(message.text[1:])
    await bot.send_message(message.from_user.id, f"""Що ви хочете поміняти в нагадуванні?\n
                                                    Ваше теперішнє нагадування:\n
                                                    Назва: {datas[0]}\n
                                                    Опис: {datas[1]}\n
                                                    Періодичність:{datas[2]}\n
                                                    Перерва:{datas[3]}\n""",reply_markup=kb.edit_reminder_markup())
    await ReminderEdit.waiting_for_choose.set()

@dp.message_handler(lambda c: c.data in ["edit_name","edit_description","edit_periodicity","edit_break_time"], state=ReminderEdit.waiting_for_choose) # 
async def edit_reminder_step_3(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    if callback_query.data == "edit_name":
        await bot.send_message(callback_query.from_user.id, "Введіть нову назву нагадування")
        await ReminderEdit.waiting_for_name.set()
    elif callback_query.data == "edit_description":
        await bot.send_message(callback_query.from_user.id, "Введіть новий опис нагадування")
        await ReminderEdit.waiting_for_description.set()
    elif callback_query.data == "edit_periodicity":
        await bot.send_message(callback_query.from_user.id, "Введіть нову періодичність нагадування")
        await ReminderEdit.waiting_for_periodisity.set()
    elif callback_query.data == "edit_break_time":
        await bot.send_message(callback_query.from_user.id, "Введіть новий період перерви нагадування")
        await ReminderEdit.waiting_for_breaktime.set()


@dp.message_handler(state=ReminderEdit.waiting_for_name, content_types=types.ContentTypes.TEXT) # choose reminder, and send edit inlinebutton
async def edit_reminder_name(message: types.Message, state: FSMContext):
    if False:
        await message.reply("Некоректний формат")
        return
    await state.update_data(reminder_name=message.text)
    await ReminderEdit.answer_about_more.set()

@dp.message_handler(state=ReminderEdit.waiting_for_description, content_types=types.ContentTypes.TEXT) # choose reminder, and send edit inlinebutton
async def edit_reminder_description(message: types.Message, state: FSMContext):
    if False:
        await message.reply("Некоректний формат")
        return
    await state.update_data(reminder_description=message.text)
    await ReminderEdit.answer_about_more.set()

@dp.message_handler(state=ReminderEdit.waiting_for_periodisity, content_types=types.ContentTypes.TEXT) # choose reminder, and send edit inlinebutton
async def edit_reminder_periodisity(message: types.Message, state: FSMContext):
    if False:
        await message.reply("Некоректний формат")
        return
    await state.update_data(periodisity=message.text)
    await ReminderEdit.answer_about_more.set()

@dp.message_handler(state=ReminderEdit.waiting_for_breaktime, content_types=types.ContentTypes.TEXT) # choose reminder, and send edit inlinebutton
async def edit_reminder_breaktime(message: types.Message, state: FSMContext):
    if False:
        await message.reply("Некоректний формат")
        return
    await state.update_data(break_time=message.text)
    await ReminderEdit.answer_about_more.set()
    await bot.send_message(message.from_user.id,"Бажаєте ще щось змніити?", reply_markup=kb.yes_no_markup())

@dp.message_handler(lambda c: c.data == "answer_yes" or c.data == "answer_no" , state=ReminderEdit.answer_about_more)
async def edit_reminder_askmore(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    if callback_query.data == "answer_yes":
        await ReminderEdit.waiting_for_choose.set()
        await bot.send_message(callback_query.from_user.id, "Що ви ще хочете поміняти в нагадуванні?",reply_markup=kb.edit_reminder_markup())
    elif callback_query.data == "answer_no":
        reminders_data = await state.get_data()
        print(reminders_data)
        await state.finish()
    

