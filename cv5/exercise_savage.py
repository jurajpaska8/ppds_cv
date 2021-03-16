from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print

N = 10
M = 13


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.cnt = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)

    def wait(self,
             sid,
             print_last=None,
             print_each=None):
        self.mutex.lock()
        self.cnt += 1
        if print_each:
            print(print_each % (sid, self.cnt))
        if self.cnt == self.N:
            self.cnt = 0
            if print_last:
                print(print_last % sid)
            self.turnstile.signal(self.N)
        self.mutex.unlock()
        self.turnstile.wait()


class Shared:
    def __init__(self):
        self.servings = 0
        self.mutex = Mutex()
        self.emptyPot = Semaphore(0)
        self.fullPot = Semaphore(0)

        self.barrier1 = SimpleBarrier(N)
        self.barrier2 = SimpleBarrier(N)


def eat(sid):
    print(f"divoch {sid}: hodujem")
    sleep(0.2 + randint(0, 3) / 10)


def getServingFromPot(shared, sid):
    print(f"divoch {sid}: beriem porciu. Po zobrati zostane {shared.servings - 1} porcii")
    shared.servings -= 1


def putServingInPot(shared, M):
    print(f"Kuchar: varim. Pocet porcii bol = {shared.servings}")
    sleep(0.5 + randint(0, 3) / 10)
    shared.servings += M


def cook(shared, M):
    while True:
        shared.emptyPot.wait()
        putServingInPot(shared, M)
        shared.fullPot.signal()


def savage(shared, sid):
    sleep(randint(0, 10) / 1000)
    while True:
        shared.barrier1.wait(sid,
                             print_each="divoch %2d: prisiel som na veceru, uz nas je %2d",
                             print_last="divoch %2d: uz sme vsetci, mozme vecerat")
        shared.mutex.lock()
        print(f"divoch {sid}: pocet zostavajucich porcii = {shared.servings}")
        if shared.servings == 0:
            print(f"divoch {sid}: budim kuchara")
            shared.emptyPot.signal()
            shared.fullPot.wait()
        getServingFromPot(shared, sid)
        shared.mutex.unlock()
        eat(sid)
        shared.barrier2.wait(sid, print_last="****divoch %2d dokoncil cyklus - otvara barieru****")


def run():
    shared = Shared()
    savages = [Thread(savage, shared, sid) for sid in range(N)]
    savages.append(Thread(cook, shared, M))


if __name__ == '__main__':
    run()
