import threading

orders_lock = threading.Lock()
orders = []
orders_id = 0
received_orders = []

def orders_pop(index):
    with orders_lock:
        return orders.pop(index)

def order_append(item):
    with orders_lock:
        orders.append(item)