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

import calendar
from datetime import date, datetime

import os

from calendar_gestion import CurrentDayId 
from calendar_gestion import MonthConvertInNumber
from calendar_gestion import MonthConvertInNumberDico

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

        for i in range(first_day_index, first_day_index + nb_days_in_month):
            button_id = f"{month_abbr}_{i}_btn"

            if button_id in self.ids:
                button = self.ids[button_id]

                button.text = str(count)
                button.halign = "left"
                button.valign = "top"
                button.text_size = button.size
                button.padding = (5, 5)  # optional padding 
                button.shorten = False  
                button.markup = True
                button.bind(on_press=self.DetectClickButton) # to detecxt click    

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
        day = instance.text.lower()
        month = current_tab.text.lower() 

        if current_tab:
            month_text = current_tab.text.lower()
            print(f"\nReaction test -> You clicked: {month_text}_{instance.text}_btn\n")
            button_name = f"Write a note for the [b]{instance.text} {month_text}[/b] :"
            print(button_name)

            if not self.note_popup: # if the 'PopUp window' doesn't exist, we create it only ONE time
                self.note_popup = NotePopup(day=day, month=month)
            
            self.note_popup.label_text = button_name # maj before open
            self.note_popup.open()
        else:
            print("No tab selected.")
            
class NotePopup(Popup):
    label_text = StringProperty("")
    
    def __init__(self, day, month, **kwargs):
        super().__init__(**kwargs)
        self.day = day
        self.month = month
        print(f"NotePopup created for day: {day}, month: {month}")

    def SaveNoteInAfile(self, instance):
        current_tab = self.ids.tab_label.text# active tab
        print(f"DEBUG / current_tab = {current_tab}")
        if current_tab:
            current_tab_folder = os.path.join(user_home,f"NoteCalendar", f"{self.month}")
            current_tab_file = os.path.join(current_tab_folder, f"{self.month}_{self.day}.txt")
            note_text = self.ids.note_input.text

            print(f"DEBUG / current_tab_folder = {current_tab_folder}")
            print(f"DEBUG / current_tab_file = {current_tab_file}")

            if not os.path.exists(current_tab_folder):
                print(f"Folder doesn't exit : {current_tab_folder}, creation...")
                os.makedirs(current_tab_folder, exist_ok=True)

            if os.path.exists(current_tab_file):
                print(f"the file '{current_tab_file}' already exist")
                # future pop up window after to propose modification
            else:
                with open(current_tab_file, 'w', encoding='utf-8') as f:
                    f.write(note_text)
                    print(f"File contain : {current_tab_file}")
                print("File saved")
                self.dismiss()
        print(f">>> SaveNoteInAfile called with instance = {instance}, text = {instance.text}")

class agenda(App):
    def build(self):
        return AgendaWidget()
    
if __name__ == '__main__':
    agenda().run()