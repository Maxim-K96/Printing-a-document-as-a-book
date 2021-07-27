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
#from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config

from kivy.core.window import Window

root = os.path.split(__file__)[0]
Builder.load_file('{}/GUI.kv'.format(
	root if root != '' else os.getcwd())
)

# Глобальные настройки
WIDTH = 750
HEIGHT = 600
Config.set('graphics', 'resizeble', 0)
Config.set('graphics', 'width', WIDTH)
Config.set('graphics', 'height', HEIGHT)
Window.clearcolor = (32/255, 33/255, 36/255, 1)
Window.title = "Печать страниц"

class IntInput(TextInput):
	pat = re.compile('[^0-9]')
	def insert_text(self, substring, from_undo=False):
		pat = self.pat
		if pat.search(self.text):
			s = re.sub(pat, '', substring)
		else:
			s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])

		return super(IntInput, self).insert_text(s, from_undo=from_undo)

class DataPages(Page):
	def __init__(self, pages):
		Page.__init__(self, pages)
		self.pages = pages


class MyButton(Button):
	pass

class MainWindow(BoxLayout):
	pass

class Bottom_pos(AnchorLayout):
	pass
#class MyLabel(Label):
#	pass


class MyApp(App):
	# Создание всех виджетов (объектов)
	def __init__(self):
		super().__init__()
		self.label = IntInput(size_hint = (1, .9), auto_indent=True)
		self.text_input = IntInput(size_hint = (.03, .05), font_size=20)
		self.button = MyButton(on_press = self.btn_press)

	def build(self):
		al = AnchorLayout()
		layout = MainWindow()
		gl = GridLayout(cols=2, spacing=4, size_hint=(.5, 1), padding=4)
		layout.add_widget(self.label)
		al_2 = AnchorLayout(anchor_x='right', anchor_y='bottom', size_hint=(1, .1))
		gl.add_widget(self.text_input)
		gl.add_widget(self.button)
		al_2.add_widget(gl)
		layout.add_widget(al_2)
		al.add_widget(layout)

		return al

	def type_cast(self, obj):
		if obj.isdecimal() == True:
			return int(obj)
		elif obj.isalnum() == False:
			print('Error. Вы не ввели никакого значения. Повторите ввод!!!')
			return False
		else:
			print('Error. Вы ввели некоректное значение. Повторите ввод!!!')
			return False

	def add_text(self, string:str, clear=False, font_size=20):
		if clear == True:
			self.label.text = ''
		self.label.font_size = font_size
		self.label.text += string

	def btn_press(self, instance):
		try:
			valid = self.type_cast(self.text_input.text)
			if valid == False:
				self.add_text('Error. Вы ввели некоректное значение. Повторите ввод!!!', clear=True)
#				valid = self.type_cast(self.text_input.text)
			pages = DataPages(valid)
			avers, revers = pages.list_of_print()
			item = lambda _list, index: ','.join((str(i) for i in _list[int(index)]))
			self.add_text('', clear=True)
			for i in range(len(avers)):
				self.add_text(f'Лист {i+1}\n Аверс: {item(avers, i)}\n Реверс: {item(revers, i)}\n{"="*60}\n', font_size=14)
		except AttributeError:
			self.label.color = [.90, .48, .49]
			self.label.text = f'Error. Количество страниц ({self.text_input.text}) не кратно 4-м...'


if __name__ == '__main__':
	MyApp().run()
