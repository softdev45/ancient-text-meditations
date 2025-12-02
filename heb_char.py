h_old = ['𐤕', '𐤔', '𐤓', '𐤒', '𐤑', '𐤐', '𐤏', '𐤎', '𐤍', '𐤌', '𐤋', '𐤊', '𐤉', '𐤈', '𐤇', '𐤆', '𐤅', '𐤄', '𐤃', '𐤂', '𐤁', '𐤀','\n', ' ']
h_new = ['ת', 'ש', 'ר', 'ק', 'ץצ', 'ףפ', 'ע', 'ס', 'ןנ', 'םמ', 'ל', 'ךכ', 'י', 'ט', 'ח', 'ז', 'ו', 'ה', 'ד', 'ג', 'ב', 'א', '\n', ' ']
#print(len(h_old),len(h_new))



def index_2(el, arr):
    for i,e in enumerate(arr):
        if el in e:
            return i
    return len(arr)-1

def transform(w,a,b):
    l = list(w)
    l = list(map(lambda el: b[index_2(el, a)], l))
    return ''.join(l)


