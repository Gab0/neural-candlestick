#/bin/python

import http.server
import socketserver
from threading import Thread
import urllib.parse
stdHandler = http.server.SimpleHTTPRequestHandler

class getHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        param=urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        print(param)

def getServer(handler=getHandler, port=2999):
    httpd = socketserver.TCPServer(("", port), handler)
    server = Thread(target=httpd.serve_forever)
    server.start()

    return httpd

