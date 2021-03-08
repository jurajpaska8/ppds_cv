from time import sleep
from fei.ppds import randint, Thread
from readers_writers_classes import Document


def reader(document, thread_id, avg_read_time, break_iter):
    while True:
        # randomness
        sleep(randint(0, 100) / 1000)
        print(f"{thread_id}. Reader before document access.")

        # wait for turnstile
        document.turn.wait()
        # signal to turnstile
        document.turn.signal()

        # reader trying to read document
        document.switch.lock(document.room_empty)
        if document.access_counter >= break_iter:
            print("Break")
        print(f"{thread_id}. Writer after action.")

        # reader action
        sleep(randint(0, 2 * avg_read_time) / 1000)
        document.access_counter += 1
        document.readers_access += 1
        print(f"{thread_id}. Reader after action.")

        # reader leaving document
        document.switch.unlock(document.room_empty)
        print(f"{thread_id}. Reader after document access")


def writer(document, thread_id, avg_read_time, break_iter):
    while True:
        # randomness
        sleep(randint(0, 100) / 1000)

        # wait for turnstile
        print(f"{thread_id}. Writer before document access.")
        document.turn.wait()

        # writer trying to get access
        document.room_empty.wait()
        if document.access_counter >= break_iter:
            print("Break")
        print(f"{thread_id}. Writer after action.")

        # action
        sleep(randint(0, 2 * avg_read_time) / 1000)
        document.access_counter += 1
        document.writers_access += 1

        # writer leaving document
        document.room_empty.signal()

        # signal to turnstile
        document.turn.signal()
        print(f"{thread_id}. Writer after document access")


# # document creating
# doc = Document()
# # threads creating
# threads = []
# for i in range(100):
#     t = Thread(writer, doc, i)
#     threads.append(t)
#
# for i in range(100):
#     t = Thread(reader, doc, i)
#     threads.append(t)
#
# for t in threads:
#     t.join()
