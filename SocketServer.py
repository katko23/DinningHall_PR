# Python 3 server example
import socket,Setings
from threading import Thread

hostName = Setings.serverName
serverPort = Setings.this_serverPort

class Server(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        sock = socket.socket()  # socket creation
        sock.bind((hostName, serverPort))  # socket binding on LAN
        sock.listen(4096)  # server a listen

        print('socket is listening')

        while True:
            c, addr = sock.accept()
            print('got connection from ', addr)

            jsonReceived = c.recv(1024)
            print("Json received -->", jsonReceived)

            c.close()

