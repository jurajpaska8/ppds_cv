import queue


def task(name: str, q: queue.Queue):
    if q.empty():
        print(f'Task {name} done')
    else:
        while not q.empty():
            c = q.get()
            total = 0
            print(f'Task {name} running')
            for x in range(c):
                total += 1
                yield
            print(f'Task {name}, total = {total}')


if __name__ == '__main__':
    q = queue.Queue()
    for w in [2, 5, 8, 6]:
        q.put(w)

    one = task('One', q)
    two = task('Two', q)
    tasks = [one, two]

    # run
    done = False
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
                print(f"koniec {t}")
                if len(tasks) == 0:
                    done = True
