from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from misc import dp, bot
from database_fun import add_new_reminder, check_reminder_count

class ReminderInfo(StatesGroup):
    waiting_for_reminder_name = State()
    waiting_for_reminder_description = State()
    waiting_for_reminder_periodisity = State()
    waiting_for_reminder_break_time = State()
 
@dp.callback_query_handler(lambda c: c.data == "add_reminder_simple", state = "*")
async def add_reminder_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await bot.send_message(chat_id, "Впишіть короткий опис нагадування яке буде в вас висвітлюватися, наприклад: 'Відпочинь від комп'ютера'")
    await ReminderInfo.waiting_for_reminder_name.set()

@dp.message_handler(state=ReminderInfo.waiting_for_reminder_name, content_types=types.ContentTypes.TEXT)
async def add_reminder_step_2(message: types.Message, state: FSMContext):
    if len(message.text.lower()) > 20 :
        await message.reply("Максимальна довжина короткого опису 20 знаків")
        return
    await state.update_data(reminder_name=message.text)
    await ReminderInfo.next()  # для простых шагов можно не указывать название состояния, обходясь next()
    await message.answer("Тепер місце на більш ширший опис, можете пропустити це відправивши будь яке коротке слово")

@dp.message_handler(state=ReminderInfo.waiting_for_reminder_description, content_types=types.ContentTypes.TEXT)
async def add_reminder_step_3(message: types.Message, state: FSMContext):
    if len(message.text.lower()) > 200 :
        await message.reply("Максимальна довжина великого опису 200 знаків")
        return
    await state.update_data(reminder_description=message.text)
    await ReminderInfo.next()  # для простых шагов можно не указывать название состояния, обходясь next()
    await message.answer("Впишіть, як часто буде повторюватись нагадування наприклад: '30m' буде значити кожних 30 хвилин, '2h' кожні дві години")

@dp.message_handler(state=ReminderInfo.waiting_for_reminder_periodisity, content_types=types.ContentTypes.TEXT)
async def add_reminder_step_4(message: types.Message, state: FSMContext):
    if message.text.lower()[-1] not in ['h','m']:
        await message.reply("Нажаль ви не коректно ввели, повторіть знову")
        return
    await state.update_data(reminder_periodisity=message.text)
    await ReminderInfo.next()  # для простых шагов можно не указывать название состояния, обходясь next()
    await message.answer("Впишіть, коли вас не турбувати цим нагадуванням, прошу вписувати в форматі 24годиному наприклад: '23:00 - 8:00'")

@dp.message_handler(state=ReminderInfo.waiting_for_reminder_break_time, content_types=types.ContentTypes.TEXT)
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

class ReminderDbInfo(StatesGroup):
    waiting_for_reminder_name = State()
    waiting_for_reminder_description = State()
    waiting_for_reminder_periodisity = State()
    waiting_for_reminder_break_time = State()
    waiting_for_reminder_db_name = State()

@dp.callback_query_handler(lambda c: c.data == "add_reminder_with_bd", state = "*")
async def add_reminderdb_callback(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    chat_id = callback_query.from_user.id
    await bot.send_message(chat_id, "Впишіть короткий опис нагадування яке буде в вас висвітлюватися, наприклад: 'Відпочинь від комп'ютера'")
    await ReminderDbInfo.waiting_for_reminder_name.set()

@dp.message_handler(state=ReminderDbInfo.waiting_for_reminder_name, content_types=types.ContentTypes.TEXT)
async def add_reminderdb_step_2(message: types.Message, state: FSMContext):
    if len(message.text.lower()) > 20 :
        await message.reply("Максимальна довжина короткого опису 20 знаків")
        return
    await state.update_data(reminder_name=message.text)
    await ReminderDbInfo.next()  # для простых шагов можно не указывать название состояния, обходясь next()
    await message.answer("Тепер місце на більш ширший опис, можете пропустити це відправивши будь яке коротке слово")

@dp.message_handler(state=ReminderDbInfo.waiting_for_reminder_description, content_types=types.ContentTypes.TEXT)
async def add_reminderdb_step_3(message: types.Message, state: FSMContext):
    if len(message.text.lower()) > 200 :
        await message.reply("Максимальна довжина великого опису 200 знаків")
        return
    await state.update_data(reminder_description=message.text)
    await ReminderDbInfo.next()  # для простых шагов можно не указывать название состояния, обходясь next()
    await message.answer("Впишіть, як часто буде повторюватись нагадування наприклад: '30m' буде значити кожних 30 хвилин, '2h' кожні дві години")

@dp.message_handler(state=ReminderDbInfo.waiting_for_reminder_periodisity, content_types=types.ContentTypes.TEXT)
async def add_reminderdb_step_4(message: types.Message, state: FSMContext):
    if message.text.lower()[-1] not in ['h','m']:
        await message.reply("Нажаль ви не коректно ввели, повторіть знову")
        return
    await state.update_data(reminder_periodisity=message.text)
    await ReminderDbInfo.next()  # для простых шагов можно не указывать название состояния, обходясь next()
    await message.answer("Впишіть, коли вас не турбувати цим нагадуванням, прошу вписувати в форматі 24годиному наприклад: '23:00 - 8:00'")

@dp.message_handler(state=ReminderDbInfo.waiting_for_reminder_break_time, content_types=types.ContentTypes.TEXT)
async def add_reminderdb_step_5(message: types.Message, state: FSMContext):
    if len(message.text.lower()) > 200 :
        await message.reply("Ви ввели некоректний період")
        return
    await state.update_data(reminder_break_time=message.text)
    await ReminderDbInfo.next()  # для простых шагов можно не указывать название состояния, обходясь next()
    await message.answer("Впишіть, що ви будете нотувати, наприклад: кількість віджиманнь, вивчених слів, часу потраченого на навчання")

@dp.message_handler(state=ReminderDbInfo.waiting_for_reminder_db_name, content_types=types.ContentTypes.TEXT)
async def add_reminderdb_step_6(message: types.Message, state: FSMContext):
    if len(message.text.lower()) > 20:
        await message.reply("Не довше 20 знаків")
        return
    user_data = await state.get_data()
    reminder_count = check_reminder_count(message.from_user.id)
    if reminder_count == False:
        await message.reply("В вас максимальна кількість нагадувань вже")
    else:
        add_new_reminder(message.from_user.id, str(message.from_user.id) + str(reminder_count), user_data['reminder_name'], user_data['reminder_description'], "advansed", user_data['reminder_periodisity'], message.text, True)
        await message.answer(f"Ви створили продвінуте нагадування:{user_data['reminder_name']}.\n"
                         f"Опис: {user_data['reminder_description']}\n"
                         f"Повторення кожних:{user_data['reminder_periodisity']}\n"
                         f"Пауза{user_data['reminder_break_time']}\n"
                         f"Рахувати ми будемо: {message.text}")
        await state.finish()