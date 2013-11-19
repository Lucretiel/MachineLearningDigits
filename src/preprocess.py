'''
Preprocess converts the digit data provided by the class to the internal
base64-protobuf format used here.
'''

from common import message_writer, autoexec, Digit
from sys import stdin

@autoexec(__name__)
@message_writer
def preprocess():
    '''
    Preprocess the data in the file to the protobuf format.
    '''
    for line in stdin:
        data = [float(x) for x in line.strip().split()]
        yield Digit(int(data[0]), data[1:])
