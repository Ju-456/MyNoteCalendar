from kivy.app import App
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.core.window import Window
from kivy.utils import platform

import calendar
from datetime import datetime
import os
import re

from annexe_functions import CurrentDayId 
from annexe_functions import MonthConvertInNumber
from annexe_functions import MonthConvertInNumberDico
from annexe_functions import GetDotMarkupFromFile
from annexe_functions import get_preview_text
from annexe_functions import get_app_storage_path

Builder.load_file("kivy_files/AgendaWidget.kv")
Builder.load_file("kivy_files/NotePopup.kv")
user_home = os.path.expanduser("~")

class AgendaWidget(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Window.bind(on_key_down=self.on_key_down_p)
        self.click_on_p = False

        self.SelectCurrentMonth()
        Clock.schedule_once(self.SelectCurrentMonth, 0)
        Clock.schedule_once(self.CurrentDayEffect, 0.1) # wait for the charmgent

        today = datetime.now()
        year = today.year
        month = today.month
        first_day_index = calendar.monthrange(year, month)[0]
        
        self.InitCalendarForCurrentMonth(year, month, first_day_index)
        self.bind(current_tab=self.DetectTabChange)

        self.note_popup = None

    def SelectCurrentMonth(self, *args):
        month_index = datetime.now().month
          
        month_ids = MonthConvertInNumber(args)

        current_month_id = month_ids[month_index - 1]
        if current_month_id in self.ids:
            self.switch_to(self.ids[current_month_id])
        else:
            print(f"Warning : {current_month_id} not found in ids")        

    def CurrentDayEffect(self, dt=None):
        today = datetime.now()
        year = today.year
        current_month = today.month

        first_day_index = calendar.monthrange(year, current_month)[0]

        current_day_id = CurrentDayId(first_day_index, current_month)

        if current_day_id in self.ids:
            button = self.ids[current_day_id]
            button.background_color = (0.6, 0.8, 1, 1)  # clear blue
        else:
            print(f"the button '{current_day_id}' not found.")
    
    def on_key_down_p(self, window, key, scancode, codepoint, modifiers):
        if codepoint == 'p':
            self.click_on_p = not self.click_on_p
            print(f"Toggle click_on_p: {self.click_on_p}")

            today = datetime.now()
            year = today.year
            month = today.month
            first_day_index = calendar.monthrange(year, month)[0]

            self.InitCalendarForCurrentMonth(year, month, first_day_index)

    def InitCalendarForCurrentMonth(self, current_year, current_month, first_day_index):
        nb_days_in_month = calendar.monthrange(current_year, current_month)[1]  # total of number in the month
        count = 1 

        month_abbr = calendar.month_abbr[current_month].lower()
        today = datetime.now()
        current_day_id = None
        if current_month == today.month and current_year == today.year:
            today_first_day_index = calendar.monthrange(current_year, current_month)[0]
            current_day_id = CurrentDayId(today_first_day_index, current_month)
            print(f"current_day_id: {current_day_id}")

        for i in range(first_day_index, first_day_index + nb_days_in_month):
            button_id = f"{month_abbr}_{i}_btn"

            if button_id in self.ids:
                button = self.ids[button_id]

                button.day_number = count # real day bc ids button =/= day number
                button.text = str(count)
                button.halign = "left"
                button.valign = "top"
                button.text_size = button.size
                button.padding = (5, 5)  # optional padding 
                button.shorten = False  
                button.markup = True
                button.bind(on_press=self.DetectClickButton) # to detecxt click 

                current_tab_folder = os.path.join(user_home, "MyNoteCalendar", month_abbr)
                note_path = os.path.join(current_tab_folder, f"{month_abbr}_{button.day_number}.txt")
                print(f"note_path: {note_path}")
                
                if os.path.exists(note_path):
                    if self.click_on_p:  #detection with boolean
                        button.text = get_preview_text(note_path, button.day_number)
                    else:
                        button.text = GetDotMarkupFromFile(note_path, current_day_id, button_id, button.day_number)
       
                count += 1
        
        self.DisablePaddingButtons(current_year, current_month, first_day_index)

    def DisablePaddingButtons(self, current_year, current_month, first_day_index):
        nb_days_in_month = calendar.monthrange(current_year, current_month)[1]
        month_abbr = calendar.month_abbr[current_month].lower()

        #print(f"Disable Buttons called for {month_abbr},\nnb of days in month: {nb_days_in_month},\nfirst_day_index: {first_day_index}")

        for day in range(0, first_day_index ): # disable days before the 1st
            button_id = f"{month_abbr}_{day}_btn"
            if button_id in self.ids:
                btn = self.ids[button_id]
                btn.disabled = True
                btn.background_color = (0.8, 0.8, 0.8, 1)
                btn.color = (0.5, 0.5, 0.5, 1)
            else:
                print(f"Button {button_id} not found!")

        for day in range(nb_days_in_month + first_day_index, 35): # disable days after the 31st
            button_id = f"{month_abbr}_{day}_btn"
            if button_id in self.ids:
                btn = self.ids[button_id]
                btn.disabled = True
                btn.background_color = (0.8, 0.8, 0.8, 1)
                btn.color = (0.5, 0.5, 0.5, 1)
            else:
                print(f"Button {button_id} not found!")

    def DetectTabChange(self, instance, current_tab):
        current_tab = self.current_tab
        print(current_tab.text)

        if current_tab:
            print(f"User is in the month : {current_tab.text}")

            month_text = current_tab.text.lower() 
            month_dict = MonthConvertInNumberDico()
            month_num = month_dict.get(month_text)

            if not month_num:
                print("Invalid tab text, can't convert it")
                return
            
            today = datetime.now()
            year = today.year
            first_day_index = calendar.monthrange(year, month_num)[0]
            self.InitCalendarForCurrentMonth(year, month_num, first_day_index)
        else:
            print("User is nowhere")

    def DetectClickButton(self, instance):
        current_tab = self.current_tab  # active tab

        #to integer in NotePopup
        day = instance.text.strip().splitlines()[0]
        month = current_tab.text.lower() 

        print(f"day : {day}")
        print(f"month : {month}")
        
        if current_tab:
            print(f"\nReaction test -> You clicked: {month}_{day}_btn\n")
            button_name = f"Write a note for the [b]{day} {month}[/b] :"
            #print(button_name)

            if not self.note_popup:
                self.note_popup = NotePopup(day=day, month=month)
                self.note_popup.open()
            else:# maj of all attribute
                self.note_popup.day = day
                self.note_popup.month = month
                self.note_popup.label_text = button_name # maj before open
                self.note_popup.LoadNote(month)  # forced the loading
                self.note_popup.open()
                        
class NotePopup(Popup):
    label_text = StringProperty("")
    show_preview = BooleanProperty(True)
    
    def __init__(self, day, month, **kwargs):
        super().__init__(**kwargs)
        self.day = str(day).strip().splitlines()[0]
        self.month = month
        print(f"In NotePopup : NotePopup created for day: {day}, month: {month}")
        self.ids.note_input.bind(text=self.update_preview)

    def SaveNoteInAfile(self):
        current_tab = self.ids.tab_label.text # active tab
        print(f"DEBUG / current_tab = {current_tab}")

        if current_tab:
            base_path = get_app_storage_path() # adapted path in function of platform
            current_tab_folder = os.path.join(base_path, f"{self.month}")
            current_tab_file = os.path.join(current_tab_folder, f"{self.month}_{self.day}.txt")
            print(f"DEBUG / self.month = {self.month}")
            print(f"DEBUG / self.day = {self.day}")
            note_text = self.ids.note_input.text.strip() # remove the space at the beginning and end of the txt

            if not note_text:
                print("Note is empty, not saving.")
                return 
    
            print(f"DEBUG / current_tab_folder = {current_tab_folder}")
            print(f"DEBUG / current_tab_file = {current_tab_file}")

            if not os.path.exists(current_tab_folder):
                print(f"Folder doesn't exit : {current_tab_folder}, creation...")
                os.makedirs(current_tab_folder, exist_ok=True)

            with open(current_tab_file, 'w', encoding='utf-8') as f:
                f.write(note_text)
                print(f"Note mise à jour dans le fichier : {current_tab_file}")
            self.dismiss()

        print(f"SaveNoteInAfile called. Text content: {self.ids.note_input.text}")
    
    def RemoveNote(self):
        current_tab_file = os.path.join(user_home, "MyNoteCalendar", f"{self.month}", f"{self.month}_{self.day}.txt")
        current_tab_folder = os.path.join(user_home,f"MyNoteCalendar", f"{self.month}")

        if os.path.exists(current_tab_file):
            os.remove(current_tab_file)
            print(f"Remove the note for : {current_tab_file}")

        if os.path.exists(current_tab_folder) and len(os.listdir(current_tab_folder)) == 0:
            os.rmdir(current_tab_folder)
            print(f"Remove the folder : {current_tab_folder} bc empty now")

    def LoadNote(self, month):
        current_tab_folder = os.path.join(user_home, "MyNoteCalendar", month)
        note_path = os.path.join(current_tab_folder, f"{month}_{self.day}.txt")
        print(f"current_tab_folder: {current_tab_folder}")
        print(f"note_path: {note_path}")

        current_tab = self.ids.tab_label.text # active tab
        print(f"DEBUG / current_tab = {current_tab}")

        self.ids.note_input.text = "" # remove the last txt before

        if current_tab and os.path.exists(note_path):
            with open(note_path, 'r', encoding='utf-8') as f:
                note_text = f.read()  # reading the file

            self.ids.note_input.text = note_text  # affected the widget's contain
            self.show_preview = True
            print("Note loaded:", note_text)
            return True
        else:
            self.ids.note_input.text = ""
            self.show_preview = False
            print("File does not exist.")
            return False
    
    def update_preview(self, instance, value):
        self.ids.preview_label.text = value

    def store_selection(self, s, e):
        self.selection_from = s
        self.selection_to = e
        print(f"Register selection : s = {s} et e = {e}")
    
    def select_and_store(self):
        ti = self.ids.note_input
        ti.focus = True
        
        Clock.schedule_once(lambda dt: ti.select_all(), 0) # 1st clock cycle : register the departure
        Clock.schedule_once(lambda dt: self.store_selection(ti.selection_from, ti.selection_to), 0.01) # # 2nd clock cycle : save all the selection 
    
    def apply_style(self, style):
        ti = self.ids.note_input
        s, e = self.selection_from, self.selection_to

        if s == e:
            print("No text selected")
            return
        if s > e:
            s, e = e, s

        selected = ti.text[s:e]
        ti.select_text(s, e)

        tag_map = {
            "bold": "b",
            "italic": "i",
            "pastel_green": "color=#a6fca6",
            "pastel_yellow": "color=#dada6c",
            "pastel_blue": "color=#a8d1fd",
            "color_red": "color=#7a0202",
            "color_green": "color=#036d03",
            "color_blue": "color=#121274",
        }

        if style not in tag_map:
            return

        wrapped = self.toggle_bbcode(selected, tag_map[style])

        ti.text = ti.text[:s] + wrapped + ti.text[e:]
        self.note_preview = ti.text
        ti.focus = True

    def toggle_bbcode(self, text, tag):
        if tag.startswith("color="):
            open_tag = f"[{tag}]"
            close_tag = "[/color]"
            pattern = re.compile(
                rf'^\s*\[{re.escape(tag)}\]\s*(.*?)\s*\[/color\]\s*$',
                re.DOTALL
            )
        else:
            open_tag = f"[{tag}]"
            close_tag = f"[/{tag}]"
            pattern = re.compile(
                rf'^\s*\[{re.escape(tag)}\]\s*(.*?)\s*\[/{re.escape(tag)}\]\s*$',
                re.DOTALL
            )

        match = pattern.match(text)
        if match:
            return match.group(1)  # déwrappé
        else:
            return f"{open_tag}{text}{close_tag}"

    def toggle_color_menu(self):
        color_menu = self.ids.color_menu
        if color_menu.height == 0:
            color_menu.height = '40dp'
            color_menu.opacity = 1
        else:
            color_menu.height = 0
            color_menu.opacity = 0

    def toggle_pastel_menu(self):
        pastel_menu = self.ids.pastel_menu
        if pastel_menu.height == 0:
            pastel_menu.height = '40dp'
            pastel_menu.opacity = 1
        else:
            pastel_menu.height = 0
            pastel_menu.opacity = 0

    def toggle_view(self):
        self.show_preview = not self.show_preview
        self.update_preview(None, self.ids.note_input.text)

    def close_pastel_menu(self):
        self.pastel_menu.opacity = 0
        self.pastel_menu.disabled = True

    def close_color_menu(self):
        self.color_menu.opacity = 0
        self.color_menu.disabled = True


class MyNoteCalendar(App):
    def build(self):
        return AgendaWidget()