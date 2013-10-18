'''
Preprocess converts the digit data provided by the class to the internal
base64-protobuf format used here.
'''

from common import message_writer, autoexec
from digits_pb2 import Digit
from sys import stdin

@autoexec(__name__)
@message_writer
def preprocess():
    '''
    Preprocess the data in the file to the protobuf format.
    '''
    digit = Digit()
    for line in stdin:
        digit_data = [float(x) for x in line.strip().split()]
        digit.numeral = int(digit_data[0])
        digit.data.extend(digit_data[1:]) # pylint: disable=E1101
        yield digit
        digit.ClearField("data")
