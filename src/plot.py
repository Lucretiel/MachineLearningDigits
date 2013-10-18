'''
Plot the recieved feature data
'''

import matplotlib.pyplot as plt
from common import message_reader, autoexec
from digits_pb2 import PlotData
import argparse


PARSER = argparse.ArgumentParser()
PARSER.add_argument('--title', '-t')
PARSER.add_argument('--xlabel', '-x')
PARSER.add_argument('--ylabel', '-y')
PARSER.add_argument('--legend', '-l', action='store', nargs='?',
    const='best', metavar='location')
PARSER.add_argument('--digit_spec', '-d', action='append', nargs=2,
    metavar=('digit', 'spec'))

# pylint: disable=R0913

@autoexec(__name__, PARSER)
@message_reader(PlotData)
def plot(plot_data_input, digit_spec, title, xlabel, ylabel, legend):
    '''
    Plot the features
    '''

    plot_data = {int(digit):([], [], spec) for digit, spec in digit_spec}

    for data in plot_data_input:
        # pylint: disable=E1101
        if data.type == PlotData.point_type:
            digit_plot_data = plot_data.get(data.point.numeral)
            if digit_plot_data:
                digit_plot_data[0].append(data.point.x_feature)
                digit_plot_data[1].append(data.point.y_feature)
        elif data.type == PlotData.line_type:
            pass

    for numeral, digit_plot_data in plot_data.iteritems():
        # pylint: disable=W0142
        plt.plot(*digit_plot_data, label=numeral)
    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if legend:
        plt.legend(loc=legend)
    plt.show()
