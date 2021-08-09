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
Builder.load_file('{}\\GUI.kv'.format(
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

class LabelInfo(Label):
	pass


class MyApp(App):
	def __init__(self):
		super().__init__()
		self.output = TextOutput()
		self.page_input = IntInput() #focus=True
		self.info = LabelInfo(markup=True)

	def build(self):
		main_case = MainCase()
		second_case = SecondCase()
		bottom_half_of_the_second_container = BottomHalfOfTheSecondContainer()
		btn__and__input_pages = ButtonAndPagesInput()
		button = ButtonShare(on_press = self.btn_press)

		second_case.add_widget(self.output)
		second_case.add_widget(bottom_half_of_the_second_container)

		btn__and__input_pages.add_widget(self.info)
		btn__and__input_pages.add_widget(self.page_input)
		btn__and__input_pages.add_widget(button)

		bottom_half_of_the_second_container.add_widget(btn__and__input_pages)

		main_case.add_widget(second_case)

		return main_case

	def datatype_ghost(self, data:str)->int:
		if data.isdecimal():
			return int(data)
		raise AttributeError(f'AttributeError. Вы ввели некоректное значение. Повторите ввод!!!')

	def clear(self):
		self.output.text = ''

	def add_text(self, string='', font_size=20):
		self.output.font_size = font_size
		self.output.text += string

	def label_text(self, text, colour='2c3e50'):
		if '#' in colour:
			colour = colour.split('#')[-1]
		self.info.text = f'[color={colour}]{text}[/color]'

	def data(self):
		try:
			data = self.datatype_ghost(self.page_input.text)
			self.request = Backand(data)
			avers, revers = self.request.response()
			return avers, revers
		except AttributeError as err:
			return None, err

	def data_output(self):
		avers, revers = self.data()
		if avers == None:
			self.label_text(revers, colour='EA2027'); 
			self.clear(); return
		item = lambda _list, index: ','.join((str(i) for i in _list[int(index)]))
		self.clear()
		info = self.request.info()
		text = f'[b]Для печати потребуется листов А4[/b]: [u]{info["page_A4"]}[/u]\n[b]Печать документа объемом[/b]: [u]{info["all_pages"]}[/u] [b]страниц[/b]'
		self.label_text(text, colour='44bd32')
		for i in range(len(avers)):
			result = f'\n{"="*25} Лист {i+1} {"="*25}\n Аверс: {item(avers, i)}\n Реверс: {item(revers, i)}\n'
			self.add_text(result, font_size=FONT_SIZE_OUTPUT)

	def btn_press(self, instance):
		self.data_output()

if __name__ == '__main__':
	MyApp().run()
