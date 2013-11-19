'''
Plot the recieved feature data
'''

import matplotlib.pyplot as plt
import numpy
from common import message_reader, autoexec, Features, Weights, poly_space
import argparse


PARSER = argparse.ArgumentParser()
PARSER.add_argument('--title', '-t')
PARSER.add_argument('--xlabel', '-x')
PARSER.add_argument('--ylabel', '-y')
PARSER.add_argument('--legend', '-l', action='store', nargs='?',
    const='best', metavar='location')
PARSER.add_argument('--digit_spec', '-d', action='append', nargs=2,
    metavar=('digit', 'spec'))
PARSER.add_argument('--regression-name', '-n')
PARSER.add_argument('--regression-resolution', '-r', type=int,
    default=200)

@autoexec(__name__, PARSER)
@message_reader
def plot(plot_data_input, digit_spec, title, xlabel, ylabel, legend,
        regression_name, regression_resolution):
    '''
    Plot the features
    '''

    plot_data = {int(digit): ([], [], spec) for digit, spec in digit_spec}
    plot_line = None

    for data in plot_data_input:
        if isinstance(data, Features):
            digit_plot_data = plot_data.get(data.numeral)
            if digit_plot_data:
                digit_plot_data[0].append(data.x_feature)
                digit_plot_data[1].append(data.y_feature)
        elif isinstance(data, Weights):
            plot_line = data

    for numeral, digit_plot_data in plot_data.items():
        plt.plot(*digit_plot_data, label=numeral)
    if plot_line:
        xmin, xmax = plt.xlim()
        ymin, ymax = plt.ylim()
        X, Y = numpy.meshgrid(
            numpy.linspace(xmin, xmax, regression_resolution),
            numpy.linspace(ymin, ymax, regression_resolution))
        Z = plot_line.value_at(X, Y)
        plt.contour(X, Y, Z, levels=[0])

    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if legend:
        plt.legend(loc=legend)
    plt.show()
