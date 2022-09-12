import socket
import Setings
import MaxWait
import time,datetime
from threading import Thread

class Waiter(Thread):
    def __init__(self,o_l,id):
        Thread.__init__(self)
        self.waiter_order_list = o_l.pop(0)
        self.id_waiter = id

        print("order of  waiter :")
        print(o_l)

    def run(self):
        self.setbody(self.waiter_order_list.order_id,self.waiter_order_list.table_id,self.id_waiter,self.waiter_order_list.items,self.waiter_order_list.priority)
        self.send()


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
        self.body = '"order_id":' + str(order_id) + ',' \
                '"table_id":' + str(table_id) + ',' \
                '"waiter_id":' + str(waiter_id) + ',' \
                '"items":' + str(items) + ',' \
                '"priority":' + str(priority) + ',' \
                '"max_wait":' + str(self.max_waiting(items)) + ',' \
                '"pick_up_time"' + str(self.pick_up_time()) + '// UNIX timestamp'

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
