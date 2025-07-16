from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel

Builder.load_file("AgendaWidget.kv")

class AgendaWidget(TabbedPanel):
    pass

class agenda(App):
    def build(self):
        return AgendaWidget()
    
if __name__ == '__main__':
    agenda().run()