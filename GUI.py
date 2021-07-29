#!/usr/bin/env python3.9

import re
import os
from pages_print import Page
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
from kivy.config import Config

from kivy.core.window import Window

root = os.path.split(__file__)[0]
Builder.load_file('{}/GUI.kv'.format(
	root if root != '' else os.getcwd())
)

# Глобальные настройки
WIDTH = 750
HEIGHT = 600
FONT_SIZE_OUTPUT = 14
FONT_SIZE_ERROR = 16

#Config.set('kivy','window_icon','sivaicon.png')
#Config.set('graphics', 'resizable', True)

Config.set('graphics', 'resizeble', 0)
Config.set('graphics', 'width', WIDTH)
Config.set('graphics', 'height', HEIGHT)
Window.clearcolor = (32/255, 33/255, 36/255, 1)
Window.title = 'Печать страниц'

class IntInput(TextInput):
	not_numbers = '[^0-9]'
	pat = re.compile(not_numbers)
	def insert_text(self, substring, from_undo=False):
		pat = self.pat
		if pat.search(self.text):
			s = re.sub(pat, '', substring)
		else:
			s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])

		return super(IntInput, self).insert_text(s, from_undo=from_undo)

class Backand(Page):
	def __init__(self, pages):
		Page.__init__(self, pages)
		self.pages = pages

class TextOutput(TextInput):
	all_characters = '[\\w+\\s=~|`''""/\\.,)(\\][\\{\\}*^&\\-!\\\\@#$:;?%]'
	pat = re.compile(all_characters)
	def insert_text(self, substring, from_undo=False):
		s = re.sub(self.pat, '', substring)
		return super(TextOutput, self).insert_text(s, from_undo=from_undo)

class MainCase(AnchorLayout):
	pass

class ButtonShare(Button):
	pass

class SecondCase(BoxLayout):
	pass

class ButtonAndPagesInput(GridLayout):
	pass

class BottomHalfOfTheSecondContainer(AnchorLayout):
	pass

class MyApp(App):
	def __init__(self):
		super().__init__()
		self.output = TextOutput()
		self.page_input = IntInput() #focus=True
		self.button = ButtonShare(on_press = self.btn_press)

	def build(self):
		main_case = MainCase()
		second_case = SecondCase()
		bottom_half_of_the_second_container = BottomHalfOfTheSecondContainer()
		btn__and__input_pages = ButtonAndPagesInput()

		second_case.add_widget(self.output)
		second_case.add_widget(bottom_half_of_the_second_container)

		btn__and__input_pages.add_widget(self.page_input)
		btn__and__input_pages.add_widget(self.button)

		bottom_half_of_the_second_container.add_widget(btn__and__input_pages)

		main_case.add_widget(second_case)

		return main_case

	def datatype_ghost(self, data:str)->int:
		if data.isdecimal():
			return int(data)
		raise AttributeError(f'AttributeError. Вы ввели некоректное значение. Повторите ввод!!!')

	def add_text(self, string:str, clear_window=False, font_size=20):
		if clear_window:
			self.output.text = ''
		self.output.font_size = font_size
		self.output.text += string

	def data_output(self):
		try:
			data = self.datatype_ghost(self.page_input.text)
			request = Backand(data)
			avers, revers = request.response()
			item = lambda _list, index: ','.join((str(i) for i in _list[int(index)]))
			self.add_text('', clear_window=True)
			for i in range(len(avers)):
				result = f'\n{"="*25} Лист {i+1} {"="*25}\n Аверс: {item(avers, i)}\n Реверс: {item(revers, i)}\n'
				self.add_text(result, font_size=FONT_SIZE_OUTPUT)
		except AttributeError as err:
			message_error = f'AttributeError {err}'
			self.add_text(message_error, clear_window=True, font_size=FONT_SIZE_ERROR)

	def btn_press(self, instance):
		self.data_output()

if __name__ == '__main__':
	MyApp().run()
