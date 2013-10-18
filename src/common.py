'''Common functionaltiy for the digit learning project'''

from base64 import b64encode, b64decode
from sys import stdin, stdout
from google.protobuf.message import Message as MessageBase

######################################################################
# THE BASICS - ENCODE, DECODE, READ, WRITE
######################################################################

def encode_message(message):
    '''
    Encode a protobuf message into base64
    '''
    return '{}\n'.format(b64encode(message.SerializeToString()))

def decode_message(data, message):
    '''
    Decode base64 into a protobuf message
    '''
    message.ParseFromString(b64decode(data.rstrip()))
    return message

def read_messages(stream, message_type):
    '''
    Read and decode messages of a stream. One message per line. Yields
    the base64 encoded data as well as the decoded message
    '''
    message = message_type()
    for line in stream:
        yield line, decode_message(line, message)

def make_encoded(messages):
    '''
    Encoder-generator for messages. Yields the message if it is already encoded,
    encodes and yields it if it's a MessageBase, and discards otherise.
    '''
    for message in messages:
        if isinstance(message, str):
            yield message
        elif isinstance(message, MessageBase):
            yield encode_message(message)

def write_messages(stream, messages):
    '''
    Write a series of messages to a stream, one message per line. Ignores
    anything that isn't a message or encoded data
    '''
    try:
        stream.writelines(make_encoded(messages))
    except IOError:
        pass
######################################################################
# DECORATORS
######################################################################

## STATEFUL DECORATORS. USUALLY APPLIED TO GENERATORS

# WRITERS

def message_writer(func):
    '''
    Calls the wrapped function, and writes all messages returned or yielded
    '''

    def writer(*args, **kwargs):
        '''
        Bound writer function. Writes bound function return values to outstream
        '''
        write_messages(kwargs.pop('outstream', stdout), func(*args, **kwargs))
    return writer

# READERS

def encoded_reader(message_type):
    '''
    Calls the function with an iterable of (encoded, message) pairs, and return
    the result
    '''
    def decorator(func):
        '''
        Decorate a function to be an encoded_reader of a given message_type
        '''
        def reader(*args, **kwargs):
            '''
            Bound reader function. Passes an iterable of (encoded, messagae)
            pairs to the bound function as the first positional argument.
            '''
            return func(
                read_messages(
                    kwargs.pop('instream', stdin), message_type),
                *args, **kwargs)
        return reader
    return decorator

def message_reader(message_type):
    '''
    Calls the function with an iterable of messages, and returns the result
    '''
    def decorator(func):
        '''
        Decorate a function to be a message_reader of the given message_type.
        '''
        @encoded_reader(message_type)
        def reader(encoded_message_pairs, *args, **kwargs):
            '''
            Bound reader function. Passes an iterable of messages to the bound
            function as the first positional argument.
            '''
            encoded_removed = (message for _, message in encoded_message_pairs)
            return func(encoded_removed, *args, **kwargs)
        return reader
    return decorator
######################################################################
## HELPFUL FUNCTIONS FOR PARSING DIGIT DATA
######################################################################

NUM_ROWS = 16
NUM_COLUMNS = 16
class PixelData(tuple):
    '''
    This class simulates a 2d matrix of pixels, which are read from protobuf
    Digit.data data. It provides row-wise and column-wise iteration, and
    (unchecked) 2d index lookup
    '''

    #global xrange objects remove the need for an xrange call when looping
    row_range = xrange(NUM_ROWS)
    colum_range = xrange(NUM_COLUMNS)

    @staticmethod
    def get_index(row, column):
        '''
        Get the 1D index of a given row, column index
        '''
        return (row * NUM_COLUMNS) + column

    def get_pixel(self, row, column):
        '''
        Get the pixel value at a given row, column
        '''
        return self[self.get_index(row, column)]

    #Note that the iterate_over functions return sequences
    def iterate_over_row(self, row):
        '''
        Iterate over a given row.
        '''
        return self[self.get_index(row, 0):self.get_index(row, 16)]

    def iterate_over_column(self, column):
        '''
        Iterate over a given column.
        '''
        return [self.get_pixel(row, column) for row in self.row_range]

    #Note that the "iterate over all x" functions return generators
    def rows(self):
        '''
        Iterate over all rows
        '''
        for row in self.row_range:
            yield self.iterate_over_row(row)

    def columns(self):
        '''
        Iterate over all columns
        '''
        for column in self.colum_range:
            yield self.iterate_over_column(column)

######################################################################
## AUTOEXEC. Run that function right away
######################################################################

def autoexec(name=None, parser=None):
    '''
    Decorator to immediatly execute function. Pass it __name__ to make
    it only execute if name == '__main__' Pass it parser to run
    arg_parse, then apply the results as kwargs to the bound function
    '''
    def decorator(func):
        '''
        Parse args if nessesary, then if name is '__main__' or not given,
        call the function immediatly.
        '''
        if name is None or name == '__main__':
            if parser:
                args = vars(parser.parse_args())
            else:
                args = {}
            func(**args)
        return func
    return decorator
