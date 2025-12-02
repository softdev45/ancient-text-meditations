from func_tools import files_in
import json

class BibleJsonLoader():


	def __init__(self, directory):
		files = files_in(directory)
		self.content = {}
		for file in files:
			with open(file, 'r') as datafile:
				data = json.load(datafile)
				book_name = file.split('/')[-1].split('.')[0]
				self.content[book_name] = data



