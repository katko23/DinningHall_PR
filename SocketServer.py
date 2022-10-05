# Python 3 server example
import json
import socket,Setings
import threading
from threading import Thread
from flask import Flask, render_template, request, url_for, jsonify


hostName = Setings.serverName
serverPort = Setings.this_serverPort

class Server(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        app = Flask(__name__)

        @app.route('/distribution', methods=['POST'])
        def my_test_endpoint():
            from Waiter_Walk import waiters
            input_json = request.get_json(force=True)
            # force=True, above, is necessary if another developer
            # forgot to set the MIME type to 'application/json'
            print('data from client:', input_json)
            temp = json.loads(input_json)
            waiters[int(temp['waiter_id']) - 1].orders_done.append(temp)
            dictToReturn = {'answer': "Dinning Hall received"}
            return jsonify(dictToReturn)

        app.run(host=hostName, port=serverPort, debug=False)

#         sock = socket.socket()  # socket creation
#         sock.bind((hostName, serverPort))  # socket binding on LAN
#         sock.listen(4096)  # server a listen
#
#         print('socket is listening')
#
#         while True:
#             c, addr = sock.accept()
#             print('got connection from ', addr)
#
#             jsonReceived = c.recv(1024)
# #            recvs = self.data_received(jsonReceived)
# #           ordersLock = threading.Lock()  # create a mutex
# #            ordersLock.acquire()
# #           Order.Orders.orders_done.append(recvs)
# #           ordersLock.release()
#             print("Json received -->\n", jsonReceived,"\n")
#
#
#
#             c.close()

    # def data_received(self,temp):
    #     string = temp.split("\n")
    #     for i in range(6):
    #         string.pop(0)
    #     dictionary = dict()
    #     for i in string:
    #         words = i.split(":")
    #         secondWord = str(words[1]).split(",")
    #         if(len(words) > 0):
    #             dictionary.update({str(words[0]) : str(secondWord[0])})
    #     return dictionary