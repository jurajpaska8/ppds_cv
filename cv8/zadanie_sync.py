import asyncio
import time

from aiofile import async_open


class Shared:
    def __init__(self):
        self.counter = 0


async def write(tid, shared, afp):
    time_start = time.perf_counter()
    while shared.counter < 10:
        print(f'id: {tid}, ctr: {shared.counter}')
        shared.counter += 1
        await afp.write(f"id: {tid}, ctr: {shared.counter}\n" + f"{shared.counter - 1}" * 100000000 + "\n")
    print(f'ctr: {shared.counter} time {time.perf_counter() - time_start :.1f}')


async def main():
    """
    2 korutiny zapisuju asynchronne do suboru - 1 GB trva cca 2 sekundy
    """
    async with async_open("text_async.txt", 'w+') as afp:
        shared = Shared()
        a = write(0, shared, afp)
        b = write(1, shared, afp)
        start_time = time.perf_counter()
        await asyncio.gather(a, b)
        elapsed = time.perf_counter() - start_time
        print(f"\nTotal elapsed time: {elapsed:.1f}")


def write_sync(tid, shared, fp):
    time_start = time.perf_counter()
    while shared.counter < 10:
        print(f'id: {tid}, ctr: {shared.counter}')
        shared.counter += 1
        fp.write(f"id: {tid}, ctr: {shared.counter}\n" + f"{shared.counter - 1}"*100000000 + "\n")
        yield
    print(f'ctr: {shared.counter} time {time.perf_counter() - time_start :.1f}')


def main_sync():
    """
    2 generatory zapisuju synchronne do suboru - 1 GB trva cca 8 sekund
    """
    with open("text_sync.txt", 'w+') as fp:
        shared = Shared()
        a = write_sync(0, shared, fp)
        b = write_sync(1, shared, fp)
        tasks = [a, b]

        start_time = time.perf_counter()
        done = False
        while not done:
            for t in tasks:
                try:
                    next(t)
                except StopIteration:
                    tasks.remove(t)
                if len(tasks) == 0:
                    done = True
        elapsed = time.perf_counter() - start_time
        print(f"\nTotal elapsed time: {elapsed:.1f}")


if __name__ == '__main__':
    asyncio.run(main())
    main_sync()
