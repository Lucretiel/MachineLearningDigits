'''
Filter the received data. Only emit the data of the given numerals.
'''

from common import encoded_reader, message_writer, autoexec
from digits_pb2 import Digit
import argparse

PARSER = argparse.ArgumentParser('filter')
PARSER.add_argument('valid', nargs='+', type=int, choices=range(10),
    metavar='digit')

@autoexec(__name__, PARSER)
@encoded_reader(Digit)
@message_writer
def run_filter(pairs, valid):
    '''
    Filter the data, keeping only the given valid digits.
    '''
    valid_numerals = set(valid)
    for encoded, digit in pairs:
        if digit.numeral in valid_numerals:
            yield encoded
