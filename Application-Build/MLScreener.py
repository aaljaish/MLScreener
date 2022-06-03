from kivy.app import App
import time
from kivy.config import Config

from kivy.uix.button import Button
import pandas as pd
from kivy.uix.popup import Popup
from plyer import filechooser
import os
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.core.clipboard import Clipboard

from Classifier import Classifier

from kivy.core.window import Window

Window.size = (1000, 600)

Instructions = '''
1. Use your preferred bibliographic database to download a file that includes information
 about each article's title, abstract, keywords, and subject headings.
 
2. Ensure that the title column is labelled "TI".

3. Ensure that the abstract column is labelled as "AB".

4. Ensure that the keyword column is labelled as "KW".

5. Ensure that the subject headings column is labelled as "MH".

'''


def instruction_click(dummy):
    layout = GridLayout(rows=2, padding=[0, 0, 0, 0])

    popup_label = Label(text=Instructions, size_hint=(None, None), size=(650, 350),
                        halign='left', markup=True, font_size=15)
    layout.add_widget(popup_label)

    popup = Popup(title='Instructions',
                  title_size=20,
                  content=layout,
                  size_hint=(None, None), size=(700, 500))

    popup.open()

    close_popup = Button(text=(str('Close')), font_size=20, size_hint=(0.5, 0.2))
    layout.add_widget(close_popup)
    close_popup.bind(on_press=popup.dismiss)


class Root(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start = time.time()
        self.label = ""
        self.start_app()
        self.cwd = os.getcwd()
        self.cwd = self.cwd.replace("\\", "//")
        print('Main Directory: ', self.cwd)

    def start_app(self):
        instruction_button = Button(text=(str('Click here for instructions')),
                                    font_size=20,
                                    size_hint=(0.5, 0.2),
                                    background_color=(0, 0, 0, 1),
                                    on_press=instruction_click)

        self.add_widget(instruction_button)
        instruction_button.bind(on_press=instruction_click)

        load_button = Button(text=(str('Load CSV file and classify my records')),
                             font_size=20,
                             size_hint=(1.0, 0.2),
                             background_color=(0, 0, 0, 1),
                             on_press=self.button_click)
        self.add_widget(load_button)
        load_button.bind(on_press=self.button_click)

    def button_click(self, dummy):
        if self.label != "":
            self.remove_widget(self.label)

        path = filechooser.open_file(title="Pick a CSV file..",
                                     filters=[("Comma-separated Values", "*.csv")])
        if len(path) > 0:
            path = path[0]
            folder_path = path.split('\\')
            folder_path = '//'.join(folder_path[:-1])

            df=pd.read_csv(path, encoding='ISO-8859-1')
            col_names=df.columns

            # to check if list is subset of other
            # using all()

            # initializing list
            req_cols = ['TI', 'AB', 'KW', 'MH']

            # using all() to check if required columns are found
            flag = 0
            if all(x in col_names for x in req_cols):
                flag = 1
            if flag:
                lbl_text, saved_path = Classifier(path, working_dir=self.cwd, save_folder_path=folder_path)

                text_size = self.size
                self.label = Label(text=lbl_text,
                                   size_hint=(1.0, 1.0),
                                   pos_hint=(0.5, 0.5),
                                   markup=True,
                                   font_size='20sp')
                self.label.bind(size=self.label.setter('text_size'))
                self.add_widget(self.label)
                Clipboard.copy(saved_path)
            else:
                self.label = Label(text='[b][color=FF0000]The program failed to run because at least on required column is missing.[/b]\n\
Please ensure the following columns are present: TI, AB, KW, MH. See instructions above.[/color]', size_hint=(1.0, 1.0), pos_hint=(0.5, 0.5), markup=True)
                self.label.bind(size=self.label.setter('text_size'))
                self.add_widget(self.label)


class MLScreener(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.icon = 'mlscreener_icon.ico'
        return Root()


if __name__ == '__main__':
    MLScreener().run()
