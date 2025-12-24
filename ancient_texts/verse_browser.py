import re
from lxml import etree
from dataclasses import dataclass, asdict

#import numpy as np

def get_file_name(filepath):
    version_name = filepath.split('/')[-1].split('.')[0] #fname without ext
    return version_name


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


    def __init__(self, *filepaths):
        self.data = {}
        self.filepaths = filepaths
        self.versions = []
        for filepath in filepaths:
            if filepath.endswith('.xml'):
                self.load_xml_file(filepath)
        print('loaded bible data')

    def load_xml_file(self, filepath):
        self.xml_tree = etree.parse(filepath)
        version_name = get_file_name(filepath) #fname without ext
        self.versions.append(version_name)
        verses = self.xml_tree.xpath('//seg')
        self.data[version_name] = list(map(lambda v: Verse(v.text.strip(), *v.attrib['id'].split('.')[1:]), verses )) #extract id
        print(f'loaded file: {filepath}')

    def query(self, query, version= None):
        verses = self.get_verses(version)
        ptrn = re.compile(rf"{query}")
        result = [ v for v in verses if ptrn.search(v.text, re.IGNORECASE) ]
        return result
    
    def query_ref(self, ref, version = None):
        verses = self.get_verses(version)
        # ref = list(map( lambda e: str(e), ref))
        print(ref)
        ref[1] = int(ref[1])
        #quick fix for PROD; TODO: refactor
        if(len(ref)==3):
            ref[2] = int(ref[2])

        result = [ asdict(v) for v in verses if ref[0] == v.book and ref[1] == v.chapter and (len(ref)<=2 or ref[2] == v.verse) ]
        # print(result)
        return result
    
    def query_word(self, word, version = None):
        verses = self.get_verses(version)
        print(verses[0])

        # print(word)
        result = [ asdict(v) for v in verses if word.lower() in v.text.lower()]
        print(result)
        return result

    def get_versions(self):
        return list(self.data.keys())

    def get_verses(self, version = None):
        verses = self.data[self.versions[0]]
        if version:
            verses = self.data[version]
        return verses
