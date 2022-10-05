import random
import socket
import Setings
import MaxWait
import time,datetime
import Order as O_Class
from threading import Thread
import threading
import requests
import Tables_List

class Waiter(Thread):
    def __init__(self,id):
        Thread.__init__(self)
        self.id_waiter = id
        #self.tables_list = tables
        #print("order of  waiter :")
        #print(o_l)

    def run(self):
        while True:
            import Order
            queueLock = threading.Lock()  # create a mutex
            queueLock.acquire()  # stop others thread
            Order.Order.orders_lock.acquire()
            if(len(O_Class.Order.orders) > 0):
                waiter_take_order = random.randint(2, 4)
                time.sleep(waiter_take_order * Setings.timeunit)
                waiter_order_list = O_Class.Order.orders.pop(0)
                self.setbody(waiter_order_list.order_id, waiter_order_list.table_id, self.id_waiter,
                             waiter_order_list.items, waiter_order_list.priority, waiter_order_list.max_wait)
                self.send()
            Order.Order.orders_lock.release()
            queueLock.release()  # resume other threads
            self.serve()

    orders_done = []
    host = Setings.hostName
    port = Setings.serverPort
    headers = """\
POST /order HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Host: {host}\r
Connection: close\r
\r\n"""
    body = {}

    def setbody(self, order_id, table_id, waiter_id, items, priority, max_wait):
        self.body = {
            "order_id":order_id,
            "table_id":table_id + 1,
            "waiter_id":waiter_id + 1,
            "items":items,
            "priority":priority,
            "max_wait":max_wait,
            "pick_up_time":self.pick_up_time()}
        # self.body = \
        #     '"order_id":' + str(order_id) + ',\n' \
        #     '"table_id":' + str(table_id + 1) + ',\n' \
        #     '"waiter_id":' + str(waiter_id + 1) + ',\n' \
        #     '"items":' + str(items) + ',\n' \
        #     '"priority":' + str(priority) + ',\n' \
        #     '"max_wait":' + str(self.max_waiting(items)) + ',\n' \
        #     '"pick_up_time":' + str(self.pick_up_time())

    def pick_up_time(self):
        unix_timestamp = time.time()
        return unix_timestamp


    def send(self):
        dictToSend = self.body
        res = requests.post("http://"+str(self.host)+":"+str(self.port)+"/order", json=dictToSend)
        print('response from server:', res.text)
        dictFromServer = res.json()

        # body_bytes = self.body.encode('ascii')
        # header_bytes = self.headers.format(
        #     content_type="application/json",
        #     content_length=len(body_bytes),
        #     host=str(self.host) + ":" + str(self.port)
        # ).encode('iso-8859-1')
        #
        # payload = header_bytes + body_bytes
        #
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect((self.host, self.port))
        #
        # s.sendall(payload)
        # print(s.recv(1024))

    def serve(self):
        import Tables
        if(len(self.orders_done)>0):
            serveLock = threading.Lock()  # create a mutex
            serveLock.acquire()
            serving = self.orders_done.pop(0)
            print("\n\n",serving,"\n\n")
            #Tables_List.tables[serving['table_id'] - 1].ocupped = False
            #temp = Tables_List.tables[serving['table_id'] - 1]
            #temp.ocupped = False
            Tables.TableClass.tclock.acquire()
            Tables_List.tables[serving['table_id'] - 1].deocupped()
            print(Tables_List.tables[serving['table_id'] - 1].ocupped)
            Tables.TableClass.tclock.release()
            print("order with id ", serving['order_id'], " was served by waiter nr ", serving['waiter_id'])
            serveLock.release() #release mutex


