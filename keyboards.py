from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def menu_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Добавити напоминання", callback_data="add_reminder"),
                InlineKeyboardButton("Керувати нагадуваннями", callback_data="controll_reminder"),
                InlineKeyboardButton("Показати статистику", callback_data="show_stat"),
                InlineKeyboardButton("Показати мої нагадування", callback_data="show_reminders"),
                InlineKeyboardButton("Інше", callback_data="other"))
    return markup

def controll_reminder_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Видалити нагадування", callback_data="delete_reminder"),
                InlineKeyboardButton("Призупинити нагадування", callback_data="freeze_reminder"),
                InlineKeyboardButton("Редагувати нагадування", callback_data="edit_reminder"))
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
                InlineKeyboardButton("Змінити назву нагадування", callback_data="edit_description"),
                InlineKeyboardButton("Змінити частоту нагадування", callback_data="edit_periodicity"),
                InlineKeyboardButton("Змінити період перериву", callback_data="edit_break_time"))
    return markup

def show_reminders_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Показати всі нагадування", callback_data="show_all_reminders"),
                InlineKeyboardButton("Показати нагадування прості", callback_data="show_simple_reminders"),
                InlineKeyboardButton("Показати продвінуті нагадування", callback_data="show_adv_reminders"))
    return markup

def show_stat_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Графік за певний період", callback_data="graf_some_period"),
                InlineKeyboardButton("Статистика за весь час", callback_data="stat_all_time"),
                InlineKeyboardButton("Аналіз за весь час", callback_data="analyze_stat"))
    return markup

def yes_no_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Так", callback_data="answer_yes"),
                InlineKeyboardButton("Ні", callback_data="answer_no"))
    return markup