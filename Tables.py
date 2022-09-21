import random
import time,datetime
import Order
from threading import Thread
import threading
import MaxWait
import Setings


class TableClass(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.nr_of_items = 0
        self.items = []
        self.priority = 0
        self.id = id

    ocupped = [False for i in range(Setings.nr_of_tables)]

    # def serve_oc(self):
    #     ocupatLock = threading.Lock()  # create a mutex
    #     ocupatLock.acquire()
    #     self.ocupped = False
    #     ocupatLock.release()

    def run(self):
        while True:
            if (self.ocupped[self.id - 1] == False):
                print("se ocupa")
                take_order = random.randint(3, 10)
                time.sleep(take_order * Setings.timeunit)
                self.orderGenerator()
                order = Order.Order_API()
                order.items = self.items
                order.table_id = self.id
                order.order_id = Order.Order.id
                Order.Order.id = Order.Order.id + 1
                order.max_wait = self.max_waiting(self.items)
                order.priority = self.priority_f(len(self.items), order.max_wait)
                queueLock = threading.Lock()  # create a mutex
                queueLock.acquire()  # stop others thread
                Order.Order.orders.append(order)
                queueLock.release()  # start others thread
            # else:
            #     if (len(self.ocupped) == 0):
            #         self.ocupped.append(True)
            #    print("_______________________________________________________________ Aici sunt toatee mesele pline")



    def orderGenerator(self):
        self.nr_of_items = random.randint(1, 10)
        #print("nr of items:" + str(self.nr_of_items))
        #print("priority:" + str(self.priority))
        self.items.clear()
        for i in range(self.nr_of_items):
            foodid = random.randint(1,13)
            self.items.append(foodid)

        self.ocupped[self.id - 1] = True
        #print("items" + str(self.items))

    def max_waiting(self,items):
        max = 0
        for i in range(len(items)):
            if (max < MaxWait.TimeMax[items[i]-1]):
                max = MaxWait.TimeMax[items[i]-1]
        return max

    def priority_f(self,nr_items,time):
        if (0 < (time / nr_items) and (time / nr_items) <= 5): return 5;
        if (5 < (time / nr_items) and (time / nr_items) <= 6): return 4;
        if (6 < (time / nr_items) and (time / nr_items) <= 8): return 3;
        if (8 < (time / nr_items) and (time / nr_items) <= 12): return 2;
        if (12 < (time / nr_items) and (time / nr_items) <= 46): return 1;





