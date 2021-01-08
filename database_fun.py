import sqlite3

conn = sqlite3.connect('sqlite.db')

def add_new_user(user_id, user_name, user_first_name, registration_date, language, timezone):#добавление пользователя 1tablica  (user_id, name, date_registration)
    c = conn.cursor()
    c.execute("INSERT INTO users_info VALUES (?,?,?,?,?,?)",(user_id, user_name, user_first_name, registration_date, language, timezone))
    conn.commit()
    conn.close()

def add_new_reminder(user_id, reminder_id, reminder_name, reminder_description, reminder_type, periodisity, break_time, active_status):
    c = conn.cursor()
    c.execute("INSERT INTO ? VALUES (?,?,?,?,?,?,?)",(user_id, reminder_id, reminder_name, reminder_description, reminder_type, periodisity, break_time, active_status))
    conn.commit()
    conn.close()

def reminder_edit(edit_type, user_id, reminder_id, reminder_name, reminder_description, reminder_type, periodisity, break_time, active_status):#редагування напоминнаня (видалення, замороження, зміна данних)
    if edit_type == "delete":#видалення нагадування
        c = conn.cursor()
        c.execute("DELETE FROM reminders_main WHERE reminder_id = ?", (user_id, reminder_id))
        c.execute("DELETE FROM reminders_simple_info WHERE reminder_id = ?", (user_id, reminder_id))
        c.execute("DELETE FROM reminders_adv_info WHERE reminder_id = ?", (user_id, reminder_id))
        conn.commit()
        conn.close()
        return "Нагадування видалено"
    elif edit_type == "freeze": #замороження нагадування
        c = conn.cursor()
        c.execute("UPDATE ? SET active_status = ? WHERE reminder_id = ?", (user_id, active_status, reminder_id))
        conn.commit()
        conn.close()
        return "Нагадування призупинено"
    elif edit_type == "edit":#редагування напоминнаня
        c = conn.cursor()
        c.execute("""UPDATE ? SET reminder_name = ?, reminder_description = ?, reminder_type = ?, periodisity = ?, break_time = ? WHERE reminder_id = ?""", (user_id, reminder_name, reminder_description, reminder_type, periodisity, break_time, reminder_id))
        conn.commit()
        conn.close()
        return "Нагадування змінено"
    else:
        return "Упс, щось пішло не так"

def all_reminders(user_id,reminder_type): #витягування списку напоминаннь да інформації про них
    c = conn.cursor()
    if reminder_type == "simple_type":
        all_reminders = c.execute("SELECT * FROM ? WHERE reminder_type = ? ",(user_id,reminder_type))
    elif reminder_type == "stat_type":
        all_reminders = c.execute("SELECT * FROM ? WHERE reminder_type = ? ",(user_id,reminder_type))
    elif reminder_type == "all":
        all_reminders = c.execute("SELECT * FROM ?",(user_id))
    conn.close()
    return all_reminders

def reminder_stat(user_id):
    return "в розробці"


def check_register(user_id):
    c = conn.cursor()
    c.execute("SELECT * FROM users_info WHERE user_id = ? ",(user_id))
    check = c.fetchall()
    if check is not None:
        return True
    else:
        return False