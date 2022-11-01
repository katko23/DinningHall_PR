# Python 3 server example
import SocketServer,Tables_List,Order,Waiter_Walk,Registration
from threading import Thread

if __name__ == "__main__":
    server = SocketServer.Server()
    server.start()

    orders_D = Order.Order()

    thread_tables = Thread(target=Tables_List.tables_init())
    # thread_tables.start()
    # Tables_List.table_init()

    thread_waiters = Thread(target=Waiter_Walk.waiters_walking_func())

    thread_waiters.start()

    has_regist = False
    while has_regist == False:
        import time
        # time.sleep(10)
        if ( Registration.register() ):
            has_regist = True
            print("has regist")







