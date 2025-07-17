import calendar
from datetime import date, datetime

import re 

def FirstDayInAMouth():
    current_datetime = datetime.now()
    current_year = current_datetime.year
    current_month = current_datetime.month

    first_day_index = calendar.monthrange(current_year, current_month)[0]
    print(f"Id of the first_day_index = {first_day_index}") # 0 = monday, 1 = tuesday ,ects...
    
    return first_day_index, current_month

def CurrentDayId(first_day_index, current_month):
    current_day = datetime.now().day

    month_abbr = calendar.month_abbr[current_month].lower()
    index_in_tab = first_day_index + current_day - 1
    current_day_id = f"{month_abbr}_{index_in_tab}_btn"

    print(f"Id of the current day = {current_day_id}")

    return current_day_id

first_day_index, current_month = FirstDayInAMouth()
CurrentDayId(first_day_index, current_month)