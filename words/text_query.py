from words.word import Word
import Levenshtein as L
#from thefuzz import fuzz
import pylcs


def verse_query(ref: str):
	result = []
	loc = list(map(lambda el: int(el), ref.split(',')[1:]))
	result = list(filter(lambda el: loc[0]==el.book and loc[1]==el.chapter and loc[2] == el.verse, Word.db))
	result = list(map(lambda wrd: wrd.get_data(), result))
	return result

def word_query(word: str):
	result = []
	#TODO test for 6 3 5 (conn leg revel) somewhat-FIXED 
	# if word in Word.word_agreg:
	# 	print('found in word_agreg - slicing max 3')
	# 	result.append((None, Word.word_agreg[word][0:3], word)) # 3 words from the list
	# 	#TODO filter results (compact)
	# elif word in Word.root_agreg:
	# 	print('found in root_agreg - slicing max 3')
	# 	result.append((None, Word.root_agreg[word][0:3], word)) # 3 words from the list

	

	if False:
		# set-based comparsion (number of similar characters in a word)
		print('seeking with method set-wise')
		found = list(reversed(sorted([(len(set(word) & set(key)),val,key) for key,val in Word.word_agreg.items() ], key=lambda el:el[0])))
		max_len,_1,_2 = found[0]
		found = [el for el in found if el[0] == max_len and len(el[1])>0 ]
		found = list(reversed(sorted([(pylcs.lcs_sequence_length(word,key),val,key) for (_score,val,key) in found ], key=lambda el:el[0])))
		max_len,_1,_2 = found[0]
		found = [el for el in found if el[0] == max_len and len(el[1])>0 ]
		result.extend(found)


	if len(result) < 5 or True:
		print('browsing in root_agreg - slicing closest')
		import time
		# st = time.time()
		words_aggreg = list(Word.word_agreg.items())+list(Word.root_agreg.items())
		# print(time.time() - st)
		# words_aggreg = list(Word.word_agreg.items())+list(Word.root_agreg.items())
		# print(time.time() - st)

		sub_string_result = []
		found = list(reversed(sorted([(pylcs.lcs_string_length(word,key),val,key) for key,val in words_aggreg ], key=lambda el:el[0])))
		max_len,_1,_2 = found[0]
		found = [el for el in found if el[0] == max_len and len(el[1])>0 ]
		max_len_str = max_len
		print('string', found)
		# try browsing with longest common sequence
		found = list(reversed(sorted([(pylcs.lcs_sequence_length(word,key),val,key) for key,val in words_aggreg ], key=lambda el:el[0])))
		max_len,_1,_2 = found[0]
		if not max_len > max_len_str: 
			result.extend(sub_string_result) #add prev results if subseq is not longer (L-Q word formation)
		print(max_len)
		if max_len >= len(word)-2:
			found = [el for el in found if el[0] == max_len and len(el[1])>0 ]
			print('subseq', found)
			result.extend(found)
	

		# add first non empty result
		# first_none_empty = 0
		# try:
		# 	while not len(curr := Word.word_agreg[found[first_none_empty][2]]):
		# 		first_none_empty += 1
		# 	result.append(curr[0])
		# except :
		# 	import traceback
		# 	traceback.print_exc()
	return result
