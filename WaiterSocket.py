import socket
import Setings
import MaxWait
import time,datetime
import Order as O_Class
from threading import Thread
import threading

class Waiter(Thread):
    def __init__(self,id):
        Thread.__init__(self)
        self.id_waiter = id
        #print("order of  waiter :")
        #print(o_l)

    def run(self):
        while True:
            queueLock = threading.Lock()  # create a mutex
            queueLock.acquire()  # stop others thread
            if(len(O_Class.Order.orders) > 0):
                waiter_order_list = O_Class.Order.orders.pop(0)
                self.setbody(waiter_order_list.order_id, waiter_order_list.table_id, self.id_waiter,
                             waiter_order_list.items, waiter_order_list.priority)
                self.send()
            queueLock.release()  # resume other threads


    host = Setings.hostName
    port = Setings.serverPort
    headers = """\
POST /order HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Host: {host}\r
Connection: close\r
\r\n"""
    body = ""

    def setbody(self, order_id, table_id, waiter_id, items, priority):
        self.body = \
            '"order_id":' + str(order_id) + ',\n' \
            '"table_id":' + str(table_id+1) + ',\n' \
            '"waiter_id":' + str(waiter_id+1) + ',\n' \
            '"items":' + str(items) + ',\n' \
            '"priority":' + str(priority) + ',\n' \
            '"max_wait":' + str(self.max_waiting(items)) + ',\n' \
            '"pick_up_time":' + str(self.pick_up_time())

    def pick_up_time(self):
        presentDate = datetime.datetime.now()
        unix_timestamp = datetime.datetime.timestamp(presentDate) * 1000
        return unix_timestamp

    def max_waiting(self,items):
        max = 0
        for i in range(len(items)):
            if (max < MaxWait.TimeMax[i]):
                max = MaxWait.TimeMax[i]
        return max

    def send(self):
        body_bytes = self.body.encode('ascii')
        header_bytes = self.headers.format(
            content_type="application/json",
            content_length=len(body_bytes),
            host=str(self.host) + ":" + str(self.port)
        ).encode('iso-8859-1')

        payload = header_bytes + body_bytes

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))

        s.sendall(payload)
        print(s.recv(1024))

