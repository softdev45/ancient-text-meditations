import re
from lxml import etree
from dataclasses import dataclass

#import numpy as np

@dataclass
class Verse:
    text: str
    book: str
    chapter: int
    verse: int

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

    def query(self, query):
        ptrn = re.compile(rf"{query}")
        self.last_query_result = result = [ v for v in self.verses if ptrn.search(v.text, re.IGNORECASE) ]
        return result
    
    def query_ref(self, ref):
        self.last_ref_query_result = result = [ v for v in self.verses if ref == [v.book,v.chapter,v.verse] ]
        return result[0]

        
                


