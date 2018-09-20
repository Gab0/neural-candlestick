from flask import Flask, request
import json
import threading
import numpy as np
import os

import neuralCandles
import optparse

cmdparser = optparse.OptionParser()
cmdparser.add_option('--port <int>', dest='port',
                     type='int', default=2999,
                     help='TCP port to listen')

cmdparser.add_option('-g',
                     dest='GPU',
                     action="store_true",
                     default=False)

#cmdparser.add_option('-l', dest='LoaderMode',
#                     default=False, action='store_true',
#                     help='Candle getter mode;')

options, args = cmdparser.parse_args()

Device = "cuda*" if options.GPU else "cpu"

# check those flags. they assign multicore CPU processing or GPU processing.
# if any of those two components are failing,
# look for info about them for your keras backend (theano or tensorflow) on google.

theano_flags = [
    "mode=FAST_RUN",
    "blas.ldflags=-lopenblas",
    "device=%s" % Device,
    "floatX=float32",
    ",openmp=True"
]

os.environ["THEANO_FLAGS"] = ','.join(theano_flags)

os.environ['MKL_NUM_THREADS'] = '16'
os.environ['GOTO_NUM_THREADS'] = '16'
os.environ['OMP_NUM_THREADS'] = '16'
os.environ['openmp'] = 'True'


"""
import tensorflow as tf
from keras.backend import tensorflow_backend as K

with tf.Session(config=tf.ConfigProto(
                    intra_op_parallelism_threads=16)) as sess:
    K.set_session(sess)
"""


import neuralEvolution
#import neuralGenesis

addr = ('', options.port)


def getServer(candleBanks, neuralNetworkCreator):
    app = Flask(__name__)

    app.candleBanks = candleBanks
    app.currentBank = 0
    app.neuralNetworkCreator = neuralNetworkCreator


    @app.route('/switch', methods=['POST'])
    def switchCandleBank():
        app.currentBank = 1 - app.currentBank
        return ("Candle bank mode %i" % app.currentBank)

    @app.route('/manage', methods=['POST'])
    def manageDatabase():
        parameters = json.loads(request.data)
        action = parameters['action']

        currentBank = app.candleBanks[parameters['bank']]
        if action == 'show':
            currentBank.show()
        elif action == 'save':
            currentBank.store()
        elif action == 'load':
            currentBank.load()
        elif action == 'discard':
            currentBank.discard()

        return action

    @app.route('/candleinput', methods=['POST'])
    def storeCandlestick():
        Candles = json.loads(request.data)
        app.candleBank[app.currentBank].attach(Candles['candles'])
        print(Candles)

    @app.route('/neat', methods=['POST'])
    def runNeat():
        parameters = json.loads(request.data)
        candles = app.candleBanks[0].getDataset()
        # print(json.dumps(candles, indent=2))
        neuralEvolution.hyperneat_candles.evolveNeurals(
            parameters['config_path'],
            candles['input'],
            candles['target']
        )

        return "Finished."
    @app.route('/setupnetwork', methods=['POST'])
    def setupNetwork():
        parameters = json.loads(request.data)
        print(parameters)
        try:
            #app.neuralNetworkCreator.createNetwork(parameters['blueprint'])
            app.network = neuralEvolution.evolve_candles.evolveNetwork(
                app.candleBanks[0].getDataset(),
                app.candleBanks[1].getDataset()
            )
        except Exception as E:
            print("Network creation failed!")
            print(E)
            raise

        return("Network created.")

    @app.route('/fitness', methods=['POST'])
    def runTraining():
        nb_epochs = json.loads(request.data)['nb_epoch']
        evolutionDataset = app.candleBanks[0].getDataset()
        evalDataset = app.candleBanks[1].getDataset()
        Loss = app.neuralNetworkCreator.learn(
            evolutionDataset,
            evalDataset=evalDataset,
            nb_epochs=nb_epochs,
        )
        return(str(Loss))

    @app.route('/predict', methods=['POST'])
    def predictCandle():
        Candles = json.loads(request.data)
        dataCandles = np.array([Candles['candles']])
        if 'prediction' in Candles.keys():
            predictionCandles = np.array([Candles['prediction']])
            W = app.neuralNetworkCreator.network.evaluate(
                dataCandles, predictionCandles)
            print(type(W))
            return('0.4')
        else:
            W = app.neuralNetworkCreator.network.predict(
                dataCandles)
            return(str(W[0][0][3] * 20000))

    return app


if __name__ == '__main__':
    currentFolder = os.path.dirname(os.path.abspath(__file__))
    candleStorage = neuralCandles.candleLoader.candleStorage(
        os.path.join(currentFolder,
                     "candles")
    )

    evalCandleStorage = neuralCandles.candleLoader.candleStorage(
        os.path.join(currentFolder,
                     "evalcandles")
    )
    candleBanks = [candleStorage, evalCandleStorage]


    # neuralNetworkCreator = neuralGenesis.neuralNetworkCreator()
    neuralNetworkCreator = None
    app = getServer(candleBanks, neuralNetworkCreator)
    app.run()
