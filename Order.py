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


    def run(self):
        table = [Tables.TableClass() for i in range(Setings.nr_of_tables)]
        while True:
            for i in range(Setings.nr_of_tables):
                if (table[i].ocupped == False):
                    table[i].orderGenerator()
                    order = Order_API()
                    order.items = table[i].items
                    order.table_id = i
                    order.order_id = self.id
                    order.priority = table[i].priority
                    queueLock = threading.Lock()  # create a mutex
                    queueLock.acquire()  # stop others thread
                    self.orders.append(order)
                    queueLock.release()  # start others thread
                #else:
                    #print("_______________________________________________________________ Aici sunt toatee mesele pline")

                # print(table[i].items)
                self.id = self.id + 1

class Order_API:
    def __init__(self):
        self.order_id = 0
        self.table_id = 0
        self.items = []
        self.priority = 0

    def order_writer(self,orders):
        queueLock = threading.Lock()  # create a mutex
        workQueue = queue.Queue(10)
        queueLock.acquire()  # stop others thread
        for order_nr in orders:
            workQueue.put(order_nr)
        queueLock.release()  #start others thread
        return orders