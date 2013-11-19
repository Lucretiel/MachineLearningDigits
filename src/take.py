'''
Take emits 1 of each given digit, sequentially. For instance,
{1, 2, 3, 1, 2, 3} -> take 2 1 3 will emit the first 2 and the last 1 and 3.
'''

from common import message_handler, autoexec
import argparse

PARSER = argparse.ArgumentParser('take')
PARSER.add_argument('wanted_digits', nargs='+', type=int, choices=range(10),
    metavar='digit')

@autoexec(__name__, PARSER)
@message_handler
def take(digits, wanted_digits):
    '''
    Take from the data pairs the given digits, in order.
    '''
    try:
        for wanted in wanted_digits:
            yield next(digit for digit in digits if digit.numeral == wanted)
    except StopIteration:
        pass
