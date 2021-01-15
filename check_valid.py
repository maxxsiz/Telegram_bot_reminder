import re

def check_name(name):
    if len(name) < 20:
        return False
    else:
        return True
    
def check_description(description):
    if len(check_description) < 100:
        return False
    else:
        return True

def check_break_time(breaktime):
    match = re.fullmatch(r'[0-1][0-9][:][0-5][0-9]-[0-2][0-9][:][0-5][0-9]|[2][0-3][:][0-5][0-9]-[2][0-3][:][0-5][0-9]', breaktime)
    return True if match else False

def check_periodisity(periodisity): # min 5m, max 8h or 480m
    match = re.fullmatch(r'[1-8]h|[5-9]m|[1-9][0-9]m|[1-3][0-9][0-9]m|4[0-8]0m|4[0-7][0-9]m', periodisity)
    return True if match else False

def check_date(date):
    match = re.fullmatch(r'\d\d/\d\d/\d{4}',date)
    return True if match else False

def check_count(count):
    match = re.fullmatch(r'\d{,4}',count)
    return True if match else False
