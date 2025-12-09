from func_tools import files_in
from dataclasses import dataclass
from json import load as json_load
import itertools
from typing import List



@dataclass
class Scroll:
    bookname: str
    filepart: int
    content: dict
    chapter: int = None


@dataclass
class Logos:
    greek: str
    eng: str
    transliter: str
    punct: str
    grammar: str
    strongs_num: str
    

@dataclass
class Library:
    scrolls: List[Scroll]

    # def get(book, chapter, verse):

    def search(self, phrase: str):
        result = []
        for scroll in self.scrolls:
            for verse in scroll.content:
                for word in verse:
                    if phrase in word.eng:
                        result.append(verse)
                        break
        return result[:3]



def build_books_lib(book_dir='./greek_nt_json'):
    files = files_in(book_dir)
    files = list(itertools.chain.from_iterable(files))

    scrolls = []

    for filename in filter(lambda f: f.endswith('json'), files):
        extension_pos = filename.rfind('.')
        name_parts = filename[:extension_pos].split('/')
        part = int(name_parts[-1])
        book_name = name_parts[-2]

        with open(filename, 'r') as fp:
            content = json_load(fp)

        scroll = Scroll(book_name, part, content)
        scroll = process_raw_content(scroll)
        scrolls.append(scroll)

    return Library(scrolls)


# list(map(lambda w: list(map(lambda v: v['en'], w)), b[0].content['verses'].values()))

def process_raw_content(scroll: Scroll):
    scroll.chapter = int(scroll.content['chapter'])
    verses = list(scroll.content['verses'].values())
    # print(verses)
    for i in range(0, len(verses)):
        verse = list(
            map(
                lambda wrd: Logos(
                    wrd['gr'], wrd['en'], wrd['tl'], wrd['pu'], wrd['pa'], wrd['st']
                ),
                verses[i]
            )
        )
        verses[i] = verse
    scroll.content = verses
    return scroll
