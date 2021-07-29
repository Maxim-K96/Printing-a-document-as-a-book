#!/usr/bin/env python3.9

import re

PAGES_ON_A4_SHEET = 4

class Page:
	def __init__(self, pages_in_a_book:int):
		self.pages_in_a_book = int(pages_in_a_book)
		if self.validation(self.pages_in_a_book):
			raise AttributeError(f'Количество страниц ({self.pages_in_a_book}) не кратно 4-м... ')

	def __str__(self):
		avers, revers = self.response()
#		pages = lambda _list: list(map(lambda i: i, _list))
		item = lambda _list, index: ','.join((str(i) for i in _list[int(index)]))
		def pages(_list_1:list, _list_2:list)->str:
			result = ''
			for i in range(len(_list_1)):
				result += f'Лист {i+1}\n Аверс: {item(_list_1, i)}\n Реверс: {item(_list_2, i)}\n{"="*60}\n'
			return result

		return f'{pages(avers, revers)}'

	def formation_of_notebook(self):
		all_pages_in_book = [i for i in range(self.pages_in_a_book+1)]
		pages_in_notebook = [i for i in all_pages_in_book[::40]]
		pages_in_notebook.append(all_pages_in_book[-1])
		index_start = 1
		for index_end in pages_in_notebook:
			notebook = all_pages_in_book[index_start:int(index_end)+1]
			index_start = index_end+1
			yield notebook

	def iterating_through_the_sheets(self):
		for list_pages in self.formation_of_notebook():
			if len(list_pages) != 0:
				list_pages.insert(0,0)
				yield list_pages

	def front_or_rear(self, additional_sheet=0):
		for front_or_rear in self.iterating_through_the_sheets():
			for i in range((len(front_or_rear)//2)+additional_sheet):
				if additional_sheet == 0:
					if i%2!=0:
						yield front_or_rear[-i], front_or_rear[i]
				else:
					if i%2==0:
						yield front_or_rear[i], front_or_rear[-i]

	def removing_zeros(self, elem):
		return elem >= 1

	def _iter_list(self, _list, index):
		item = _list[:int(index)]
		del _list[:int(index)]
		return item

	def separator_pages(self, list_pages:list)->list:
		number_of_sheets = ((len(list_pages)//10)//2)+1
		for i in range(number_of_sheets):
			if len(list_pages) >= 20:
				yield self._iter_list(list_pages, 20)
			else:
				yield self._iter_list(list_pages, len(list_pages))

	def response(self):
		list_page_front = list(self.page_iterator(tuple(self.front_or_rear())))
		list_page_rear = list(filter(self.removing_zeros,list(self.page_iterator(tuple(self.front_or_rear(1))))))

		front = tuple(self.separator_pages(list_page_front))
		rear = tuple(self.separator_pages(list_page_rear))

		return front, rear

	def page_iterator(self, list_of_all_pages:tuple)->int:
		for page_list_separator in list_of_all_pages:
			for page in page_list_separator:
				yield page

	def validation(self, pages_in_a_book:int)->bool:
		valid = False if pages_in_a_book % PAGES_ON_A4_SHEET==0 else True
		return valid

if __name__ == '__main__':
	pages = Page(260)
	print(pages)

