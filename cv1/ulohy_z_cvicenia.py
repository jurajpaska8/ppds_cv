from fei.ppds import Mutex


class Shared:
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end
        self.mutex = Mutex()


class Histogram(dict):
    def __init__(self, seq=[]):
        super().__init__()
        for item in seq:
            self[item] = self.get(item, 0) + 1


# def counter(sh):
#     # sh.mutex.lock()
#     while True:
#         if sh.counter >= sh.end:
#             break
#         sh.array[sh.counter] += 1
#         sh.counter += 1
#     # sh.mutex.unlock()
#
#
# for i in range(10):
#     shared = Shared(1_000_000)
#     thread1 = Thread(counter, shared)
#     thread2 = Thread(counter, shared)
#
#     thread1.join()
#     thread2.join()
#
#     print(Histogram(shared.array))
