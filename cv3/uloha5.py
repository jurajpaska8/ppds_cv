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
