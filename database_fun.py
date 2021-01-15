import sqlite3
import codecs

def add_new_user(userid, user_first_name, user_last_name, registration_date, language, timezone):#добавление пользователя 1tablica  (user_id, name, date_registration)
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute("INSERT INTO users_info VALUES (?,?,?,?,?,?)",(userid, user_first_name, user_last_name, registration_date, language, timezone,))
    conn.commit()
    conn.close()

def add_new_reminder(userid, reminder_id, reminder_name, reminder_description, reminder_type, periodisity, break_time, active_status, count, stat_dict):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute("INSERT INTO reminders_main VALUES (?,?,?,?,?,?,?,?,?,?)",(userid, reminder_id, reminder_name, reminder_description, reminder_type, periodisity, break_time, active_status, count, stat_dict))
    conn.commit()
    conn.close()

def reminder_delete(reminder_id):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute("DELETE FROM reminders_main WHERE reminder_id = ?", (reminder_id,))
    #c.execute("DELETE FROM reminders_simple_info WHERE reminder_id = ?", (reminder_id,))
    #c.execute("DELETE FROM reminders_adv_info WHERE reminder_id = ?", (reminder_id,))
    conn.commit()
    conn.close()
    return "Нагадування видалено"

def check_reminder_status(reminder_id):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute("SELECT active_status FROM reminders_main WHERE reminder_id = ?",(reminder_id,))
    if int(c.fetchone()[0]) == 0:
        active_status = 0
    else: 
        active_status = 1
    conn.close()
    return active_status

def reminder_freeze(reminder_id, active_status):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute("UPDATE reminders_main SET active_status = ? WHERE reminder_id = ?", (active_status, reminder_id,))
    conn.commit()
    conn.close()
    return "Нагадування призупинено" 
    
def reminder_edit(reminder_id, column_name, new_value):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    column_name = column_name.encode("utf-8").decode("utf-8")
    q = "UPDATE reminders_main SET {kolumn} = ? WHERE reminder_id = ?".format(kolumn = column_name)
    c.execute(q,(new_value, reminder_id))
    print(q)
    conn.commit()
    conn.close()
    return "Нагадування змінено"

def single_reminder(reminder_id):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute("SELECT reminder_name, reminder_description, periodisity, break_time FROM reminders_main WHERE reminder_id = ?",(reminder_id,))
    datas = c.fetchone()
    return datas

def all_reminders(userid, reminder_type, few_type): #витягування списку напоминаннь да інформації про них
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    if reminder_type == "simple_type":
        all_reminders = c.execute("SELECT * FROM reminders_main WHERE reminder_type = ? AND user_id = ?",(reminder_type, userid,))
    elif reminder_type == "stat_type":
        all_reminders = c.execute("SELECT * FROM reminders_main WHERE reminder_type = ? AND user_id = ?",(reminder_type, userid,))
    elif reminder_type == "all":
        all_reminders = c.execute("SELECT * FROM reminders_main WHERE  user_id = ?",(userid,))  
    all_reminders_text = "Кнопка | Назва | Повний опис | Повторення кожних | Перерва \n"
    for row in all_reminders:
        if few_type == "withslash":
            all_reminders_text += f"/{row[1]} | {row[2]} | {row[3]} | {row[5]} | {row[6]} \n"
        else:
            all_reminders_text += f"{row[2]} | {row[3]} | {row[5]} | {row[6]} \n"
    conn.close()
    return all_reminders_text

def all_reminders_list(userid, reminder_type):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    if reminder_type == "simple_type":
        all_reminders = c.execute("SELECT reminder_id FROM reminders_main WHERE reminder_type = ? AND user_id = ?",(reminder_type, userid,))
    elif reminder_type == "stat_type":
        all_reminders = c.execute("SELECT reminder_id FROM reminders_main WHERE reminder_type = ? AND user_id = ?",(reminder_type, userid,))
    elif reminder_type == "all":
        all_reminders = c.execute("SELECT reminder_id FROM reminders_main WHERE  user_id = ?",(userid,))  
    all_reminders_list = []
    for row in all_reminders:
        all_reminders_list.append(row[0])
    print(all_reminders_list)
    conn.close()
    return all_reminders_list

def reminder_stat(userid):
    return "в розробці"

def all_active_reminders():
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute("SELECT reminder_id, periodisity, break_time FROM reminders_main WHERE active_status = True")
    for row in all_reminders:
        all_reminders_list.append(row[0])
    return rm_list


def check_register(userid):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users_info WHERE user_id = ? ",(userid,))
    check = c.fetchone()
    conn.close()
    if check is not None:
        print("вже зареєстрований")
        return False
    else:
        print("ще не зареєстрований")
        return True

def check_reminder_count(userid):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reminders_main WHERE user_id = ? ",(userid,))
    check = c.fetchall()
    conn.close()
    len_check = len(check)
    if len_check < 10:
        return "00" + str(len_check)
    elif len_check < 100:
        return "0" + str(len_check)
    elif len_check < 1000:
        return str(len_check)
    else:
        return False


def take_user_timezone(userid):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute("SELECT timezone FROM user_info WHERE user_id = ? ",(userid,))
    timezone = c.fetchone()
    conn.close()
    return timezone