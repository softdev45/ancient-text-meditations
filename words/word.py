from ancient_texts.helper_tools import only_letters, calc_word_count, load_new
from tools.func_tools import gen_book_map

# import main2 as main
import re
import prettytable

from consolemenu import *
from consolemenu.items import *

import Levenshtein

BM = gen_book_map()

class Word:

    db = []
    objects = []
    root_agreg = {}
    word_agreg = {}
    test = ['2', '〔1｜1｜1｜1〕', 'רֵאשִׁ֖ית', 'rēšît', 'rēšˌîṯ', 'רֵאשִׁית', 'E70002', 'H7225', 'subs.f.sg.a', 'noun, feminine, singular, absolute', 'beginning', '〔2＠the beginning〕']
    wrd_loc = {}
    rt_loc = {}

    def __init__(self, data, index=None):
        if not index:
            index = len(Word.objects)
        self.index=index
        Word.objects.append(self)

        self.data = data
        #self.word = only_letters(data[2])
        self.word = data[2]
        self.word_decorated = data[2]
        self.pronounce = data[3:5]
        self.root = data[5]
        self.grammar = data[-3]
        self.grammar_short = data[8]
        self.en = data[-2]
        self.ctx_en = data[-1]

        root_ag = Word.root_agreg.get(self.root, [])
        root_ag.append(self)
        Word.root_agreg[self.root] = root_ag
        
        word_ag = Word.word_agreg.get(self.word, [])
        word_ag.append(self)
        Word.word_agreg[self.word] = word_ag

        pos = re.findall(r'[\d]+',data[1].strip())
        self.verse_total = pos[0]
        self.book = int(pos[1])
        self.chapter = int(pos[2])
        self.verse = int(pos[3])
        self.book_name = BM[self.book]

        # ^object's fields were set^

        wrd_loc = Word.wrd_loc.get(self.word, [])
        wrd_loc.append(self.get_location())
        Word.wrd_loc[self.word] = wrd_loc

        rt_loc = Word.rt_loc.get(self.root, [])
        rt_loc.append(self.get_location())
        Word.rt_loc[self.root] = rt_loc

    def get_location(self, book_name=False):
        loc = (self.book,self.chapter,self.verse)
        if book_name:
            #TODO use field
            loc = (BM[self.book],) + loc
        return  loc

    def get_verse_words(self):
        result = []
        db = Word.db
        num = self.index

        cur = num - 1
        while db[cur].verse_total == db[num].verse_total:
            result.insert(0, db[cur])
            cur -= 1
        cur = num
        #print(len(db),' #dblen ')
        #print(num,cur,' #num,curr ')
        # ISSUE REG: indexError search on YHWH<hbr>
        while db[cur].verse_total == db[num].verse_total:
            result.append(db[cur])
            cur += 1
        return result
        
    #get verse of given word: words before and after given word
    def get_verse(self, which='ctx'):
        result = self.get_verse_words()
        result_h = list(map(lambda w: w.word, result))
        result_e = list(map(lambda w: w.en, result))
        result_ctx = list(map(lambda w: w.ctx_en, result))
        if which == 'ctx':
            return ' '.join(result_ctx)
        merged =  ' '.join(result_h) +' <=> '+ ' '.join(result_e)+' <=> '+ ' '.join(result_ctx)
        return merged.replace('[object marker]', '->')
    
    def get_next_loc(self):
        index = Word.wrd_loc[self.word].index(self.get_location())
        if index + 1 < len(Word.wrd_loc[self.word]):
            return Word.wrd_loc[self.word][index+1]
        else:
            return '<l.o.>'

    def get_data_row(self):
        return self

    def get_data(self):
        return [f'[{self.root}]',
                self.word,
                self.en,
                self.ctx_en,
                self.pronounce,
                self.get_location(book_name=True),
                # len(Word.rt_loc[self.root]),
                # len(Word.wrd_loc[self.word])
                ]

    def __str__(self):
        return f'{self.root}\t\t{self.word}\t\t{self.en}\t\t{self.ctx_en}\t\t{self.book}:{self.chapter}:{self.verse}\t\t{len(Word.wrd_loc[self.word])}\t\t{len(Word.rt_loc[self.root])} {self.get_next_loc()}\t\t\t{self.pronounce}'
    
    def __repr__(self):
        return f'({self.word})[{self.root}]({self.en}/{self.ctx_en})@{self.get_location()}'

    def repr2(self):
        return f"({self.word}/{self.root})/[{self.ctx_en}/{self.en}]"


