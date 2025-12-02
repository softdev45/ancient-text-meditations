import csv
import re 

#scripts to process bible text csv; extract from <heb> tags

HA="""אבגדהוזחטיךכלםמןנסעףפץצקרשת"""

H_RANGE = range(ord(HA[0]),ord(HA[-1])+1)

def only_letters(word):
    return ''.join([l for l in word \
            if ord(l) in H_RANGE])

def calc_word_count(word_list):
    result = dict()
    for word in word_list:
        result[word] = result.get(word,0)+1
    return result


# playground
# start
#  

db = []
wd = []

def extr(s):
    print(s)
    r = re.findall(r'<heb>(.*)</heb><heb>', s)
    return r[0]

def db_get_str(i):
    return f'{only_letters(db[i][2])} [{db[i][5]}]: {db[i][-2]}{db[i][-1]} {db[i][3:5]}{db[i][1]}'


def get_similar(word):
    result = set()
    for i,w in enumerate(wd):
        if w == word:
            result.add(db_get_str(i))
    return result

def get_prefixed(prefix):
    result = set()
    for i,w in enumerate(wd):
        if w.startswith(prefix):
            result.add(db_get_str(i))
    return result

def get_suffixed(prefix):
    result = set()
    for i,w in enumerate(wd):
        if w.endswith(prefix):
            result.add(db_get_str(i))
    return result

def get_with_substr(prefix):
    result = set()
    for i,w in enumerate(wd):
        if prefix in w:
            result.add(db_get_str(i))
    return result
    
def select():
    result = set()
    for i,w in enumerate(wd):
        if w.startswith('ת') and only_letters(db[i][5]).startswith('נ'):
            result.add(db_get_str(i))
    return result

#END PLAYground

def load_from_file():
    # global db
    db = []
    with open('./h.csv', 'r') as file:
        f = csv.reader(file, delimiter='\t')
        verses = list(f)[1:]
        for elem in verses:
            r2_occur = re.findall(r'<heb>(.*)</heb><heb>', elem[2]) #in text occurence
            r5_root = re.findall(r'<heb>(.*)</heb>', elem[5]) #root
            bare_occurance = only_letters(r2_occur[0]) # skip vowel points (hebrew)
            #if bare == '':
            #    print (elem)
            wd.append(bare_occurance)
            elem[2] = only_letters(r2_occur[0]) #extract hebrew word from within <heb> tag
            elem[5] = only_letters(r5_root[0]) #extract hebrew root from within <heb> tag
            AT = '＠'
            if AT in elem[-1]:
                last_column = elem[-1]
                elem[-1] = last_column[last_column.index(AT)+1:-1]
                #elem[-1] = re.findall(r'([a-zA-Z0-9\"\'\,\.;: \w.\[\]\-]*)',elem[-1])
            db.append(elem)
    return db

def save_to_file(db):
    # global db
    with open('./new2_db.csv', 'w') as outfile:
            w = csv.writer(outfile, delimiter='\t')
            for v in db:
                w.writerow(v)

def load_new(dbfile = './new2_db.csv'):
    #global db
    db = []
    with open(dbfile, 'r') as file:
        f = csv.reader(file, delimiter='\t')
        verses = list(f)
        for elem in verses:
            db.append(elem)
    return db
        
    #wc = calc_word_count(wd)
    #wcs = sorted(list(wc.items()), key=lambda x: x[1])


def most_frequent_words():
    for w in wcs[-20:-10]:
        import numpy as np
        print(w)
        w = w[0]
        wrd = np.array(db[wd.index(w)])
        wrd = wrd[[2,10]]
        print(f'{w} {wrd}')


def sketch_1():
    with open('./he8i_sm.csv', 'r') as file:
        f = csv.reader(file, delimiter='\t')
        l = list(f)
        r = re.findall(r'<heb>(.*)</heb><heb>', t[2])
        print('result')
        print(only_letters(r[0]))
        for e in r:
            print(e)
            for el in e:
                print(f'\t{el}')

        a = 'א'
        sh = 'ש'
        # print(a, ord(a))# ל a
        # print('----')
        # for e in t:
        # 	print(e,ord(e))

    # for i in range(ord(a)-20,ord(sh)+2):
    # 	print(f'{i} {chr(i)}')




