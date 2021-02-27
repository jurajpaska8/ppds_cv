from fei.ppds import print, Mutex, Thread, Event, Semaphore
from time import sleep
from random import randint


class FibonacciShared:
    def __init__(self, size):
        self.size = size
        self.array = [0] * size
        self.array[1] = 1
        self.index = 2
        self.mutex = Mutex()


def count_member(fsh, idx):
    sleep(randint(1, 10) / 10)
    if idx == fsh.index:
        fsh.mutex.lock()
        fsh.array[idx] = fsh.array[idx - 1] + fsh.array[idx - 2]
        print(fsh.array[idx])
        print("ThreadId %d " % (idx - 2))
        fsh.index += 1
        fsh.mutex.unlock()


thread_count = 10
fibonacci_count = thread_count + 2
fib = FibonacciShared(fibonacci_count)
threads = list()
for i in range(2, fibonacci_count):
    threads.append(Thread(count_member, fib, i))

for t in threads:
    t.join()
