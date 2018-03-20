#!/bin/python

import numpy as np

from keras.models import Model, Sequential
from keras.layers import Dense, Dropout, TimeDistributed
#from keras import optimzers
#from keras import objectives
#from keras import metrics

import time

zerotime = time.time()
default_networkParameters = {
    'layerone': {
        'type': 0,
        'subtype':2,
        'size': 30,
        'rate': 0.2

    },
    'layertwo': {
        'type': 1,
        'subtype': 1,
        'size': 40,
        'rate': 0.4
    },

    'layerthree': {
        'type': 1,
        'subtype': 1,
        'size': 40,
        'rate': 0.4

            },
    'stageonesize': 2,
    'optimizer': 0,
    'loss': 0,
    'foresee': 6,
    'historySize': 18
}


def generateNetwork(networkParameters=default_networkParameters):
    optimizationTypes = {
        0: 'adam'


    }

    lossFunctionTypes = {
        0: 'mean_squared_error'
    }

    network = Sequential()

    # network always receive OLHCV so we start with that
    network.add(TimeDistributed(Dense(5),input_shape=(None,5)))

    # network will have the format: <input> <time distributed phase> <2d phase> <output>
    layers = [ 'layerone', 'layertwo', 'layerthree' ]
    for i, W in enumerate(layers):
        param = networkParameters[W]

        appendLayer( network, param, timeBased= i < networkParameters['stageonesize'] )

    

    # now to the variability
    #network.add(TimeDistributed(Dense(5)))
    optimizer = optimizationTypes[networkParameters['optimizer']]
    loss = lossFunctionTypes[networkParameters['loss']]
    network.compile(loss=loss, optimizer=optimizer)
    return network

getFinalLayerName = lambda network: network.layers[-1].name.split('_')[0]

def appendLayer(network, parameters, timeBased=True):
    layerTypes = {
        0: [ Dense, 'size'],
        1: [ Dropout, 'rate'],
        2: appendTimeDistributed,
        3: appendLSTM
    }

    layerType = layerTypes[parameters['type']]

    constructor = layerType[0]
    arguments =  [parameters[W] for W in layerType[1:] ]

    layer = constructor(*arguments)

    if timeBased:
        layer = TimeDistributed(layer)

    network.add(layer)


def appendDense(size, rate):
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

if __name__ == '__main__':
    print("Testing network genesis with stock parameters.")
    network = generateNetwork()
    print(network.summary)

    print("took %.3f for network genesis." % (time.time()-zerotime))
