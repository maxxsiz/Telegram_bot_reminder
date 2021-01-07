import sqlite3

conn = sqlite3.connect('sqlite.db')

def add_new_user(user_id, user_name, user_first_name, registration_date, language, timezone):#добавление пользователя 1tablica  (user_id, name, date_registration)
    c = conn.cursor()
    c.execute("INSERT INTO users_info VALUES (?,?,?,?,?,?)",(user_id, user_name, user_first_name, registration_date, language, timezone))
    #создание личной таблицы пользователя (remider_id, name , description, type, periodisity, break_time, active_status)
    c.execute("""CREATE TABLE ? 
             (remider_id INT, remider_name TEXT, remider_description TEXT, remider_type TEXT, periodisity INT, break_time INT, active_status BOOLEAN)""",(user_id))
    conn.commit()
    conn.close()

def add_new_remider(user_id, remider_id, remider_name, remider_description, remider_type, periodisity, break_time, active_status):
    c = conn.cursor()
    c.execute("INSERT INTO ? VALUES (?,?,?,?,?,?,?)",(user_id, remider_id, remider_name, remider_description, remider_type, periodisity, break_time, active_status))
    conn.commit()
    conn.close()

def remider_edit(edit_type, user_id, remider_id, remider_name, remider_description, remider_type, periodisity, break_time, active_status):#редагування напоминнаня (видалення, замороження, зміна данних)
    if edit_type == "delete":#видалення нагадування
        c = conn.cursor()
        c.execute("DELETE FROM ? WHERE remider_id = ?", (user_id, remider_id))
        conn.commit()
        conn.close()
        return "Нагадування видалено"
    elif edit_type == "freeze": #замороження нагадування
        c = conn.cursor()
        c.execute("UPDATE ? SET active_status = ? WHERE remider_id = ?", (user_id, active_status, remider_id))
        conn.commit()
        conn.close()
        return "Нагадування призупинено"
    elif edit_type == "edit":#редагування напоминнаня
        c = conn.cursor()
        c.execute("""UPDATE ? SET remider_name = ?, remider_description = ?, remider_type = ?, periodisity = ?, break_time = ? WHERE remider_id = ?""", (user_id, remider_name, remider_description, remider_type, periodisity, break_time, remider_id))
        conn.commit()
        conn.close()
        return "Нагадування змінено"
    else:
        return "Упс, щось пішло не так"

def all_remiders(user_id,remider_type): #витягування списку напоминаннь да інформації про них
    c = conn.cursor()
    if remider_type == "simple_type":
        all_remiders = c.execute("SELECT * FROM ? WHERE remider_type = ? ",(user_id,remider_type))
    elif remider_type == "stat_type":
        all_remiders = c.execute("SELECT * FROM ? WHERE remider_type = ? ",(user_id,remider_type))
    elif remider_type == "all":
        all_remiders = c.execute("SELECT * FROM ?",(user_id))
    conn.close()
    return all_remiders

def remider_stat(user_id):
    return "в розробці"
#витягування данних для статистики