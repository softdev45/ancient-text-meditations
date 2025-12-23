import re
from lxml import etree
from dataclasses import dataclass, asdict

#import numpy as np

@dataclass
class Verse:
    text: str
    book: str
    chapter: int
    verse: int

    def __init__(self, text, *args):
        self.text = text
        self.book = args[0]
        self.chapter = int(args[1])
        self.verse = int(args[2])

    # def __repr__(self):
    #     return f"{self.book}:{self.chapter}:{self.verse} {self.text}"
    # def __str__(self):
    #     return f"{self.book}:{self.chapter}:{self.verse} {self.text}"

class VerseBrowser():


    def __init__(self, filepath):
        self.filepath = filepath
        if filepath.endswith('.xml'):
            self.load_xml_file()
        print('loaded bible data')

    def load_xml_file(self):
        self.xml_tree = etree.parse(self.filepath)
        verses = self.xml_tree.xpath('//seg')
        self.verses = list(map(lambda v: Verse(v.text.strip(), *v.attrib['id'].split('.')[1:]), verses )) #extract id
        print(self.verses[:10])
        print(type(self.verses[0].chapter))

    def query(self, query):
        ptrn = re.compile(rf"{query}")
        self.last_query_result = result = [ v for v in self.verses if ptrn.search(v.text, re.IGNORECASE) ]
        return result
    
    def query_ref(self, ref):
        # ref = list(map( lambda e: str(e), ref))
        print(ref)
        ref[1] = int(ref[1])
        #quick fix for PROD; TODO: refactor
        if(len(ref)==3):
            ref[2] = int(ref[2])

        result = [ asdict(v) for v in self.verses if ref[0] == v.book and ref[1] == v.chapter and (len(ref)<=2 or ref[2] == v.verse) ]
        self.last_ref_query_result = result 
        # print(result)
        return result
    
    def query_word(self, word):
        # print(word)
        result = [ asdict(v) for v in self.verses if word.lower() in v.text.lower()]
        self.last_word_query_result = result 
        # print(result)
        return result


        
                


