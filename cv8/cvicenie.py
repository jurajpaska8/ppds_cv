import asyncio

import time


async def task(name: str, q: asyncio.Queue):
    if q.empty():
        print(f'Task {name} done')
    else:
        while not q.empty():
            delay = await q.get()
            print(f'Task {name} running')
            time_start = time.perf_counter()
            await asyncio.sleep(delay)
            elapsed = time.perf_counter() - time_start
            print(f'Task {name}, elapsed time = {elapsed}')


async def main():
    qu = asyncio.Queue()
    for w in [3, 5, 8, 7]:
        await qu.put(w)

    one = task('One', qu)
    two = task('Two', qu)

    # run
    start_time = time.perf_counter()
    await asyncio.gather(one, two)
    elapsed = time.perf_counter() - start_time
    print(f"\nTotal elapsed time: {elapsed:.1f}")


if __name__ == '__main__':
    asyncio.run(main())
