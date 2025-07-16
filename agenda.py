from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.clock import Clock

import calendar
from datetime import date, datetime

Builder.load_file("AgendaWidget.kv")

class AgendaWidget(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.select_current_month()
        Clock.schedule_once(self.select_current_month, 0)

    def select_current_month(self, *args):
        month_index = datetime.now().month  
        month_ids = [
            "jan_tab", "feb_tab", "mar_tab", "apr_tab", "may_tab", "jun_tab",
            "jul_tab", "aug_tab", "sep_tab", "oct_tab", "nov_tab", "dec_tab"
        ]

        current_month_id = month_ids[month_index - 1]
        if current_month_id in self.ids:
            self.switch_to(self.ids[current_month_id])
        else:
            print(f"Warning: {current_month_id} not found in ids")

class agenda(App):
    def build(self):
        return AgendaWidget()
    
if __name__ == '__main__':
    agenda().run()