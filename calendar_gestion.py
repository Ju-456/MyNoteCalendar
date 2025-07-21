import calendar
from datetime import date, datetime

import re 

def FirstDayInAMonth():
    current_datetime = datetime.now()
    current_year = current_datetime.year
    current_month = current_datetime.month

    first_day_index = calendar.monthrange(current_year, current_month)[0]
    print(f"Id of the first_day_index = {first_day_index}") # 0 = monday, 1 = tuesday ,ects...
    
    return first_day_index, current_month

def MonthConvertInNumber(*args): # to use ".get" bc dico can't be used as ".get"
    return  [
        "jan_tab", "feb_tab", "mar_tab", "apr_tab", "may_tab", "jun_tab",
        "jul_tab", "aug_tab", "sep_tab", "oct_tab", "nov_tab", "dec_tab"
    ]

def MonthConvertInNumberDico():
    return {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4,
        "may": 5, "jun": 6, "jul": 7, "aug": 8,
        "sep": 9, "oct": 10, "nov": 11, "dec": 12
    }

def CurrentDayId(first_day_index, current_month):
    current_day = datetime.now().day

    month_abbr = calendar.month_abbr[current_month].lower()
    index_in_tab = first_day_index + current_day - 1
    current_day_id = f"{month_abbr}_{index_in_tab}_btn"

    print(f"Id of the current day = {current_day_id}")

    return current_day_id

first_day_index, current_month = FirstDayInAMonth()
CurrentDayId(first_day_index, current_month)