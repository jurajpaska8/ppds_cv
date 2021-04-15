"""
kazda korutina zapise raz za sekundu riadok vo forme [id korutiny, cislo zapisu, cas zapisu, hodnota z pola] do suboru
"""
import asyncio
import time

from aiofile import async_open


class Shared:
    def __init__(self):
        self.counter = 0
        self.list = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


async def write(tid, shared, afp):
    time_start = time.perf_counter()
    while shared.counter < 10:
        print(f'id: {tid}, ctr: {shared.counter}')
        tmp = shared.list.pop(0)
        await asyncio.sleep(1)
        shared.counter += 1
        await afp.write(f"id: {tid}: ctr: {shared.counter} time: {time.perf_counter() - time_start :.1f}, val:{tmp}\n")
    print(f'ctr: {shared.counter} time {time.perf_counter() - time_start :.1f}')


async def main():
    async with async_open("text_sync.txt", 'w+') as afp:
        shared = Shared()
        a = write(0, shared, afp)
        b = write(1, shared, afp)
        start_time = time.perf_counter()
        await asyncio.gather(a, b)
        elapsed = time.perf_counter() - start_time
        print(f"\nTotal elapsed time: {elapsed:.1f}")


if __name__ == '__main__':
    asyncio.run(main())
