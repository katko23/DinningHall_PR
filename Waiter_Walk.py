import Setings


def waiters_walking_func(waiters):
    for i in range(Setings.nr_of_waiters):
        waiters[i].start()

