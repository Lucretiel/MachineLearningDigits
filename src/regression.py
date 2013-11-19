from common import message_handler, autoexec, Weights
from regressions import all_regressions
import argparse

PARSER = argparse.ArgumentParser('regression',
    epilog="Available Featues: {}".format(
        ', '.join(all_regressions.func_names())))
PARSER.add_argument('--degree', '-d', type=int, default=1)
PARSER.add_argument('--digits', '-n', nargs=2, type=int, choices=range(10))
PARSER.add_argument('regression', choices=all_regressions.func_names())

@autoexec(__name__, PARSER)
@message_handler
def apply_regression(features, regression, degree, digits):
    yield all_regressions.get(regression)(features, degree,
        digits[0], digits[1])
