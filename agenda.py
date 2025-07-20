from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.clock import Clock

import calendar
from datetime import date, datetime

from calendar_gestion import CurrentDayId 
from calendar_gestion import MonthConvertInNumber
from calendar_gestion import MonthConvertInNumberDico

Builder.load_file("AgendaWidget.kv")

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

    def InitCalenderForCurrentMonth(self, current_year, current_month, first_day_index ):
        nb_days_in_month = calendar.monthrange(current_year, current_month)[1]  # total of number in the month
        count = 1 

        month_abbr = calendar.month_abbr[current_month].lower()

        for i in range(first_day_index, first_day_index + nb_days_in_month):
            button_id = f"{month_abbr}_{i}_btn"

            if button_id in self.ids:
                button = self.ids[button_id]
                button.text = str(count)
                count += 1

    def DetectTabChange(self, instance, current_tab):
        current_tab = self.current_tab
        print(current_tab.text)

        if current_tab:
            print(f"User is in the month : {current_tab.text}")

            month_text = current_tab.text.lower() 
            month_dict = MonthConvertInNumberDico()
            month_num = month_dict.get(month_text)

            if not month_num:
                print("Inval_id tab text, can't convert it")
                return
            
            today = datetime.now()
            year = today.year
            first_day_index = calendar.monthrange(year, month_num)[0]
            self.InitCalenderForCurrentMonth(year, month_num, first_day_index)
        else:
            print("User is nowhere")

class agenda(App):
    def build(self):
        return AgendaWidget()
    
if __name__ == '__main__':
    agenda().run()