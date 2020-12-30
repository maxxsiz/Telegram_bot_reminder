import telebot
from settings import token
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(token)

def menu_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Добавити напоминання", callback_data="add_remider"),
                InlineKeyboardButton("Редагувати напоминнання", callback_data="edit_remider"),
                InlineKeyboardButton("Показати статистику", callback_data="show_stat"),
                InlineKeyboardButton("Інше", callback_data="other"))
    return markup

def add_remider_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Добавити повторююче нагадування", callback_data="add_remider"),
                InlineKeyboardButton("Добавити повторююче нагадування з данними", callback_data="add_remider_with_bd"))
    return markup

def edit_remider_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Змінити назву нагадування", callback_data="edit_name"),
                InlineKeyboardButton("Змінити частоту нагадування", callback_data="edit_periodicity"),
                InlineKeyboardButton("Змінити період перериву", callback_data="edit_break_time"))
    return markup

def show_stat_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Графік за певний період", callback_data="graf_some_period"),
                InlineKeyboardButton("Статистика за весь час", callback_data="stat_all_time"),
                InlineKeyboardButton("Аналіз за весь час", callback_data="analyze_stat"))
    return markup
    
def bot_main():
    @bot.message_handler(commands=['start','menu'])
    def start_message(message):
        if message.text == "/start":
            bot.send_message(message.chat.id, """Привіт я бот нагадувач, буду тобі нагадувати про щось що ти мусиш робити кожен день або декілька разів в день.
            Також я можу вести статистику, наприклад нагадувати тобі присідати а після записувати скільки ти зробив разів. Якщо зацікавив жми /menu""")
        elif message.text == "/menu":
            bot.send_message(message.chat.id, "Виберіть, що Вас цікавить.",reply_markup=menu_markup())

    @bot.message_handler(context_type=['text'])
    def log_fun(message):
        print(message.text)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        user_id = call.from_user.id
        chat_id = call.message.chat.id
        #menu
        if call.data == "add_remider":
            bot.send_message(chat_id,"Виберіть, що Вас цікавить.", reply_markup=add_remider_markup()) 
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "edit_remider":
            bot.send_message(chat_id,"Виберіть, що Вас цікавить.", reply_markup=edit_remider_markup())
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "show_stat":
            bot.send_message(chat_id, "Виберіть, що Вас цікавить.", reply_markup=show_stat_markup())
            bot.delete_message(call.message.chat.id, call.message.message_id) 
        elif call.data == "other":
            bot.send_message(chat_id, "В розробці")
            bot.delete_message(call.message.chat.id, call.message.message_id)
        #add_remider
        elif call.data == "add_remider":
            bot.send_message(chat_id, "Виберіть, що Вас цікавить.")
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "add_remider_with_bd":
            bot.send_message(chat_id,"Виберіть, що Вас цікавить.") 
            bot.delete_message(call.message.chat.id, call.message.message_id)
        #edit_remider
        elif call.data == "edit_name":
            bot.send_message(call.message.chat.id, "Введіть нову назву нагадування ( максимальна довжина 20 знаків ) ")
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "edit_periodicity":
            bot.send_message(call.id, "Введіть час повтороно нагадування /n в годинах: 3h або ж в хвилинах 30m")
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "edit_break_time":
            bot.send_message(chat_id, "Введіть період в 24 годинному форматі /n  наприклад: /21:00-6:00 ")
            bot.delete_message(call.message.chat.id, call.message.message_id)
        #show_stat
        elif call.data == "graf_some_period":
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "stat_all_time":
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "analyze_stat":
            bot.delete_message(call.message.chat.id, call.message.message_id)

    bot.polling()
        
def start_restart():
    try:
        bot_main()
    except Exception as e:
        start_restart()

start_restart()