from time import sleep
from fei.ppds import Event, print, Mutex, Semaphore, Thread
from random import randint


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.cnt = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == self.N:
            self.cnt = 0
            self.turnstile.signal(self.N)
        self.mutex.unlock()
        self.turnstile.wait()


def barrier_example(barrier, thread_id):
    """Predpokladajme, ze nas program vytvara a spusta 5 vlakien,
    ktore vykonavaju nasledovnu funkciu, ktorej argumentom je
    zdielany objekt jednoduchej bariery
    """
    sleep(randint(1, 10) / 10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %d po bariere" % thread_id)


# priklad pouzitia ADT SimpleBarrier
# sb = SimpleBarrier(5)
# threads = list()
# for i in range(5):
#     t = Thread(barrier_example, sb, i)
#     threads.append(t)
#
# for t in threads:
#     t.join()
