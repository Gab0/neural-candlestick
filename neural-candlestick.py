#!/bin/python


import httpInterface

port = 2997
addr = ('', port)

Server = httpInterface.getServer(port=port)


print("neural-candles server running on %s" % port)
