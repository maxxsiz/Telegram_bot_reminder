import telebot
from settings import token

bot = telebot.TeleBot(token)

def menu_markup():
    markup = InlineKeyboardMurkap()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Добавити напоминання", callback_data="add_remider"),
                InlineKeyboardButton("Редагувати напоминнання", callback_data="edit_remider"),
                InlineKeyboardButton("Показати статистику", callback_data="show_stat"),
                InlineKeyboardButton("Інше", callback_data="other"))

def add_remider_markup():
    markup = InlineKeyboardMurkap()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Добавити звичайне нагадування", callback_data="add_remider"),
                InlineKeyboardButton("Добавити нагадування з данними", callback_data="edit_remider"),
                InlineKeyboardButton("Добавити ", callback_data="show_stat"),
                InlineKeyboardButton("Інше", callback_data="other"))

def edit_remider_markup():
    markup = InlineKeyboardMurkap()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Змінити назву нагадування", callback_data="add_remider"),
                InlineKeyboardButton("Змінити частоту нагадування", callback_data="edit_remider"),
                InlineKeyboardButton("Змінити період перериву", callback_data="show_stat"),
                InlineKeyboardButton("Інше", callback_data="other"))

def show_stat_markup():
    markup = InlineKeyboardMurkap()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Добавити напоминання", callback_data="add_remider"),
                InlineKeyboardButton("Редагувати напоминнання", callback_data="edit_remider"),
                InlineKeyboardButton("Показати статистику", callback_data="show_stat"),
                InlineKeyboardButton("Інше", callback_data="other"))

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

bot.polling()