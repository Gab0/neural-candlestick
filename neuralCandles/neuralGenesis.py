#!/bin/python
import numpy as np
import json
from keras.models import Model, Sequential
from keras.layers import Dense, Dropout, TimeDistributed, Conv1D
from keras.layers import LSTM, Reshape, LeakyReLU
from keras.layers import PReLU, ELU
from keras.utils.generic_utils import get_custom_objects

#from keras import optimzers
#from keras import objectives
#from keras import metrics

from keras import backend as K
import time


class neuralNetworkCreator():
    def __init__(self):
        self.network = None

    def createNetwork(self, specifications):
        zerotime = time.time()
        self.network = generateNetwork(networkParameters=specifications)

        print("took %.3f for network genesis." % (time.time() - zerotime))

    def learn(self, dataset, evalDataset, nb_epochs=300):
        History = self.network.fit(dataset['input'],
                                   dataset['target'],
                                   epochs=nb_epochs,
                                   validation_data=(evalDataset['input'],
                                                    evalDataset['target'])
        )

        return History.history['loss'][-1]




def getDefaultNetworkParameters():
    return json.loads(open("defaultNetwork.json").read())


def closelosspercent(Y_true, Y_predicted):
    def G(VAL):
        return VAL[0][0][3]

    T = G(Y_true)
    loss = G(Y_predicted) - T

    loss /= T
    print(loss)
    loss = K.abs(loss)

    return loss * 100


def pricevariation(Y_true, Y_predicted):
    def D(VAL):
        return VAL[0][0][3] - VAL[0][0][0]

    tC = D(Y_true)
    pC = D(Y_predicted)

    #percentile = (tC - pC) / tC
    #percentile = K.abs(percentile)
    #print(percentile)
    TCG = K.greater(tC, 0)
    PCG = K.greater(pC, 0)

    if TCG and PCG:
        L = 100 # - percentile
    elif not TCG and not PCG:
        L = 100 # - percentile
    else:
        L = 0

    return K.variable(np.array(L, dtype='float64'),
                      dtype='float64', name='loss')


get_custom_objects().update({"closelosspercent": closelosspercent})
get_custom_objects().update({"pricevariation": pricevariation})


def generateNetwork(networkParameters):

    optimizationTypes = {
        0: 'adam',
        1: 'sgd',  # BAD SUITED;
        2: 'adagrad',
        3: 'rmsprop'
    }

    lossFunctionTypes = {
        0: 'mean_squared_error',
        1: 'closelosspercent',
        2: 'pricevariation'
    }

    network = Sequential()

    # network always receive OLHCV so we start with that
    network.add(TimeDistributed(Dense(5), input_shape=(None, 5)))

    # network will have the format: <input> <time distributed phase> <2d phase> <output>

    i = 0

    for LAYER in networkParameters['neuralLayers']:
        if i == networkParameters['stageonesize']:
            # network.add(TimeDistributed(Merge()))
            # network.add(TimeDistributed(Dense(1)))
            pass
        appendLayer(network, LAYER,
                    timeDistributed=i < networkParameters['stageonesize'])
        i += 1
    # now to the variability

    # setup output layer;
    print("append to output")
    # network.add(TimeDistributed(Dense(30)))
    network.add(LSTM(5))
    network.add(Reshape((1, 5)))
    # network.add(TimeDistributed(Dense(5)))

    optimizer = optimizationTypes[networkParameters['optimizer']]
    loss = lossFunctionTypes[networkParameters['loss']]
    network.compile(loss=loss, optimizer=optimizer)
    return network


def getFinalLayerName(network):
    return network.layers[-1].name.split('_')[0]


def appendLayer(network, parameters, timeDistributed=True):
    layerTypes = {
        0: [Dense, 'size'],
        1: [Conv1D, 'filters', 'size'],
        2: [Dropout, 'rate'],
        3: [LeakyReLU, 'alpha'],
        4: [PReLU],
        5: [ELU, 'alpha'],

    }

    layerType = layerTypes[parameters['type']]

    constructor = layerType[0]
    arguments = [parameters[W] for W in layerType[1:]]

    # print(arguments)
    layer = constructor(*arguments)

    if timeDistributed:
        layer = TimeDistributed(layer)

    network.add(layer)


def appendDense(network, size, rate):
    if network.layers:
        finalLayerName = getFinalLayerName(network)
        if finalLayerName == 'dense':
            pass
    l = Dense(size)
    w = TimeDistributed(l)
    network.add(w)


def appendDropout(network, size, rate):
    if network.layers:
        if len(network.layers[-1].output_shape) == 3:
            l = Dropout(rate)
            w = TimeDistributed(l)
            network.add(w)
        else:
            raise


def appendTimeDistributed(network, size):
    if network.layers:
        finalLayerName = getFinalLayerName(network)
        if finalLayerName == 'dense':
            pass


def appendLSTM(network, size):
    pass

