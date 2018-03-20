#!/bin/python


import httpInterface
import neuralGenesis
import subprocess
import sys
import time

port = int(sys.argv[-1])
addr = ('', port)


def process(self, candle):
    print("processing %s" % candle)
    return candle






def testServer(port):
    Q = subprocess.Popen([ 'wget', 'http://127.0.0.1:%i?candle=2333' % port, '--spider' ], stdout=subprocess.PIPE)
    print("WGET TEST TEXT:")
    time.sleep(2)
    print(Q.stdout.read())

    print("neural-candles server running on %s" % port)


Server = httpInterface.getServer(responseFunction=process, port=port)
Network = neuralGenesis.getNetwork()
