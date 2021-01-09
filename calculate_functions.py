from datetime import date, time, datetime

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