'''
Apply 2 features to the received digits
'''

from common import message_handler, autoexec, Features
from features import all_features
import argparse

PARSER = argparse.ArgumentParser('apply',
    epilog="Available Features: {}".format(', '.join(all_features.func_names())))
PARSER.add_argument('x_feature', choices=all_features.func_names(),
    metavar='x_feature')
PARSER.add_argument('y_feature', choices=all_features.func_names(),
    metavar='y_feature')

@autoexec(__name__, PARSER)
@message_handler
def apply_features(digits, x_feature, y_feature):
    '''
    Apply the 2 features to every digit
    '''
    x_feature = all_features.get(x_feature)
    y_feature = all_features.get(y_feature)

    for digit in digits:
        yield Features(
            digit.numeral,
            x_feature(digit),
            y_feature(digit))
