#!/bin/python

import numpy as np

from keras.models import Model, Sequential
from keras.layers import Dense, Dropout
from keras import optimzers
from keras import objectives
from keras import metrics

def generateNetwork(networkParameters):
    """
    sample_networkParameters = {
    'layerone': {'type': 0,
    'size': 30},
    'layertwo': {'type': 1,
    'size': 40}
    }

    """

    layerTypes = {
        0: appendDense,
        1: appendTimeDistributed,
        2: appendLSTM
    }

    network = Sequential()

    # network alway receive OLHCV
    model.add(Dense(4, input_dim=5))


    # now to the variability
    model.add(TimeDistri)

def appendDense(model, size):
    
