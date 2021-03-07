from time import sleep

from fei.ppds import randint, Semaphore, Thread, Mutex
from light_switch import LightSwitch


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


def reader(document, thread_id):
    j = 0
    reader_ctr = CounterShared()
    while True:
        # randomness
        sleep(randint(0, 10) / 100)

        print(f"{thread_id}. Reader before document access.")
        # reader trying to read document
        document.switch.lock(document.room_empty)

        # reader action
        sleep(randint(0, 10) / 100)
        document.access_counter += 1
        document.readers_access += 1
        print(f"{thread_id}. Reader after action.")

        # reader leaving document
        document.switch.unlock(document.room_empty)
        reader_ctr.count()
        print(f"{thread_id}. Reader after document access")
        # j += 1


def writer(document, thread_id):
    j = 0
    while True:
        # randomness
        sleep(randint(0, 10) / 100)

        # writer trying to get access
        print(f"{thread_id}. Writer before document access.")
        document.room_empty.wait()

        # action
        sleep(randint(0, 10) / 100)
        document.access_counter += 1
        document.writers_access += 1
        if document.access_counter >= 1000:
            print("Break")
        print(f"{thread_id}. Writer after action.")

        # writer leaving document
        document.room_empty.signal()
        print(f"{thread_id}. Writer after document access")
        # j += 1


# document creating
doc = Document()
# readers parameters
readers_count = 1
read_time_average_seconds = 5
# writers parameters
writers_count = 100
writers_time_average_seconds = 5


# threads creating
threads = []
for i in range(100):
    t = Thread(writer, doc, i)
    threads.append(t)

for i in range(1):
    t = Thread(reader, doc, i)
    threads.append(t)

for t in threads:
    t.join()
