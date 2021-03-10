from fei.ppds import Semaphore, Thread
from time import sleep
from random import randint


PHIL_NUM = 5


def philosopher(forks, i):
    while True:
        think(i)
        get_forks(forks, i)
        eat(i)
        put_forks(forks, i)


def think(i):
    print(f"{i:02d}: thinking")
    sleep(randint(40, 50) / 1000)


def eat(i):
    print(f"{i:02d}: eating")
    sleep(randint(40, 50) / 1000)


def get_forks(forks, i):
    # footman.wait()
    print(f"{i:02d}: try to get forks")
    forks[right(i)].wait()
    forks[left(i)].wait()
    print(f"{i:02d}: taken forks")


def put_forks(forks, i):
    forks[right(i)].signal()
    forks[left(i)].signal()
    # footman.signal()
    print(f"{i:02d}: put forks")


def right(i):
    return i


def left(i):
    return (i + 1) % PHIL_NUM


def main():
    forks_shared = [Semaphore(1) for _ in range(PHIL_NUM)]

    phils = [Thread(philosopher, forks_shared, i) for i in range(PHIL_NUM)]

    for p in phils:
        p.join()
    print("HI")


if __name__ == '__main__':
    main()
