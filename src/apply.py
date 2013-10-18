'''
Apply 2 features to the received digits
'''

from common import message_reader, message_writer, PixelData, autoexec
from digits_pb2 import Digit, PlotData
from features import all_features
import argparse

PARSER = argparse.ArgumentParser('apply')
PARSER.add_argument('x_feature', choices=all_features.keys(),
    metavar='x_feature')
PARSER.add_argument('y_feature', choices=all_features.keys(),
    metavar='y_feature')

@autoexec(__name__, PARSER)
@message_reader(Digit)
@message_writer
def apply_features(digits, x_feature, y_feature):
    '''
    Apply the 2 features to every digit
    '''
    result = PlotData()
    result.type = PlotData.point_type
    x_feature = all_features[x_feature]
    y_feature = all_features[y_feature]

    for digit in digits:
        data = PixelData(digit.data)
        result.point.numeral = digit.numeral
        result.point.x_feature = x_feature(data)
        result.point.y_feature = y_feature(data)
        yield result
