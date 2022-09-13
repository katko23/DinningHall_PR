# Python 3 server example
import threading

import SocketServer,WaiterSocket,Order,Setings,Waiter_Walk
from threading import Thread

if __name__ == "__main__":
    server = SocketServer.Server()
    server.start()

    orders_D = Order.Order()
    orders_D.start()

    waiters = [WaiterSocket.Waiter(i) for i in range(Setings.nr_of_waiters)]
    for i in range(Setings.nr_of_waiters):
        waiters[i].start()







