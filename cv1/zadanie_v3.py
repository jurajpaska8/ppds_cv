from fei.ppds import Thread
from ulohy_z_cvicenia import Shared, Histogram


# Verzia 3
# obsahuje uzamknutie zamku na zaciatku while cyklu. Bolo potrebne funkciu doladit a pridat odomknutie aj do if
# casti algoritmu, inak nastavalo uviaznutie jedneho z vlakien
# takyto pristup povazujem zo vsetkych troch ako najlepsi z hladiska paralelizmu
def counter(sh):
    while True:
        sh.mutex.lock()
        if sh.counter >= sh.end:
            sh.mutex.unlock()
            break
        sh.array[sh.counter] += 1
        sh.counter += 1
        sh.mutex.unlock()


for i in range(10):
    shared = Shared(1_000_000)
    t1 = Thread(counter, shared)
    t2 = Thread(counter, shared)

    t1.join()
    t2.join()

    print(Histogram(shared.array))
