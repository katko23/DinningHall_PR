# Python 3 server example
import SocketServer,WaiterSocket,Order,Setings
from threading import Thread

if __name__ == "__main__":
    server = SocketServer.Server()
    server.start()

    orders_D = Order.Order()
    orders_D.start()

    Waiters = [WaiterSocket.Waiter(orders_D.orders,i) for i in range(Setings.nr_of_waiters)]
    for i in range(Setings.nr_of_waiters):
        Waiters[i].start()




