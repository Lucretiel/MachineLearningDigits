'''
Filter the received data. Only emit the data of the given numerals.
'''

from common import message_handler, autoexec
import argparse

PARSER = argparse.ArgumentParser('filter')
PARSER.add_argument('valid', nargs='+', type=int, choices=range(10),
    metavar='digit')

@autoexec(__name__, PARSER)
@message_handler
def run_filter(digits, valid):
    '''
    Filter the data, keeping only the given valid digits.
    '''
    valid_numerals = set(valid)
    return (digit for digit in digits if digit.numeral in valid_numerals)
