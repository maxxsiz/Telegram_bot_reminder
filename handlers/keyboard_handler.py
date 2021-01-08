from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.webhook import SendMessage
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import keyboards as kb
from misc import dp, bot


@dp.callback_query_handler(lambda c: c.data, state = "*")
async def process_all_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    if callback_query.data == "add_reminder":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id,"Виберіть, що Вас цікавить.", reply_markup=kb.add_reminder_markup())
    elif callback_query.data == "edit_reminder":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id,"Виберіть, що Вас цікавить.", reply_markup=kb.edit_reminder_markup())
    elif callback_query.data == "show_stat":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id, "Виберіть, що Вас цікавить.", reply_markup=kb.show_stat_markup())
    elif callback_query.data == "other":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id, "В розробці")
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