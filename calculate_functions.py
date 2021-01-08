from datetime import date, time

def send_time_text(type_text):
    t = time.minute()
    t_text = ''
    t_list = []
    if type_text == "list":
        for i in range(24):
            if i >= 0 and i < 10:
                 t_list.append("/0" + str(i) + ":" +str(t))
            else:
                t_list.append("/" + str(i) + ":" +str(t))
        return t_list
    else: 
        added_text =":" + str(t) +  "  "
        for i in range(24):
            if i >= 0 and i < 10:
                t_text += "/0" + str(i) + added_text
            else:
                t_text += "/" + str(i) + added_text
        return t_text


def calc_timezone(hour): #timezone calculator
    t = time.hour()
    timezone =  int(hour) - int(t) + 1
    return timezone