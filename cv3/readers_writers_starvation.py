from time import sleep
from fei.ppds import randint, Thread


def reader(document, thread_id, avg_read_time, break_iter):
    while True:
        # randomness
        sleep(randint(0, 100) / 1000)
        # print(f"{thread_id}. Reader before document access.")

        # reader trying to read document
        document.switch.lock(document.room_empty)
        if document.access_counter >= break_iter:
            # print("Reader break")
            document.switch.unlock(document.room_empty)
            break

        # reader action
        sleep(randint(0, avg_read_time * 2) / 1000)
        document.access_counter += 1
        document.readers_access += 1
        # print(f"{thread_id}. Reader after action.")

        # reader leaving document
        document.switch.unlock(document.room_empty)
        # print(f"{thread_id}. Reader after document access")


def writer(document, thread_id, avg_write_time, break_iter):
    while True:
        # randomness
        sleep(randint(0, 100) / 1000)

        # writer trying to get access
        # print(f"{thread_id}. Writer before document access.")
        document.room_empty.wait()
        if document.access_counter >= break_iter:
            # print("Writer break")
            document.room_empty.signal()
            break

        # action
        sleep(randint(0, avg_write_time * 2) / 1000)
        document.access_counter += 1
        document.writers_access += 1
        # print(f"{thread_id}. Writer after action.")

        # writer leaving document
        document.room_empty.signal()
        # print(f"{thread_id}. Writer after document access")
