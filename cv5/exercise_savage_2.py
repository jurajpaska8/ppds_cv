from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print
from exercise_savage import SimpleBarrier

savages_count = 10
pot_capacity = 13
cooks_count = 3
cook_capacity = 5


class Shared:
    def __init__(self):
        self.servings = 0
        self.mutex = Mutex()
        self.emptyPot = Semaphore(0)
        self.fullPot = Semaphore(0)

        self.barrier1 = SimpleBarrier(savages_count)
        self.barrier2 = SimpleBarrier(savages_count)


def eat(sid):
    print(f"divoch {sid}: hodujem")
    sleep(0.2 + randint(0, 3) / 10)


def get_serving_from_pot(shared, sid):
    print(f"divoch {sid}: beriem porciu. Po zobrati zostane {shared.servings - 1} porcii")
    shared.servings -= 1


def cook(shared, cid, M):
    sleep(randint(0, 10) / 1000)
    while True:
        sleep(randint(0, 10) / 1000)
        shared.emptyPot.wait()
        print(f"kuchar {cid}: idem varit. Aktualne je v hrnci = {shared.servings}")
        sleep(0.5 + randint(0, 3) / 10)
        if (shared.servings + M) < pot_capacity:
            shared.servings += M
            shared.emptyPot.signal()
            sleep(1)
        else:
            shared.servings = pot_capacity
            print(f"kuchar {cid}: dovarene. Aktualne je v hrnci = {shared.servings}")
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
        get_serving_from_pot(shared, sid)
        shared.mutex.unlock()
        eat(sid)
        shared.barrier2.wait(sid, print_last="****divoch %2d dokoncil cyklus - otvara barieru****")


def run():
    shared = Shared()
    savages = [Thread(savage, shared, sid) for sid in range(savages_count)]
    cooks = [Thread(cook, shared, cid, cook_capacity) for cid in range(cooks_count)]

    for s in savages:
        s.join()

    for c in cooks:
        c.join()


if __name__ == '__main__':
    run()
