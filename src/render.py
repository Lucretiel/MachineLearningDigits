'''
The render module renders recieved digits to the command line. It takes an
option --charset, which is a string that specifies what character to use for
a given intensity level (from the first character at -1 to the last at 1)
'''

from common import NUM_COLUMNS, message_reader, autoexec
import argparse

def scale(input_min, input_max, output_min, output_max):
    '''
    Create a function that linearly scales a value from the input range to the
    output range. Converts output to float, but uses int math wherever possible.
    '''
    output_range = output_max - output_min
    input_range = float(input_max - input_min)
    def scale_func(value):
        '''Bound scale function'''
        return (((value - input_min) * output_range) / input_range) + output_min
    return scale_func

PARSER = argparse.ArgumentParser('render')
PARSER.add_argument('--charset', '-c', default=" .:-=+*#%@")

@autoexec(__name__, PARSER)
@message_reader
def render(digits, charset):
    '''
    Render the given digits to the command line, using the charset
    '''

    #Horizontal border line.
    horiz = '+{}+'.format('-'*NUM_COLUMNS)

    #Template string to draw digits
    template = '\n{}\n'.join((horiz, horiz))

    #Scale function to convert pixel values to charset indexes
    charset_scale = scale(-1, 1, 0, len(charset)-1)
    def get_char(value):
        '''Get the char corrosponding to the given value'''
        return charset[int(charset_scale(value))]

    for digit in digits:
        print("Numeral: {}".format(digit.numeral))

        #Print numeral
        print(template.format('\n'.join(
            '|{}|'.format(''.join(get_char(pixel)
                for pixel in row))
            for row in digit.rows)))
