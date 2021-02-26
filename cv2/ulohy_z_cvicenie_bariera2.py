from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore

from cv2.ulohy_z_cvicenia import SimpleBarrier

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


def barrier_example2(thread_name, barrier1, barrier2):
    """Kazde vlakno vykonava kod funkcie 'barrier_example'.
    Doplnte synchronizaciu tak, aby sa vsetky vlakna pockali
    nielen pred vykonanim funkcie 'ko', ale aj
    *vzdy* pred zacatim vykonavania funkcie 'rendezvous'.
    """
    while True:
        # ...
        barrier2.wait()

        rendezvous(thread_name)
        # ...
        barrier1.wait()

        ko(thread_name)



"""Vytvorime vlakna, ktore chceme synchronizovat.
Nezabudnime vytvorit aj zdielane synchronizacne objekty,
a dat ich ako argumenty kazdemu vlaknu, ktore chceme pomocou nich
synchronizovat.
"""
sem1 = SimpleBarrier(5)
sem2 = SimpleBarrier(5)
threads = list()
for i in range(5):
    t = Thread(barrier_example2, 'Thread %d' % i, sem1, sem2)
    threads.append(t)

for t in threads:
    t.join()
