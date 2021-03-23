from random import randint
from time import sleep

from fei.ppds import print, Mutex, Semaphore, Thread

from cv2.ulohy_z_cvicenia import SimpleBarrier


class Shared:
    def __init__(self, atoms_count):
        self.atoms_count = atoms_count
        self.hydro_count = 0
        self.oxy_count = 0
        self.mol_count = 0

        self.mutex = Mutex()
        self.mol_count_mutex = Mutex()
        self.barrier = SimpleBarrier(atoms_count)
        self.oxy_queue = Semaphore(0)
        self.hydro_queue = Semaphore(0)


def bond(print_str):
    sleep(randint(0, 10) / 10)
    print(f"{print_str}")


def hydrogen(shared, idx):
    sleep(randint(1, 10) / 10)
    print(f"Vodik id = {idx}")
    shared.mutex.lock()
    shared.hydro_count += 1
    if shared.hydro_count < 2 or shared.oxy_count < 1:
        shared.mutex.unlock()
    else:
        shared.hydro_count -= 2
        shared.oxy_count -= 1
        shared.oxy_queue.signal()
        shared.hydro_queue.signal(2)

    shared.hydro_queue.wait()
    bond(f"Vodik {idx}: Vytvaram molekulu id = {shared.mol_count}")
    shared.barrier.wait()


def oxygen(shared, idx):
    sleep(randint(1, 10) / 10)
    print(f"Kyslik id = {idx}")
    shared.mutex.lock()
    shared.oxy_count += 1
    if shared.hydro_count < 2 or shared.oxy_count < 1:
        shared.mutex.unlock()
    else:
        shared.hydro_count -= 2
        shared.oxy_count -= 1
        shared.oxy_queue.signal()
        shared.hydro_queue.signal(2)

    shared.oxy_queue.wait()
    bond(f"Kyslik {idx}: Vytvaram molekulu id = {shared.mol_count}")
    shared.barrier.wait()
    shared.mutex.unlock()

    shared.mol_count_mutex.lock()
    shared.mol_count += 1
    shared.mol_count_mutex.unlock()


def create_and_run_threads():
    sh = Shared(3)
    hydrogens = [Thread(hydrogen, sh, i) for i in range(50)]
    oxygens = [Thread(oxygen, sh, i) for i in range(25)]

    for h in hydrogens:
        h.join()

    for o in oxygens:
        o.join()


if __name__ == '__main__':
    create_and_run_threads()
    print("End")
