from datetime import date, datetime
import calendar
import os
import re 
from kivy.app import App
from kivy.utils import platform

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

def get_dot_markup_from_file(filepath, current_day_id, button_id, button_day_number):
    if not os.path.exists(filepath):
        return str(button_day_number)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    max_dots = 7
    number_of_dot = len(re.findall(r"^-", content, re.MULTILINE))
    number_of_dot = min(number_of_dot, max_dots)  # limit = max_dots

    if number_of_dot == 0:
        number_of_dot = 1 # to have at least one point as an indicator
    
    color = "#9909CC" if button_id == current_day_id else "#99ccff"
    print(f"button_id = {button_id} current_day_id = {current_day_id}")
    dots = "• " * number_of_dot
    return f"{button_day_number}\n[size=24][color={color}]{dots.strip()}[/color]"

def get_preview_text(note_path, day_number, max_chars=200):
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    if not content:
        return str(day_number)
    
    preview = content[:max_chars]
    if len(content) > max_chars:
        preview += "…"
    return f"{day_number}\n[i]{preview}[/i]"

def get_app_storage_path():
    from kivy.utils import platform
    try:
        if platform in ("android", "ios"):
            return App.get_running_app().user_data_dir
        else:
            return os.path.expanduser("~/MyNoteCalendar")
    except Exception:
        if platform == "android":
            from android.storage import app_storage_path # type: ignore
            return app_storage_path()
        elif platform == "ios":
            from os.path import expanduser
            return os.path.join(expanduser("~"), "Documents")
        else:
            return os.path.expanduser("~/MyNoteCalendar")

