'''
features.py contains a decorator to register features to a global dict, for
use in other modules. It also contains the standard features, though others can
be added
'''

all_features = {} # pylint: disable=C0103

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

@register_feature()
def intensity(digit):
    '''
    Find the overall intensity of a given digit
    '''
    return sum(d+1 for d in digit)

@register_feature()
def symmetry(digit):
    '''
    Find the symmetry of a given digit
    '''
    def diffs():
        '''
        Find the diffs of the digit- difference between each pixel and its
        mirror
        '''
        for row in digit.rows():
            for pixel, opposite in zip(row, reversed(row)):
                yield abs(pixel - opposite)
    return -sum(diffs())

def minmax(data):
    '''
    Find the minimum and maximum of a given iterable
    '''
    iter_data = iter(data)
    initial_minmax = (next(iter_data),) * 2
    def check_minmax(current, check):
        '''
        Reduction to find the overall minmax
        '''
        return (min(current[0], check),
            max(current[1], check))
    return reduce(check_minmax, iter_data, initial_minmax)

@register_feature()
def horizontal_sweep(digit):
    '''
    Find the difference between the leftmost and rightmost center, where a
    center is the weighted mean of a row from left to right.
    '''
    def centers():
        '''
        Find the individual centers.
        '''
        for row in digit.rows():
            row_weight = sum(p+1 for p in row)
            row_total = sum(c * (pixel+1) for c, pixel in enumerate(row))
            if row_total == 0:
                yield 0
            else:
                yield row_total/row_weight
    min_row, max_row = minmax(centers())
    return max_row - min_row

@register_feature()
def vertical_uniformity(digit):
    '''
    Find the sum total of the differences in range of each column
    '''
    def column_spans():
        '''
        Find the range differnece for a given column
        '''
        for column in digit.columns():
            min_value, max_value = minmax(column)
            yield max_value - min_value
    return 32 - sum(column_spans())
