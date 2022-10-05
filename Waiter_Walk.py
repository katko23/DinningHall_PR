import Setings
import WaiterSocket


waiters = [WaiterSocket.Waiter(i) for i in range(Setings.nr_of_waiters)]
def waiters_walking_func():
    for i in range(Setings.nr_of_waiters):
        waiters[i].start()

