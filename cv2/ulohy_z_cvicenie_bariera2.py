from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore

"""Vypisovat na monitor budeme pri zamknutom mutexe pomocou
funkcie 'print' z modulu 'fei.ppds', aby sme nemali rozbite vypisy.
"""
from fei.ppds import print


class Shared:
    def __init__(self):
        self.counter = 0
        #self.mutex = Mutex()


class ReusableBarrier:
    def __init__(self, N):
        self.N = N
        self.cnt = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore()

    def wait(self):
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == self.N:
            self.turnstile.signal()
        self.mutex.unlock()
        self.turnstile.wait()
        self.turnstile.signal()


def rendezvous(thread_name):
    sleep(randint(1, 10) / 10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1, 10) / 10)


def barrier_example(thread_name, mutex, semaphore, shared, N):
    """Kazde vlakno vykonava kod funkcie 'barrier_example'.
    Doplnte synchronizaciu tak, aby sa vsetky vlakna pockali
    nielen pred vykonanim funkcie 'ko', ale aj
    *vzdy* pred zacatim vykonavania funkcie 'rendezvous'.
    """
    while True:
        # ...
        rendezvous(thread_name)
        # ...
        mutex.lock()
        shared.counter += 1
        if shared.counter == N:
            semaphore.signal()
        mutex.unlock()
        semaphore.wait()
        semaphore.signal()

        ko(thread_name)

        mutex.lock()
        if shared.counter == N:
            semaphore.wait()
            shared.counter -= 1
        mutex.unlock()


"""Vytvorime vlakna, ktore chceme synchronizovat.
Nezabudnime vytvorit aj zdielane synchronizacne objekty,
a dat ich ako argumenty kazdemu vlaknu, ktore chceme pomocou nich
synchronizovat.
"""
mut = Mutex()
sem = Semaphore(0)
sh = Shared()
threads = list()
for i in range(5):
    t = Thread(barrier_example, 'Thread %d' % i, mut, sem, sh, 5)
    threads.append(t)

for t in threads:
    t.join()
