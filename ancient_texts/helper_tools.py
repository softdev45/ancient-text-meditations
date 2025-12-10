import csv
# scripts to process bible text csv; extract from <heb> tags

HA = """אבגדהוזחטיךכלםמןנסעףפץצקרשת"""

H_RANGE = range(ord(HA[0]), ord(HA[-1])+1)


def only_letters(word):
    return ''.join([l for l in word
                    if ord(l) in H_RANGE])


def calc_word_count(word_list):
    result = dict()
    for word in word_list:
        result[word] = result.get(word, 0)+1
    return result


def load_new(dbfile= None):
    # import traceback
    # traceback.print_stack()
    # global db
    # import pathlib
    # script_dir = pathlib.Path(__file__).parent.resolve()
    # print(__file__)
    # print(script_dir)
    db = []
    with open(dbfile, 'r') as file:
        f = csv.reader(file, delimiter='\t')
        verses = list(f)
        for elem in verses:
            db.append(elem)
        print(f'loaded {len(db)} lines from {file}')
    return db
