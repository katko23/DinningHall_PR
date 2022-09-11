# Python 3 server example
import socket
from http.server import CGIHTTPRequestHandler, BaseHTTPRequestHandler, HTTPServer
import time
import requests
import socketserver
import logging
from flask import Flask, request

hostName = "127.12.12.128"
serverPort = 27003

class MyServer(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        print (post_data)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


webServer = socketserver.TCPServer((hostName, serverPort), MyServer)
print("Server started http://%s:%s" % (hostName, serverPort))
try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass

webServer.server_close()
print("Server stopped.")