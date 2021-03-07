from light_switch import LightSwitch
from fei.ppds import Semaphore, Mutex


class CounterShared:
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def count(self):
        self.mutex.lock()
        self.counter += 1
        self.mutex.unlock()

    def get_counter(self):
        return self.counter


class Document:
    def __init__(self):
        self.switch = LightSwitch()
        self.room_empty = Semaphore(1)
        self.access_counter = 0
        self.readers_access = 0
        self.writers_access = 0