'''
features.py contains a decorator to register features to a global dict, for
use in other modules. It also contains the standard features, though others can
be added
'''

from functools import reduce
from function_registry import FunctionRegistry
all_features = FunctionRegistry()

def register_feature(name=None):
    '''
    Register a feature to the global table. If no name is provided, use
    the function's name.
    '''
    def decorator(func):
        '''
        Register the function as a feature and return it.
        '''
        regname = name
        if regname is None:
            regname = func.__name__
        all_features[regname] = func
        return func
    return decorator

@all_features.register
def intensity(digit):
    '''
    Find the overall intensity of a given digit
    '''
    return sum(pixel+1 for pixel in digit)

@all_features.register
def symmetry(digit):
    '''
    Find the symmetry of a given digit
    '''
    def diffs():
        for row in digit.rows:
            for pixel, opposite in zip(row, reversed(row)):
                yield abs(pixel - opposite)
    return -sum(diffs())

def minmax(data):
    '''
    Find the minimum and maximum of a given iterable
    '''
    def check_minmax(current, check):
        '''
        Reduction to find the overall minmax
        '''
        return min(current[0], check[0]), max(current[1], check[1])
    return reduce(check_minmax, zip(data, data))

@all_features.register
def horizontal_sweep(digit):
    '''
    Find the difference between the leftmost and rightmost center, where a
    center is the weighted mean of a row from left to right.
    '''
    def centers():
        '''
        Find the individual centers.
        '''
        for row in digit.rows:
            row_weight = sum(p+1 for p in row)
            row_total = sum(c * (pixel+1) for c, pixel in enumerate(row))
            if row_total == 0:
                yield 0
            else:
                yield row_total/row_weight
    min_row, max_row = minmax(centers())
    return max_row - min_row

@all_features.register
def vertical_uniformity(digit):
    '''
    Find the sum total of the differences in range of each column
    '''
    def column_spans():
        '''
        Find the range differnece for a given column
        '''
        for column in digit.columns:
            min_value, max_value = minmax(column)
            yield max_value - min_value
    return 32 - sum(column_spans())
