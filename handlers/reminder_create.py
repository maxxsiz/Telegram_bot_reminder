from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from main import dp, bot

class ReminderInfo(StatesGroup):
    waiting_for_remider_name = State()
    waiting_for_reminder_description = State()
    waiting_for_reminder_periodisity = State()
    waiting_for_reminder_break_time = State()

def check_correct_time(message):
    return True

@dp.callback_query_handler(lambda c: c.data == "add_reminder_simple", state = "*")
async def add_remider_callback(callback_query: types.CallbackQuery):
    print('ok')
    chat_id = callback_query.from_user.id
    await bot.send_message(chat_id, "Впишіть короткий опис нагадування яке буде в вас висвітлюватися, наприклад: 'Відпочинь від комп'ютера'")
    await ReminderInfo.waiting_for_remider_name.set()

@dp.message_handler(state=ReminderInfo.waiting_for_remider_name, content_types=types.ContentTypes.TEXT)
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

@dp.message_handler(state=ReminderInfo.waiting_for_reminder_periodisity, content_types=types.ContentTypes.TEXT)
async def add_reminder_step_5(message: types.Message, state: FSMContext):
    if check_correct_time(message.text.lower()) == False:
        await message.reply("Нажаль ви не коректно ввели, повторіть знову")
        return
    user_data = await state.get_data()
    await message.answer(f"Нагадування: {user_data['reminder_name']}.\n"
                         f"{user_data['reminder_description']}\n"
                         f"Повторення кожних {user_data['reminder_periodisity']} \n"
                         f"Перерва: {message.text}\n")
    await state.finish()
