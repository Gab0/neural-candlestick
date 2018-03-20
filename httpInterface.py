#/bin/python

import http.server
import socketserver
from threading import Thread
import urllib.parse
stdHandler = http.server.SimpleHTTPRequestHandler

class getHandler(stdHandler):

    def do_GET(self):
        self.send_response(200)
        print(self.headers)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        try:
            query = urllib.parse.urlparse(self.path).query
        except:
            print("ERRR")
            self.wfile.write(b'')
            raise

        parameters = dict(qc.split("=") for qc in query.split("&"))

        print("params > %s " % parameters)
        #print("{} wrote:".format(self.client_address[0]) + param)
        response = self.responseFunction(parameters)

        response = str(response).encode('utf-8')
        self.wfile.write(response)
        return

def getServer(handler=getHandler, responseFunction=None, port=2999):
    if not (handler or responseFunction):
        exit("useless server")

    handler.responseFunction = responseFunction
    ADDR = ("", port)
    TCPServer = http.server.HTTPServer(ADDR, handler)
    #server = Thread(target=TCPServer.serve_forever)
    TCPServer.serve_forever()
    server.start()

    return TCPServer

