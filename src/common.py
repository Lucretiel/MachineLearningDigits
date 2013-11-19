'''Common functionaltiy for the digit learning project'''
from sys import stdin, stdout
from pickle import dump as dump_to_stream, load as load_from_stream
from collections import namedtuple
from functools import wraps

######################################################################
# MESSAGE TYPES
######################################################################

NUM_ROWS = 16
NUM_COLUMNS = 16
class Digit(namedtuple('DigitBase', 'numeral, pixels')):
    #global xrange objects remove the need for an xrange call when looping
    row_range = range(NUM_ROWS)
    colum_range = range(NUM_COLUMNS)

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
        return self.pixels[self.get_index(row, column)]

    #Note that the iterate_over functions return sequences
    def iterate_over_row(self, row):
        '''
        Iterate over a given row.
        '''
        return self.pixels[self.get_index(row, 0):self.get_index(row, 16)]

    def iterate_over_column(self, column):
        '''
        Iterate over a given column.
        '''
        return [self.get_pixel(row, column) for row in self.row_range]

    #Note that the "iterate over all x" functions return generators
    @property
    def rows(self):
        '''
        Iterate over all rows
        '''
        for row in self.row_range:
            yield self.iterate_over_row(row)

    @property
    def columns(self):
        '''
        Iterate over all columns
        '''
        for column in self.colum_range:
            yield self.iterate_over_column(column)

    def __iter__(self):
        return iter(self.pixels)

######################################################################
# THE BASICS - ENCODE, DECODE, READ, WRITE
######################################################################

def read_messages(stream):
    '''
    Read Messages off a stream
    '''
    try:
        while True:
            yield load_from_stream(stream)
    except EOFError:
        pass

def write_messages(stream, messages):
    '''
    Write messages to a stream
    '''
    try:
        for message in messages:
            dump_to_stream(message, stream, protocol=3)
    except BrokenPipeError:
        pass

    #Need to close even (especially if) the previous block raises
    try:
        stream.close()
    except BrokenPipeError:
        pass

######################################################################
# DECORATORS
######################################################################

# WRITERS

def message_writer(func):
    '''
    Calls the wrapped function, and writes all messages returned or yielded
    '''
    @wraps(func)
    def writer(*args, **kwargs):
        '''
        Bound writer function. Writes bound function return values to outstream
        '''
        write_messages(kwargs.pop('outstream', stdout.buffer), func(*args, **kwargs))
    return writer

# READERS

def message_reader(func):
    '''
    Calls the function with an iterable of messages, and returns the result
    '''
    @wraps(func)
    def reader(*args, **kwargs):
        '''
        Bound reader function. Passes an iterable of messages to the bound
        function as the first positional argument.
        '''
        return func(read_messages(kwargs.pop('instream', stdin.buffer)),
            *args, **kwargs)
    return reader

def message_handler(func):
    '''
    Combination of reader and writer
    '''
    return message_writer(message_reader(func))

######################################################################
## AUTOEXEC. Run that function right away
######################################################################

def autoexec(name=None, parser=None):
    '''
    Decorator to immediatly execute function. Pass it __name__ to make
    it only execute if name == '__main__'. If it is given a parser, it runs
    parse_args on it, and passes the results to func as kwargs.
    '''
    def decorator(func):
        '''
        Parse args if nessesary, then if name is '__main__' or not given,
        call the function immediatly.
        '''
        if name is None or name == '__main__':
            args = vars(parser.parse_args()) if parser else {}
            func(**args)
        return func
    return decorator

######################################################################
## Convert a point to n-dimensional polynomial space
######################################################################

def poly_space(x, y, degrees):
    return [(x ** p) * (y ** (d - p))
    for d in range(degrees + 1) for p in range(d + 1)]

Features = namedtuple('Features', 'numeral, x_feature, y_feature')
class Weights(namedtuple('WeightsBase', 'weights, degree')):
    def value_at(self, x, y):
        def multiply_through():
            for coord, w in zip(poly_space(x, y, self.degree), self.weights):
                yield coord * w
        return sum(coord * w for coord, w in
            zip(poly_space(x, y, self.degree), self.weights))
