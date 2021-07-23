#!/usr/bin/env python3.9

class Page:
	def __init__(self, pages:int):
		self.pages = int(pages)
		self.pages_of_sheet_A4 = 4
		if self.valid(self.pages) == False:
			raise AttributeError(f'Количество страниц ({self.pages}) не кратно 4-м... ')

	def __str__(self):
		avers, revers = self.list_of_print()
#		pages = lambda _list: list(map(lambda i: i, _list))
		item = lambda _list, index: ','.join((str(i) for i in _list[int(index)]))
		def pages(_list):
			result = ''
			for i in range(len(_list)):
				result += f'{i+1}) {item(_list, i)}\n'
			return result

		return f'avers\n{pages(avers)}\n{"="*20}\n revers\n{pages(revers)}'

	def list_pages_of_print(self):
		pages = [i for i in range(self.pages+1)]
		notebook = [i for i in pages[::40]]
		notebook.append(pages[-1])
		items = 1
		for i in notebook:
			item = pages[items:int(i)+1]
			items = i+1
			yield item

	def page_list_one(self):
		for list_pages in self.list_pages_of_print():
			list_pages.insert(0,0)
			for i in range((len(list_pages)//2)):
				if i%2!=0:
					yield list_pages[-i], list_pages[i]

	def page_list_two(self):
		for list_pages in self.list_pages_of_print():
			list_pages.insert(0,0)
			for i in range((len(list_pages)//2)+1):
				if i%2==0:
					yield list_pages[i], list_pages[-i]

	def func(self, elem):
		return elem >= 1

	def separator_pages(self, list_pages):
		for i in range(((len(list_pages)//10)//2)+1):
			if len(list_pages) >= 20:
				yield list_pages[:20]
				del list_pages[:20]
			else:
				yield list_pages[:len(list_pages)]
				del list_pages[:len(list_pages)]

	def list_of_print(self):
		list_1_print = list(self.iter(tuple(self.page_list_one())))
		list_2_print = list(filter(self.func,list(self.iter(tuple(self.page_list_two())))))

		list_1 = tuple(self.separator_pages(list_1_print))
		list_2 = tuple(self.separator_pages(list_2_print))

		return list_1, list_2

	def iter(self, list_):
		for i in list_:
			for j in i:
				yield j

	def data(self):
		pages_one_notebook = self.pages_of_sheet_A4*10
		data_set = {
			'pages_one_notebook': pages_one_notebook, # Количество страниц в одной тетради
			'pagesA4': self.pages//self.pages_of_sheet_A4, # Количество листов А4
			'count_notebooks_in_book':self.pages/pages_one_notebook # Количество тетрадей в книге
			}
		return data_set

	def valid(self, pages):
		valid = True if pages%self.pages_of_sheet_A4==0 else False
		return valid

if __name__ == '__main__':
	pages = Page(460)
	print(pages)
#	avers, revers = pages.list_of_print()
#	def iter(item):
#		for i in item:
#			print(i)
#	iter(avers)
#	print('='*60)
#	iter(revers)
