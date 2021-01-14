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

def break_time(breaktime):
    m_1 = re.fullmatch(r'[0-1][0-9][:][0-5][0-9]-[0-2][0-9][:][0-5][0-9]', breaktime)
    m_2 = re.fullmatch(r'[2][0-3][:][0-5][0-9]-[2][0-3][:][0-5][0-9]', breaktime)
    return True if m_1 or m_2 else False

def check_periodisity(periodisity):
    match = re.fullmatch(r'\d{1,2}[h,m]', periodisity)
    return True if match else False

def check_date(date):
    match = re.fullmatch(r'\d\d/\d\d/\d{4}',date)
    return True if match else False

def check_count(count):
    match = re.fullmatch(r'\d{,4}',count)
    return True if match else False
