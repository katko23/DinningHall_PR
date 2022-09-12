import Tables
import Setings
import threading
import queue
from threading import Thread


class Order(Thread):
    def __init__(self):
        Thread.__init__(self)

    id = 1
    orders = []
    queueLock = threading.Lock()
    workQueue = queue.Queue(10)
    queueLock.acquire()
    for order_nr in orders:
        workQueue.put(order_nr)
    queueLock.release()

    def run(self):
        table = [Tables.TableClass() for i in range(Setings.nr_of_tables)]
        for i in range(Setings.nr_of_tables):
            if(table[i].ocupped == False):
                table[i].orderGenerator()
                order = Order_API()
                order.items = table[i].items
                order.table_id = i
                order.order_id = self.id
                order.priority = table[i].priority
                self.orders.append(order)
            #print(table[i].items)
            self.id = self.id + 1

class Order_API:
    def __init__(self):
        self.order_id = 0
        self.table_id = 0
        self.items = []
        self.priority = 0

