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
    # eating takes same time
    print(f"divoch {sid}: hodujem")
    sleep(0.2 + randint(0, 3) / 10)


def get_serving_from_pot(shared, sid):
    # taking serving takes zero time
    print(f"divoch {sid}: beriem porciu. Zostane {shared.servings - 1} porcii")
    shared.servings -= 1


def cook(shared, cid, cook_cap):
    # shuffle cooks before hitting semaphore
    sleep(randint(0, 10) / 1000)

    while True:
        # wait until pot is empty
        shared.emptyPot.wait()
        # cooking takes some time
        print(f"kuchar {cid}: idem varit. Obsah hrnca = {shared.servings}")
        sleep(0.5 + randint(0, 3) / 10)

        # if current cook does not fill pot
        if (shared.servings + cook_cap) < pot_capacity:
            # put servings into pot
            shared.servings += cook_cap
            # and give signal to another cook
            shared.emptyPot.signal()
            # then rest
            sleep(1)
        # if current cook fills pot
        else:
            # avoid "pot overflow" by setting servings count to pot capacity
            shared.servings = pot_capacity
            print(f"kuchar {cid}: dovarene. Obsah hrnca = {shared.servings}")
            # and give signal to savages
            shared.fullPot.signal()


def savage(shared, sid):
    # shuffle savage before hitting barrier
    sleep(randint(0, 10) / 1000)

    while True:
        # wait until all savages came to dinner
        shared.barrier1.wait(sid,
                             print_each="divoch %2d:uz nas je %2d",
                             print_last="divoch %2d:sme vsetci, mozme vecerat")
        # serialize access to the pot
        shared.mutex.lock()
        print(f"divoch {sid}: pocet zostavajucich porcii = {shared.servings}")

        # if pot is empty
        if shared.servings == 0:
            print(f"divoch {sid}: budim kuchara")
            # wake up cook
            shared.emptyPot.signal()
            # wait until they fill the pot
            shared.fullPot.wait()

        # if there is at least one serving, grab it and unlock mutex
        get_serving_from_pot(shared, sid)
        shared.mutex.unlock()
        # eating can be done out of serialized part
        eat(sid)
        # wait until all savages finish dinner
        shared.barrier2.wait(sid, print_last="***divoch %2d otvara barieru***")


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
