from numpy import matrix, array, exp, zeros
from numpy.linalg import pinv
from common import Weights, poly_space
from function_registry import FunctionRegistry
from random import random

all_regressions = FunctionRegistry()

def make_XY(data, degree, digit1, digit2, output_type):
    feature_data = []
    numeral_data = []
    digits = {
        digit1: 1,
        digit2: -1
    }

    for point in data:
        feature_data.append(
            poly_space(
                point.x_feature,
                point.y_feature,
                degree))

        numeral_data.append([digits[point.numeral]])

    X = output_type(feature_data)
    Y = output_type(numeral_data)
    return X, Y

@all_regressions.register
def linear_regression(data, degree, digit1, digit2):
    X, Y = make_XY(data, degree, digit1, digit2, matrix)
    X_pinv = pinv(feature_data)
    w = X_pinv * Y
    result = w.transpose().tolist()[0]
    return Weights(result, degree)

def list_add(l1, l2):
    return [a + b for a, b in zip(l1, l2)]

import sys

@all_regressions.register
def logistic_regression(data, degree, digit1, digit2):
    digits = {
        digit1: 1,
        digit2: -1
    }
    X = []
    Y = []
    for point in data:
        X.append(poly_space(point.x_feature, point.y_feature, degree))
        Y.append([digits[point.numeral]])

    X = array(X)
    Y = array(Y)

    products = X * Y

    N = len(X)
    W = array([random() for _ in X[0]])

    def summation(w):
        for x_y in products:
            #print (x_y, file=sys.stderr)
            yield x_y / (1 + exp(x_y * w))
    def gradient(w):
        return sum(summation(w))/N

    num_iterations = 500
    n = 1
    threshold = 0.001

    for t in range(num_iterations):
        g = gradient(W)
        W = (W + n*g)
        if(sum(g**2) < threshold):
            break
    return Weights(W.tolist(), degree)


