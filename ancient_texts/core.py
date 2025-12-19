from ancient_texts.heb_char import h_new

chars = list(reversed(h_new[:-2]))

def get_translation(wordlist : list):
	result = []
	wordlist.reverse()
	for word in wordlist:
		for val,symbols in nav_symbols.items():
			if word in symbols:
				print(f'found {word} in {symbols}')
				result.append(val)
				break
	#translate to index_number to later get symbol-char
	keys = list(nav_symbols.keys())
	print(keys)
	result = list(map(lambda el: keys.index(el), result))
	print(result)
	result = list(map(lambda i_el: chars[i_el[1]][0] if
				 (print(i_el,chars[i_el[1]],len(chars[i_el[1]]),i_el[0] > 0 or len(chars[i_el[1]])==1) or True ) 
				 and (i_el[0] > 0  or len(chars[i_el[1]])==1)
				#  and (i_el[0]+1 < len(result) or len(chars[i_el[1]])<2)
				 else chars[i_el[1]][1], enumerate(result))) # add sofit for last letter
	# result = list(map(lambda i_el: chars[i_el[1]][0] if
	# 			 (print(i_el,chars[i_el[1]],len(chars[i_el[1]]),i_el[0]+1 < len(result)) or True ) 
	# 			 and (i_el[0]+1 < len(result) or len(chars[i_el[1]])<2)
	# 			#  and (i_el[0]+1 < len(result) or len(chars[i_el[1]])<2)
	# 			 else chars[i_el[1]][1], enumerate(result))) # add sofit for last letter
	result.reverse()
	print(result)
	result = ''.join(result)
	print(result)
	return result




#TODO viewing many meanings		

nav_symbols = {
	1:	['Leader', 'Love', 'Master', 'First', 'Strength'],
	2:	['Tent', 'House', 'Temple', 'Community', 'Inside', 'Heart'],
	3:	['Leg', 'Meditation', 'Prayer', 'Elavate', 'Rise'],
	4:	['Way', 'Door', 'Lower', 'Attitude' ],
	5:	['Word', 'Influence', 'Revelation', 'Human', 'Spirit'],
	6:	['Nail/Hook', 'Connection', 'Weakness', 'Join/Add'],
	7:	['Plough', 'Make Ready', 'Overturn', 'Sword', 'Tongue'],
	8:	['Wall', 'Separate', 'Protect', 'End' ],
	9:	['Basket', 'Container','Gather', 'Surround', 'Mistake', 'Recollection'],
	10:	['Hand', 'Complete', 'Work', 'Power'],
	20:	['Palms', 'Allow','Press', 'Tame', 'Activate' ],
	30:	['Staff', 'Control', 'Teach', 'Guide','Towards'],
	40:	['Water', 'Chaos', 'Massive', 'Nourishment', 'Cleansing'],
	50:	['Activity', 'Life', 'Continue', 'Seed', 'Sprout'],
	60:	['Support', 'Shield', 'Thorn' ],
	70:	['Knowledge','Experience','Eye', 'Fountain'],
	80:	['Opening', 'Mouth', 'Command'],
	90:	['Desire', 'Righteous', 'Need', 'Hunt', 'Rest'],
	100:	['Least', 'Sun', 'Revolutions', 'Light', 'Again', 'Repeat'],
	200:	['Head', 'Most High', 'Person'],
	300:	['Teeth', 'Consume', 'Destroy', 'Face', 'Peak'],
	400:	['Covenant', 'Seal', 'Mark', 'Last'],
	-1:	[''],
	-2:	[''],
	-3:	[''],
}



nav_symbols_2 = {
	1:	['Leader', 'Love', 'Master', 'First', 'Strength'],
	2:	['Tent', 'House', 'Temple', 'Community', 'Inside', 'Heart'], #dwelling, home
	3:	['Leg', 'Meditation', 'Prayer', 'Elavate', 'Rise'], # great, rise
	4:	['Way', 'Door', 'Lower', 'Truth'],
	5:	['Word', 'Influence', 'Revelation'],
	6:	['Nail/Hook', 'Connection', 'Weakness', 'Join/Add'],
	7:	['Plough', 'Make Ready', 'Overturn'],
	8:	['Wall', 'Separate', 'Protect' ],
	9:	['Basket', 'Container','Gather', 'Surround'],
	10:	['Hand', 'Complete', 'Work', 'Power'],
	20:	['Palms', 'Allow','Press', 'Tame'],
	30:	['Staff', 'Control', 'Teach', 'Guide','Towards'],
	40:	['Water', 'Chaos', 'Massive', 'Nourishment', 'Cleansing'],
	50:	['Activity', 'Life', 'Continue'],
	60:	['Support', 'Shield', 'Thorn' ],
	70:	['Knowledge','Experience','Eye', 'Fountain'],
	80:	['Opening', 'Mouth', 'Command'],
	90:	['Desire', 'Righteous', 'Need', 'Hunt'],
	100:	['Least', 'Sun', 'Revolutions', 'Light'],
	200:	['Head', 'Most High'],
	300:	['Teeth', 'Consume', 'Destroy', 'Face', 'Peak'],
	400:	['Covenant', 'Seal', 'Mark', 'Last'],
	-1:	[''],
	-2:	[''],
	-3:	[''],
}

def get_nav_data():
	return nav_symbols
