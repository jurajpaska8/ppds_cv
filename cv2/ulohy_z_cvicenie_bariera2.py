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


def rendezvous(thread_name):
    sleep(randint(1, 10) / 10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1, 10) / 10)


def barrier_example(thread_name, mutex, semaphore1, semaphore2, shared, N):
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
            semaphore1.signal(N)
        mutex.unlock()
        semaphore1.wait()
        # semaphore1.signal()

        ko(thread_name)

        mutex.lock()
        if shared.counter == N:
            semaphore2.signal(N)
            shared.counter = 0
        mutex.unlock()
        semaphore2.wait()


"""Vytvorime vlakna, ktore chceme synchronizovat.
Nezabudnime vytvorit aj zdielane synchronizacne objekty,
a dat ich ako argumenty kazdemu vlaknu, ktore chceme pomocou nich
synchronizovat.
"""
mut = Mutex()
sem1 = Semaphore(0)
sem2 = Semaphore(0)
sh = Shared()
threads = list()
for i in range(5):
    t = Thread(barrier_example, 'Thread %d' % i, mut, sem1, sem2, sh, 5)
    threads.append(t)

for t in threads:
    t.join()
