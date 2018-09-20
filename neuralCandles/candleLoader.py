#!/bin/python
import numpy as np
import json
import os

from . import preprocessCandles


class candleStorage():
    def __init__(self, storagefilename):
        self.storagefilename = storagefilename
        self.candles = []

    def attach(self, candles):
        aCandles = [self.convertCandle(c) for c in candles]
        self.candles.append(aCandles)
        print(len(self.candles))

    def convertCandle(self, candle):
        candleProps = [
            'open',
            'high',
            'low',
            'close',
            'volume'
        ]

        flattenedCandle = [candle[p] for p in candleProps]
        return flattenedCandle

    def show(self):
        for candle in self.candles:
            print(candle)

    def getDataset(self, mode='price'):

        operationModes = {
            'price': preprocessCandles.priceDataset,
            'change': preprocessCandles.changeDataset
        }

        X = []
        Y = []

        for candleWindow in self.candles:
            candleWindow = preprocessCandles.prepareToInput(candleWindow)
            dataX, dataY = operationModes[mode](candleWindow)
            X.append(dataX)
            Y.append(dataY)

        # this is probably deprecated;
        convertToNP = True
        if convertToNP:
            X = np.array(X)
            Y = np.array(Y)

            data_shape = (X.shape, Y.shape)

            print("generating dataset; shapes x:%s   y:%s" % data_shape)

        if X.any() and Y.any():
            return {
                'input': X.reshape(X.shape + (1,)),
                'target': Y
            }

    def store(self, filename=None):
        filename = self.storagefilename if not filename else filename
        D = json.dumps(self.candles)
        open(filename, 'w').write(D)
        print("storing %i candle sets to %s." %
              (len(self.candles), filename))

    def load(self, filename=None):
        filename = self.storagefilename if not filename else filename
        D = open(filename).read()
        D = json.loads(D)
        self.candles = D
        print("loading %i candle sets from %s." %
              (len(self.candles), filename))

    def discard(self):
        self.candles = []