def get_random_word():
    pass


def print_rows(rows):
    if len(rows)>0 and type(rows[0]) is Word:
        rows = list(map(lambda w: w.get_data_row(), rows))
    #TODO(ref) skip same words/roots in same chapters
    for i,r in enumerate(rows[1:]):
        if (r.root == rows[i-1].root or r.word == rows[i-1].word )and r.book == rows[i-1].book and r.chapter ==rows[i-1].chapter:
            r.marked_hidden = True
    p = prettytable.PrettyTable()
    p.border = False
    p.header = False
    p.align = 'r'
    #print(len(rows))
    frows = [row.get_data() for row in rows if not hasattr(row,'marked_hidden') or not row.marked_hidden ]
    p.add_rows(frows)
    print(p)
    print(len(frows))
    print(len(rows))


def load(dbfile = './words/new2_db_100k.csv'):
# def load(dbfile = './words/new2_db.csv'):
    # import traceback
    # traceback.print_stack()
    #global db
    if not Word.db:
        wdb = load_new(dbfile)
        # wdb = main.load_new('./new2_db.csv')
        db = list(map(lambda w: Word(w), wdb))
        Word.db = db

        print_rows(db[:10]) 
    #for w in db[:10]:
    #    print(w)

def wcount():
    wl = list(map(lambda w: f'[{w.root}]', Word.db))
    wc = calc_word_count(wl)
    wcs = sorted(wc.items(), key= lambda i: i[1])
    return wcs

def usage(l='ג'):
    i=Word.root_agreg.items()
    j=sorted(i, key=lambda el: len(el[1]))
    f = list(filter(lambda el: l in el[0], j))
    o = [ (len(el[1]), el[1][0].en, f" {el[0]} ") for el in f ]
    return o


def program():
    #global db
    db = Word.db
    wrd = None
    while True:
        wrd = input()
        if wrd == '0' or not wrd:
            return
        
        if wrd[0] == '^':
            print(wrd[1:])
            r = filter(lambda w: w.word.startswith(wrd[1:]), db)
        elif wrd[0] == '!':
            print(wrd[1:])
            r = filter(lambda w: w.word == wrd[1:] or w.root == wrd[1:], db)
        elif wrd[0] == '$':
            r = filter(lambda w: w.word.endswith(wrd[1:]), db)
        elif wrd[0] == ':':
            cmd = wrd[1:].split(':')
            cmd = tuple(map(int,cmd))
            print(cmd)
            r = filter(lambda w: (cmd[0],cmd[1],cmd[2]) == (w.book,w.chapter,w.verse), db)
        elif wrd[0] == '&':
            r = filter(lambda w: wrd[1:] in w.root, db)
        else:
            r = filter(lambda w: wrd in w.word or wrd in w.root or wrd in w.en, db)
        #r = filter(lambda w: 'verb' in w.type, r)
        #r = filter(lambda w: 'piel' in w.gram, r)
        r = list(r)
        print('found: ', len(r))
        tb = []
        for e in r:
            tb.append(e.get_data_row())
            #print(e)
        print_rows(tb)

            

        #menu = ConsoleMenu()
        #for i in r:
            #f= FunctionItem(f'{i.word}', lambda x: print(x), [i.word])
            #menu.append_item(f)
        #menu.show()


if __name__ == 'words.word':
    #start()
    # import pathlib
    # script_dir = pathlib.Path(__file__).parent.resolve()
    # print(script_dir)
    if not Word.db:
        print('loading words')
        load()
        print('loaded words')

def start():
    if not Word.db:
        load()
    #print(list(Word.word_locations.items())[:20])
    program()

if __name__ == '__main__':
    print('running main procedure')
    #a = Word.test[-1][1:-1]
    #ctx_en = re.findall(r'([a-zA-Z0-9,\.;: \w.]*)',a)
    #print(ctx_en)
    #load()
    #program()
    #load()
    start()

print(__name__)
