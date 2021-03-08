from readers_writers_classes import Document
from fei.ppds import Thread, print
from readers_writers_starvation import reader, writer

# writers parameters
writers_count = 10
# average writers time in milliseconds
writers_time_average_ms = 50
# number of writer accesses
writers_accesses = []

# list of readers count
readers_count = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# list of readers average time in ms
readers_avg_time = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# number of iterations for each setting
itrs = 10
# number of all accesses (readers and writers combined) in each iter
break_iter = 100

for r in readers_count:
    print(f"START: Number of readers = {r}")
    for time in readers_avg_time:
        print(f"Avg read time = {time} ms")
        # number of writer accesses for each setting
        tmp_writers = 0
        for itr in range(itrs):
            print(f"iter = {itr}")
            # document creating
            doc = Document()
            # threads creating
            threads = []

            # writer threads
            for i in range(writers_count):
                t = Thread(writer, doc, i, writers_time_average_ms, break_iter)
                threads.append(t)

            # reader threads
            for i in range(r):
                t = Thread(reader, doc, i, time, break_iter)
                threads.append(t)

            for t in threads:
                t.join()

            tmp_writers += doc.writers_access
        print(f"Writer accesses for {r} readers and avg time {time} ms = {tmp_writers / 10} of {break_iter}")
        writers_accesses.append(tmp_writers / itrs)
