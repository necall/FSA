from fst import FST
import string, sys
from fsmutils import composechars, trace
import copy

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """

    # Let's define our first FST
    f1 = FST('soundex-generate')

    # Indicate that '1' is the initial state
    f1.add_state('start');f1.add_state('next');f1.add_state('0');f1.add_state('1');f1.add_state('2');f1.add_state('3');f1.add_state('4');f1.add_state('5');f1.add_state('6')
    f1.initial_state = 'start'

    # Set all the final states
    f1.set_final('next');f1.set_final('0');f1.set_final('1');f1.set_final('2');f1.set_final('3');f1.set_final('4');f1.set_final('5');f1.set_final('6')

    #how to deal with the final state? Does it have to exist?
    # Add the rest of the arcs
    removelist='a e h i o u w y'.split()
    listx=['1','2','3','4','5','6','0']
    switchdict={'1':['b','f','p','v'],'2':['c','g','j','k','q','s','x','z'],'3':['d','t'],'4':['l'],'5':['m','n'],'6':['r']}
    for letter in string.letters:
        f1.add_arc('start', 'next', (letter), (letter))
    for letter in string.lowercase:
        if letter in removelist:
            f1.add_arc('next','0',(letter),())
            f1.add_arc('0','0',(letter),())
            for n in range(1,7):
                f1.add_arc(str(n),'0',(letter),())
        else:
            for n in range(1,7):
                copylist = copy.deepcopy(listx)
                if letter in switchdict[str(n)]:
                    f1.add_arc('next',str(n),(letter),(str(n)))
                    f1.add_arc(str(n),str(n),(letter),())
                    copylist.remove(str(n))
                    for c in copylist:
                        f1.add_arc(c,str(n),(letter),str(n))

    return f1

    # The stub code above converts all letters except the first into '0'.
    # How can you change it to do the right conversion?

def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('start');f2.add_state('1');f2.add_state('2');f2.add_state('3')
    f2.initial_state = 'start'
    f2.set_final('start');f2.set_final('1');f2.set_final('2');f2.set_final('3')

    # Add the arcs
    for letter in string.letters:
        f2.add_arc('start', 'start', (letter), (letter))

    for n in range(1,7):
        f2.add_arc('start', '1', (str(n)), (str(n)))
        f2.add_arc('1','2',(str(n)),(str(n)))
        f2.add_arc('2','3',(str(n)),(str(n)))
        f2.add_arc('3','3',(str(n)),())

    return f2

    # The above stub code doesn't do any truncating at all -- it passes letter and number input through
    # what changes would make it truncate digits to 3?

def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    f3.add_state('1')
    f3.add_state('1a')
    f3.add_state('1b')
    f3.add_state('2')
    
    f3.initial_state = '1'
    f3.set_final('2')
    f3.add_arc('1', '1a', (), ('0'))
    f3.add_arc('1a', '1b', (), ('0'))
    f3.add_arc('1b', '2', (), ('0'))
    for letter in string.letters:
        f3.add_arc('1', '1', (letter), (letter))
    for number in range(1,7):
        f3.add_arc('1', '1a', (str(number)), (str(number)))
        f3.add_arc('1a', '1b', (str(number)), (str(number)))
        f3.add_arc('1b', '2', (str(number)), (str(number)))


    return f3



if __name__ == '__main__':
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()

    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))

