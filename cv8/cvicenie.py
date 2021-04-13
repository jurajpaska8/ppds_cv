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
            print(f'Task {name}, total = {total}')


if __name__ == '__main__':
    q = queue.Queue()
    for w in [2, 5, 8, 6]:
        q.put(w)

    tasks = [(task, 'One', q), (task, 'Two', q)]

    for t, n, q in tasks:
        t(n, q)
