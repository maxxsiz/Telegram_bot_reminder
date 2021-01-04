from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def menu_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Добавити напоминання", callback_data="add_reminder"),
                InlineKeyboardButton("Редагувати напоминнання", callback_data="edit_reminder"),
                InlineKeyboardButton("Показати статистику", callback_data="show_stat"),
                InlineKeyboardButton("Інше", callback_data="other"))
    return markup

def add_reminder_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Добавити повторююче нагадування", callback_data="add_reminder_simple"),
                InlineKeyboardButton("Добавити повторююче нагадування з данними", callback_data="add_reminder_with_bd"))
    return markup

def edit_reminder_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Змінити назву нагадування", callback_data="edit_name"),
                InlineKeyboardButton("Змінити частоту нагадування", callback_data="edit_periodicity"),
                InlineKeyboardButton("Змінити період перериву", callback_data="edit_break_time"))
    return markup

def show_stat_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Графік за певний період", callback_data="graf_some_period"),
                InlineKeyboardButton("Статистика за весь час", callback_data="stat_all_time"),
                InlineKeyboardButton("Аналіз за весь час", callback_data="analyze_stat"))
    return markup