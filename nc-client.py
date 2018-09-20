#!/bin/python

import requests
import random
import json
import numpy as np
import os


class commandLineInterface():
    def __init__(self):

        self.candleBank = 0
        self.serverUrl = 'http://localhost:5000'
        self.workingDir = os.getcwd()
        self.managementCommands = ['show', 'save', 'load', 'discard']

    def run(self):
        while True:
            modeLabel = 'EVOLVE' if not self.candleBank else 'EVALUATE'
            CMD = input('candleBank: %i-%s>' % (self.candleBank, modeLabel))

            if 'mode' in CMD:
                self.candleBank = 1 - self.candleBank
                r = requests.post(self.serverUrl + '/switch')
                print(r.text)

            elif 'build' in CMD:
                stdblueprint = json.loads(open("defaultNetwork.json").read())
                data = {
                    'blueprint': stdblueprint
                }
                W = requests.post(self.serverUrl + '/setupnetwork',
                                  data=json.dumps(data))
                print(W.text)

            elif 'evolve' in CMD:
                nb_epoch = 70
                data = {'nb_epoch': nb_epoch}
                W = requests.post(self.serverUrl + '/fitness',
                                  data=json.dumps(data))
                print(W.text)

            elif 'neat' in CMD:
                config_path = os.path.join(self.workingDir,
                                           'evolutionconf.toml')
                params = {
                    'config_path': config_path
                }

                r = requests.post(self.serverUrl + '/neat',
                                  data=json.dumps(params)
                )

            elif any([x in CMD
                      for x in self.managementCommands]):
                Action = [x in CMD
                          for x in self.managementCommands].index(True)
                Action = self.managementCommands[Action]
                requests.post(self.serverUrl + '/manage',
                              data=json.dumps({'action': Action,
                                               'bank': self.candleBank
                              }))

            elif 'predict' in CMD:
                Candle = self.loadedCandleBank.getDataset()
                C = random.randrange(0, len(Candle['input']))

                def sampleToDataset(X):
                    return np.array([X])

                Y = sampleToDataset(Candle['target'][C])
                Previous = ["%.3f" % (candle[3] * 20000)
                            for candle in Candle['input'][C]]
                data = {
                    'candles': Candle['input'][C],
                    'prediction': Candle['target'][C]
                }

                W = requests.post(self.serverUrl + '/predict',
                                  data=json.dumps(data))

                print(' '.join(Previous))
                print(W.text)
                print(Y[0][0][3] * 20000)
                #print("predicted %.3f against real price of %.3f" % (price,
                #                                                    realPrice))
            else:
                print("bad command.")


if __name__ == "__main__":
    client = commandLineInterface()
    client.run()
