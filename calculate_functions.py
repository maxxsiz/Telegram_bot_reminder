from datetime import date, time, datetime, timedelta
from database_fun import all_active_reminders, take_user_timezone

def send_time_text(type_text):
    now = datetime.now().strftime("%M")
    t_text = ''
    t_list = []
    if type_text == "list":
        for i in range(24):
            if i >= 0 and i < 10:
                 t_list.append("/0" + str(i))
            else:
                t_list.append("/" + str(i))
        return t_list
    else: 
        added_text =":" + str(now) +  "  "
        for i in range(24):
            if i >= 0 and i < 10:
                t_text += "/0" + str(i) + added_text
            else:
                t_text += "/" + str(i) + added_text
        return t_text


def calc_timezone(hour): #timezone calculator
    now = datetime.now().strftime("%H")
    timezone =  int(hour) - int(now) + 1
    return timezone

def create_time_line(reminder_id, periodisity, break_time): #create or update timeline for user`s solo reminder
    #tm = take_user_timezone(int(reminder_id[:-3])
    start_t = timedelta(hours=int(break_time[-5:-3]), minutes=int(break_time[-2:]))
    end_t = timedelta(hours=int(break_time[:2]), minutes=int(break_time[3:5]))
    per_min = lambda p: int(p[:-1]) if str(p[-1]) == "m" else int(p[:-1])*60
    per_t = timedelta(minutes=per_min(periodisity))
    if start_t > end_t:
        start_t, end_t = end_t, start_t
        time_line = [reminder_id, start_t]
        while start_t > end_t:
            end_t = end_t + per_t
            time_line.append(start_t)
    else:
        time_line = [reminder_id, start_t]
        while start_t < end_t:
            start_t = start_t + per_t
            time_line.append(start_t)
    for i in time_line:
           print(i)

create_time_line("12", "50m", "03:30-12:20")
