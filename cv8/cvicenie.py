import queue

import time


def task(name: str, q: queue.Queue):
    if q.empty():
        print(f'Task {name} done')
    else:
        while not q.empty():
            delay = q.get()
            print(f'Task {name} running')
            time_start = time.perf_counter()
            time.sleep(delay)
            elapsed = time.perf_counter() - time_start
            print(f'Task {name}, elapsed time = {elapsed}')
            yield


if __name__ == '__main__':
    qu = queue.Queue()
    for w in [3, 5, 8, 7]:
        qu.put(w)

    one = task('One', qu)
    two = task('Two', qu)
    tasks = [one, two]

    # run
    done = False
    start_time = time.perf_counter()
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
                print(f"koniec {t}")
                if len(tasks) == 0:
                    done = True
    elapsed = time.perf_counter() - start_time
    print(f"\nTotal elapsed time: {elapsed:.1f}")