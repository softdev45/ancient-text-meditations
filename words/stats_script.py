from words.word import Word, load

from sys import argv

def print_results(r):
    mapped = {}

    for wrd in r:
        if not wrd.root in mapped:
            mapped[wrd.root] = []
        mapped[wrd.root].append(wrd)

    result = [ (len(mapping), (key, mapping)) for key,mapping in mapped.items() ]
    sorted_result = sorted(result, key = lambda el: el[0])

    for sr in sorted_result[-30:]:
        print(sr[0],sr[1][1][0])

load()

db = Word.db

if len(argv) > 1:
    inpt = argv[1]

while True:

    if not inpt:
        inpt = 'נ'
        #inpt = 'א'
        #inpt = 'ב'
        inpt = 'ג'
        inpt = 'ד'
        inpt = input('root-letters:')



    r = filter(lambda w: w.root.startswith(inpt),db)
    r1 = filter(lambda w: inpt in w.root, db)

    print_results(r)
    print()
    print_results(r1)

    inpt = None

#for lnght,key_mapping in mapped.items():
#    key = key_mapping[0]
#    mapping = key_mapping[1]

    #print(len(mapping))
    #print(key, mapping)
    #print(sorted_result)




