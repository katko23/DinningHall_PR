# Python 3 server example
import json
import socket,Setings
import math
import time
from threading import Thread
import Food_Ordering_Plates as FOS
import requests
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
            temp = input_json.copy()
            if 'restaurant_id' in temp:
                print("Client Order Done", input_json);
                FOS.order_append(input_json)
            else:
                print('data from client:', input_json)
                waiters[int(temp['waiter_id']) - 1].orders_done.append(temp)
            dictToReturn = {'answer': "Dinning Hall received"}
            return jsonify(dictToReturn)

        @app.route('/v1/order', methods=['POST'])
        def ordering():
            input_json = request.get_json(force=True)
            # force=True, above, is necessary if another developer
            # forgot to set the MIME type to 'application/json'
            print('data from client:', input_json)
            dictToSend = input_json.copy()
            dictToSend['pick_up_time'] = dictToSend['created_time']
            dictToSend.pop('created_time')
            dictToSend['order_id'] = FOS.orders_id
            dictToSend['registered_time'] = time.time()
            res = requests.post("http://" + str(Setings.hostName) + ":" + str(Setings.serverPort) + "/order", json=dictToSend)
            print('response from Kitchen:', res.text)
            dictres = res.json()  #dictionary from Kitchen as response
            input_json['estimated_waiting_time'] = math.ceil(Setings.wt * (dictres["Plates_on_prepairing"] + len(input_json['items'])) / len(input_json['items']))
            dictToReturn = input_json.copy()
            input_json['restaurant_id'] = Setings.restaurant_id
            input_json['is_ready'] = False
            dictToReturn['created_time'] = dictToSend['pick_up_time']
            dictToReturn['restaurant_id'] = Setings.restaurant_id
            dictToReturn['restaurant_address'] = Setings.serverName + ":" + str(Setings.this_serverPort)
            FOS.orders_lock.acquire()
            FOS.orders_id = FOS.orders_id + 1
            dictToReturn['order_id'] = FOS.orders_id
            input_json['order_id'] = FOS.orders_id
            input_json["prepared_time"] = 0
            input_json["cooking_time"] = 0
            input_json["cooking_details"] = None
            dictToReturn['registered_time'] = dictToSend['registered_time']
            input_json['registered_time'] = dictToReturn['registered_time']
            FOS.received_orders.append(input_json)
            FOS.orders_lock.release()

            dictToReturn.pop('items')
            dictToReturn.pop('priority')
            dictToReturn.pop('max_wait')
            return jsonify(dictToReturn)

        @app.route('/v1/order/<int:Number>', methods=['GET'])
        def check(Number):
            print(Number)
            dictToReturn = {}
            for o in FOS.orders:
                if o['order_id'] == Number:
                    dictToReturn["order_id"] = o['order_id']
                    dictToReturn["is_ready"] = True
                    dictToReturn["estimated_waiting_time"] = 0
                    dictToReturn["priority"] = o['priority']
                    dictToReturn["max_wait"] = o['max_wait']
                    dictToReturn["created_time"] = o['pick_up_time']
                    dictToReturn["registered_time"] = o['registered_time']
                    dictToReturn["prepared_time"] = o['registered_time'] + o['cooking_time']
                    dictToReturn['cooking_time'] = o['cooking_time']
                    dictToReturn["cooking_details"] = o['cooking_details']
                    return jsonify(dictToReturn)
            dictToReturn["order_id"] = Number
            dictToReturn["is_ready"] = False
            dictToReturn["priority"] = 3
            dictToReturn["prepared_time"] = 0
            dictToReturn['cooking_time'] = 0
            dictToReturn["cooking_details"] = None
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