import sqlite3

conn = sqlite3.connect('sqlite.db')

def add_new_user(userid, user_first_name, user_last_name, registration_date, language, timezone):#добавление пользователя 1tablica  (user_id, name, date_registration)
    c = conn.cursor()
    c.execute("INSERT INTO users_info VALUES (?,?,?,?,?,?)",(userid, user_first_name, user_last_name, registration_date, language, timezone,))
    conn.commit()
    conn.close()

def add_new_reminder(userid, reminder_id, reminder_name, reminder_description, reminder_type, periodisity, break_time, active_status):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute("INSERT INTO reminders_main VALUES (?,?,?,?,?,?,?,?)",(userid, reminder_id, reminder_name, reminder_description, reminder_type, periodisity, break_time, active_status,))
    conn.commit()
    conn.close()

def reminder_edit(edit_type, userid, reminder_id, reminder_name, reminder_description, reminder_type, periodisity, break_time, active_status):#редагування напоминнаня (видалення, замороження, зміна данних)
    if edit_type == "delete":#видалення нагадування
        c = conn.cursor()
        c.execute("DELETE FROM reminders_main WHERE reminder_id = ?", (reminder_id,))
        c.execute("DELETE FROM reminders_simple_info WHERE reminder_id = ?", (reminder_id,))
        c.execute("DELETE FROM reminders_adv_info WHERE reminder_id = ?", (reminder_id,))
        conn.commit()
        conn.close()
        return "Нагадування видалено"
    elif edit_type == "freeze": #замороження нагадування
        c = conn.cursor()
        c.execute("UPDATE reminders_main SET active_status = ? WHERE reminder_id = ?", (active_status, reminder_id,))
        conn.commit()
        conn.close()
        return "Нагадування призупинено"
    elif edit_type == "edit":#редагування напоминнаня
        c = conn.cursor()
        c.execute("""UPDATE reminders_main SET reminder_name = ?, reminder_description = ?, reminder_type = ?, periodisity = ?, break_time = ? WHERE reminder_id = ?""", (reminder_name, reminder_description, reminder_type, periodisity, break_time, reminder_id,))
        conn.commit()
        conn.close()
        return "Нагадування змінено"
    else:
        return "Упс, щось пішло не так"

def all_reminders(userid, reminder_type): #витягування списку напоминаннь да інформації про них
    c = conn.cursor()
    if reminder_type == "simple_type":
        all_reminders = c.execute("SELECT * FROM reminders_main WHERE reminder_type = ? AND user_id = ?",(reminder_type, userid,))
    elif reminder_type == "stat_type":
        all_reminders = c.execute("SELECT * FROM reminders_main WHERE reminder_type = ? AND user_id = ?",(reminder_type, userid,))
    elif reminder_type == "all":
        all_reminders = c.execute("SELECT * FROM reminders_main WHERE  user_id = ?",(userid,))
    conn.close()
    return all_reminders

def reminder_stat(userid):
    return "в розробці"


def check_register(userid):
    c = conn.cursor()
    c.execute("SELECT * FROM users_info WHERE user_id = ? ",(userid,))
    check = c.fetchone()
    if check is not None:
        print("вже зареєстрований")
        return False
    else:
        print("ще не зареєстрований")
        return True

def check_reminder_count(userid):
    c = conn.cursor()
    c.execute("SELECT * FROM reminders_main WHERE user_id = ? ",(userid,))
    check = c.fetchall()
    conn.close()
    len_check = len(check)
    print(len_check)
    if len_check < 10:
        return "00" + str(len_check)
    elif len_check < 100:
        return "0" + str(len_check)
    elif len_check < 1000:
         return str(len_check)
    else:
        return False