from lxml import etree
import re
from dataclasses import dataclass
#import numpy as np

word = 'earth'
xpath_expression = f".//seg[contains(text(),'{word}')]"  #[not(contains(@id, '{ref}'))]"

@dataclass
class Verse:
    text: str
    book: str
    chapter: int
    verse: int

def setup():


    verses_list = ['']
    import time
    #tree = etree.parse('../bible/shelf/bible2.xml')
    tree = etree.parse('./bible_en.xml')
    st = time.time()
    verses_list = tree.xpath('//seg')
    print('all verses in: ', time.time() - st)

    print(len(verses_list))
    print(verses_list[0].text)
    print(verses_list[0].attrib)
    ptrn = re.compile(r"God")
    rr = ptrn.search(verses_list[0].text, re.IGNORECASE)
    print(rr)
    '''
    print(verses_list[0].getparent().attrib)
    print(verses_list[0].getparent().getparent().attrib)
    '''

    return tree,verses_list

def test_xpath_search(tree):
    for x in range(0,100):
        b = tree.xpath(xpath_expression)
    print(len(b))

def test_list_search(verses):
    ptrn = re.compile(rf"{word}")
    for x in range(0,100):
        b = [ v.text for v in verses if ptrn.search(v.text, re.IGNORECASE) ]
        #b = [ v.text for v in verses if word in v.text ]
        #w = word.lower()
        #b = [ v.text for v in verses if w in v.text.lower() ]
    print('list search:', len(b))

def test_np_search(verses):
    ptrn = re.compile(rf"{word}")
    #verses = list(map(lambda v: [v.text.strip()] + v.attrib['id'].split('.')[1:], verses ))
    verses = list(map(lambda v: Verse(v.text.strip(), *v.attrib['id'].split('.')[1:]), verses ))
    for i in range(0,100):
        #ii = [ iv for iv in enumerate(verses) if iv[1][1] in ('GEN','EXO')]
        #ii = [ iv for iv in enumerate(verses) if iv[1].book in ('GEN','EXO')]
        ii = [ iv for iv in enumerate(verses) if ptrn.search(iv[1].text, re.IGNORECASE)]
    #print(ii)
    print('object search:', len(ii))

import timeit as T

tree,verses = setup()

print(T.timeit('test_xpath_search(tree)',number=1,globals=globals()))

print(T.timeit('test_list_search(verses)',number=1,globals=globals()))

print(T.timeit('test_np_search(verses)',number=1,globals=globals()))



print('done')
input()
