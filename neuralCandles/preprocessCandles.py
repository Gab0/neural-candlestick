#!/bin/python

import numpy as np
import copy


def prepareToInput(candleWindow):
    # we don't want a numpy.array here!
    # just normalizing candle values
    candleWindow = copy.deepcopy(candleWindow)
    N = float(np.linalg.norm(candleWindow))
    for i, candle in enumerate(candleWindow):
        for j, V in enumerate(candle):
            candleWindow[i][j] = V / N

    return candleWindow


# TO PREDICT FUTURE PRICE;
def priceDataset(candleSet):
    #return candleSet[:-1], [candleSet[-1]]
    def between(a, m, b):
        A = a == m
        B = b == m
        return A or B

    # CLOSE VALUE WENT UP;
    A = candleSet[-1][3] > candleSet[-2][3]
    # BULL OR BEAR CANDLE;
    B = candleSet[-1][3] > candleSet[-1][0]
    # LOW IS CONTAINED;
    C = between(candleSet[-1][0], candleSet[-1][1], candleSet[-1][3])
    # HIGH IS CONTAINED;
    D = between(candleSet[-1][0], candleSet[-1][2], candleSet[1][3])
    # BIG MOVEMENT ON CANDLE (CLOSE VALUES);
    movement = abs(candleSet[-1][3] - candleSet[-2][3]) / candleSet[-2][3]
    E = movement > 0.02
    F = movement > 0.05

    labels = [A, B, C, D, E, F]
    for k in range(len(labels)):
        labels[k] = 1 if labels[k] else 0

    return candleSet[:-1], labels


# TO PREDICT PRICE MOVEMENT;
def changeDataset(candleSet):
    toPredict = candleSet[:-1]
    Result = candleSet[-1][3]
    delta = Result - toPredict[-1][3]
    future = 1 if delta >= 0 else 0
    return toPredict, [future]
