import yaml

def deaccentize(text):
	accents = '̥́̀̄̆̏̑'
	accented = {'ȁȃáàā': 'a', 'ȅȇéèē': 'e', 'ȉȋíìī': 'i',
				'ȕȗúùū': 'u', 'ȑȓŕ': 'r', 'ȀȂÁÀĀ': 'A',
				'ȄȆÉÈĒ': 'E', 'ȈȊÍÌĪ': 'I',	'ȔȖÚÙŪ': 'U',
				'ȐȒŔ': 'R', 'ӣѝ': 'и', 'ѐ': 'е',
				'ӢЍ': 'И', 'Ѐ': 'Е'}
	for accent in accents:
		text = text.replace(accent, '')
	for letters in accented:
		for letter in letters:
			text = text.replace(letter, accented[letters])
	
	return text

def decypher(sequence):
	import re
	
	if sequence:
		begin_R = re.search('@', sequence).start(0) if '@' in sequence else None
		begin_AP = re.search('[A-Z]', sequence).start(0)
		begin_MP = re.search('[a-z]', sequence).start(0)
		line_accents = sequence[:begin_R] if '@' in sequence else sequence[:begin_AP]
		Rs = sequence[begin_R:begin_AP] if '@' in sequence else None
		accents = {}
		accents['r'] = {int(i): '̥' for i in Rs[1:].split(',')} if Rs else {}
		accents['v'] = {int(i[:-1]): i[-1] for i in line_accents.split(',')} if line_accents else {}
		AP = sequence[begin_AP:begin_MP]
		MP = sequence[begin_MP:]
	else: accents, AP, MP = ({'v': {}, 'r': {}}, {}, {})

	return {'accents': accents, 'AP': AP, 'MP': MP}	
		
def insert_(word, dict_):
	list_ = sorted(list(dict_.keys()))
	first = [0] + list_
	second = list_ + [None] 
	pieces = [word[first[0]:second[0]]]
	for y in range(1, len(first)):
		pieces.append(dict_[list_[y-1]])
		pieces.append(word[first[y]:second[y]])
	newword = ''.join(pieces)
	
	return(newword)
	
def accentize(word, sequence):
	real_accent = {'`': '̀', '´': '́', '¨': '̏', '^': '̑', '_': '̄'}
	acc_list = decypher(sequence)['accents'] # we got list of accents!
	if acc_list['v']:
		if acc_list['r']: # now we put the magic ring
			word = insert_(word, acc_list['r'])
		# after that we create a list with letter numbers representing vowels
		syllabic = 0
		vow_dict = {}
		for i, c in enumerate(word):
			if c in 'aeiouAEIOUаеиоуАЕИОУ̥':
				syllabic += 1
				if syllabic in acc_list['v']:
					vow_dict[i+1] =  real_accent[acc_list['v'][syllabic]]
		newword = insert_(word, vow_dict) # then we insert accents into word!
	else:
		newword = word
	return newword
	
	
		
sr = yaml.load(open('a_sr_ru.yaml', encoding="utf-8"))

#print(type(sr['letter_a'][0]))

from random import choice
for i in range(0, 10):
	ourword = choice(list(sr['letter_a'][0].keys()))
	print('{:^50}'.format(str(ourword) + ' : ' + accentize(ourword, sr['letter_a'][0][ourword].get('i', ''))))