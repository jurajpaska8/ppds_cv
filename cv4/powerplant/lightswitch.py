from fei.ppds import Mutex


class LightSwitch(object):
    def __init__(self):
        self.mutex = Mutex()
        self.cnt = 0

    def lock(self, sem):
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == 1:
            sem.wait()
        self.mutex.unlock()
        return self.cnt

    def unlock(self, sem):
        self.mutex.lock()
        self.cnt -= 1
        if self.cnt == 0:
            sem.signal()
        self.mutex.unlock()
        return self.cnt
