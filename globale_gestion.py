from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.factory import Factory
from kivy.uix.textinput import TextInput

import calendar
from datetime import date, datetime
import os

from calendar_gestion import CurrentDayId 
from calendar_gestion import MonthConvertInNumber
from calendar_gestion import MonthConvertInNumberDico
from calendar_gestion import GetDotMarkupFromFile

Builder.load_file("kivy_files/AgendaWidget.kv")
Builder.load_file("kivy_files/NotePopup.kv")
user_home = os.path.expanduser("~")

class AgendaWidget(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SelectCurrentMonth()
        Clock.schedule_once(self.SelectCurrentMonth, 0)
        Clock.schedule_once(self.CurrentDayEffect, 0.1) # wait for the charmgent

        today = datetime.now()
        year = today.year
        month = today.month
        first_day_index = calendar.monthrange(year, month)[0]
        
        self.InitCalenderForCurrentMonth(year, month, first_day_index)
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

    def InitCalenderForCurrentMonth(self, current_year, current_month, first_day_index):
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

                current_tab_folder = os.path.join(user_home, "NoteCalendar", month_abbr)
                note_path = os.path.join(current_tab_folder, f"{month_abbr}_{button.day_number}.txt")
                print(f"note_path: {note_path}")
                
                if os.path.exists(note_path):  
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
            self.InitCalenderForCurrentMonth(year, month_num, first_day_index)
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
            current_tab_folder = os.path.join(user_home,f"NoteCalendar", f"{self.month}")
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

    def LoadNote(self, month):
        current_tab_folder = os.path.join(user_home, "NoteCalendar", month)
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
            print("Note loaded:", note_text)
        else:
            self.ids.note_input.text = ""
            print("File does not exist.")

    def get_markup_preview(self):
        return self.ids.note_input.text
    
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
        s = self.selection_from
        e = self.selection_to

        if s == e:
            print("No text selected")
            return

        if s > e:
            s, e = e, s

        selected = ti.text[s:e] #force the selection even if we lost the focus when we click on a button
        ti.select_text(s, e)

        if style == "bold":
            if selected.startswith("[b]") and selected.endswith("[/b]"):
                wrapped = selected[3:-4]
            else:
                wrapped = f"[b]{selected}[/b]"

        elif style == "italic":
            if selected.startswith("[i]") and selected.endswith("[/i]"):
                wrapped = selected[3:-4]
            else:
                wrapped = f"[i]{selected}[/i]"

        elif style == "pastel_green":
            color_code = "#ccffcc"
            wrapped = self.toggle_color(selected, color_code)

        elif style == "pastel_yellow":
            color_code = "#ffffcc"
            wrapped = self.toggle_color(selected, color_code)

        elif style == "pastel_blue":
            color_code = "#cce5ff"
            wrapped = self.toggle_color(selected, color_code)

        elif style == "color_red":
            color_code = "ff0000"
            wrapped = self.toggle_color(selected, color_code)

        elif style == "color_black":
            color_code = "000000"
            wrapped = self.toggle_color(selected, color_code)

        elif style == "color_green":
            color_code = "00aa00"
            wrapped = self.toggle_color(selected, color_code)

        elif style == "color_blue":
            color_code = "0000ff"
            wrapped = self.toggle_color(selected, color_code)

        else:
            return

        ti.text = ti.text[:s] + wrapped + ti.text[e:]
        self.note_preview = ti.text
        ti.focus = True

    def toggle_color(self, text, color_code):
        open_tag = f"[color={color_code}]"
        close_tag = "[/color]"

        if text.startswith(open_tag) and text.endswith(close_tag):
            return text[len(open_tag):-len(close_tag)]
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

class agenda(App):
    def build(self):
        return AgendaWidget()
    
if __name__ == '__main__':
    agenda().run()