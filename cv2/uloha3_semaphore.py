from fei.ppds import print, Mutex, Thread, Event, Semaphore
from time import sleep
from random import randint


class FibonacciShared:
    def __init__(self, size):
        self.size = size
        self.array = [0] * size
        self.array[1] = 1
        self.index = 2
        # for #0 and #1 we do not need Threads and therefore we do not need signalization
        self.semaphore_list = [Semaphore(0) for _ in range(size - 2)]

    def count_member(self, idx):
        self.array[idx] = self.array[idx - 1] + self.array[idx - 2]


def count_member_synchronized(fsh, thread_idx):
    sleep(randint(1, 10) / 10)
    if thread_idx != 0:
        fsh.semaphore_list[thread_idx].wait()
    fsh.count_member(fsh.index)
    print("ThreadId: %d , fibonacci value: %d " % (thread_idx, fsh.array[fsh.index]))
    fsh.index += 1
    if fsh.index < fsh.size:
        fsh.semaphore_list[thread_idx + 1].signal()


thread_count = 20
fibonacci_count = thread_count + 2
fib = FibonacciShared(fibonacci_count)
threads = list()
for i in range(thread_count):
    threads.append(Thread(count_member_synchronized, fib, i))

for t in threads:
    t.join()
