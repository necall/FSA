import sys
from fst import FST
from fsmutils import composewords, trace

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
    "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                     "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                     "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'
hundredlist = {100: kFRENCH_TRANS[100], 200: kFRENCH_TRANS[2] + ' ' + kFRENCH_TRANS[100],
               300: kFRENCH_TRANS[3] + ' ' + kFRENCH_TRANS[100], 400: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[100],
               500: kFRENCH_TRANS[5] + ' ' + kFRENCH_TRANS[100], 600: kFRENCH_TRANS[6] + ' ' + kFRENCH_TRANS[100],
               700: kFRENCH_TRANS[7] + ' ' + kFRENCH_TRANS[100], 800: kFRENCH_TRANS[8] + ' ' + kFRENCH_TRANS[100],
               900: kFRENCH_TRANS[9] + ' ' + kFRENCH_TRANS[100]}
uniquenumber = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,20,30,40,50,60]
seveneightynine = {21: kFRENCH_TRANS[20] + ' ' + kFRENCH_AND + ' ' + kFRENCH_TRANS[1],
                   31: kFRENCH_TRANS[30] + ' ' + kFRENCH_AND + ' ' + kFRENCH_TRANS[1],
                   41: kFRENCH_TRANS[40] + ' ' + kFRENCH_AND + ' ' + kFRENCH_TRANS[1],
                   51: kFRENCH_TRANS[50] + ' ' + kFRENCH_AND + ' ' + kFRENCH_TRANS[1],
                   61: kFRENCH_TRANS[60] + ' ' + kFRENCH_AND + ' ' + kFRENCH_TRANS[1],
                   70: kFRENCH_TRANS[60] + ' ' + kFRENCH_TRANS[10],
                   71: kFRENCH_TRANS[60] + ' ' + kFRENCH_AND + ' ' + kFRENCH_TRANS[11],
                   72: kFRENCH_TRANS[60] + ' ' + kFRENCH_TRANS[12], 73: kFRENCH_TRANS[60] + ' ' + kFRENCH_TRANS[13],
                   74: kFRENCH_TRANS[60] + ' ' + kFRENCH_TRANS[14], 75: kFRENCH_TRANS[60] + ' ' + kFRENCH_TRANS[15],
                   76: kFRENCH_TRANS[60] + ' ' + kFRENCH_TRANS[16],
                   77: kFRENCH_TRANS[60] + ' ' + kFRENCH_TRANS[10] + ' ' + kFRENCH_TRANS[7],
                   78: kFRENCH_TRANS[60] + ' ' + kFRENCH_TRANS[10] + ' ' + kFRENCH_TRANS[8],
                   79: kFRENCH_TRANS[60] + ' ' + kFRENCH_TRANS[10] + ' ' + kFRENCH_TRANS[9],
                   80: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20],
                   81: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[1],
                   82: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[2],
                   83: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[3],
                   84: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[4],
                   85: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[5],
                   86: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[6],
                   87: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[7],
                   88: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[8],
                   89: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[9],
                   90: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[10],
                   91: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[11],
                   92: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[12],
                   93: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[13],
                   94: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[14],
                   95: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[15],
                   96: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[16],
                   97: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[10] + ' ' + kFRENCH_TRANS[7],
                   98: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[10] + ' ' + kFRENCH_TRANS[8],
                   99: kFRENCH_TRANS[4] + ' ' + kFRENCH_TRANS[20] + ' ' + kFRENCH_TRANS[10] + ' ' + kFRENCH_TRANS[9]}


def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
        "Integer out of bounds"
    basiclist = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,21,31,41,51,61,71,70,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99]
    if len(str(integer)) == 3:
        first = "%i00" % int(str(integer)[0])
        second = "%i0" % int(str(integer)[1])
        third = "%i" % int(str(integer)[2])
        if int(str(integer)[1:]) in basiclist:
            return [first, str(int(str(integer)[1:]))]
        else:
            return [first,second,third]
    elif len(str(integer)) == 2:
        first = "%i0" % int(str(integer)[0])
        second = "%i" % int(str(integer)[1])
        if integer in basiclist:
            return [str(integer)]
        else:
            return [first, second]
    else:
        return str(integer)


def french_count():
    f = FST('french')

    f.add_state('start');
    f.add_state('hundred');
    f.add_state('unique');
    f.add_state('sen');
    f.initial_state = 'start'

    for number in xrange(1001):
        if number in hundredlist:
            f.add_arc('start', 'hundred', [str(number)], [hundredlist[number]])
        elif number == 0:
            f.add_arc('start','start',[str(number)],[kFRENCH_TRANS[0]])
            f.add_arc('unique','unique',[str(number)],[])
            f.add_arc('hundred', 'hundred', [str(number)], [])
        elif number in uniquenumber:
            f.add_arc('start', 'unique', [str(number)], [kFRENCH_TRANS[number]])
            f.add_arc('hundred', 'unique', [str(number)], [kFRENCH_TRANS[number]])
            f.add_arc('unique', 'unique', [str(number)], [kFRENCH_TRANS[number]])
        elif number in seveneightynine:
            f.add_arc('start', 'sen', [str(number)], [seveneightynine[number]])
            f.add_arc('hundred', 'sen', [str(number)], [seveneightynine[number]])


    f.set_final('hundred')
    f.set_final('unique')
    f.set_final('sen')


    return f



if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()
    if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_cinput)))


