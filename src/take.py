'''
Take emits 1 of each given digit, sequentially. For instance,
{1, 2, 3, 1, 2, 3} -> take 2 1 3 will emit the first 2 and the last 1 and 3.
'''

from common import encoded_reader, message_writer, autoexec
from digits_pb2 import Digit
import argparse

PARSER = argparse.ArgumentParser('take')
PARSER.add_argument('wanted_digits', nargs='+', type=int, choices=range(10),
    metavar='digit')

@autoexec(__name__, PARSER)
@message_writer
@encoded_reader(Digit)
def take(pairs, wanted_digits):
    '''
    Take from the data pairs the given digits, in order.
    '''
    #Strange, clever use of python name binding. The wanted value is changed
    #with every iteration of the for loop below.
    wanted = None
    filtered_pairs = (encoded for encoded, digit in pairs
        if digit.numeral == wanted)

    for wanted in wanted_digits:
        #Find next that matches predicate.
        try:
            yield next(filtered_pairs)
        except StopIteration:
            return

