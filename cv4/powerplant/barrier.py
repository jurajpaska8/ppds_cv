from fei.ppds import Mutex, Event


class BarrierUsingEvent:
    def __init__(self, N):
        self.N = N
        self.cnt = 0
        self.mutex = Mutex()
        self.event = Event()

    def increment_and_wait(self):
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == self.N:
            self.cnt = 0
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()

    def wait(self):
        self.event.wait()
