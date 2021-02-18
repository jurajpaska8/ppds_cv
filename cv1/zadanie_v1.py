from fei.ppds import Thread
from ulohy_z_cvicenia import Shared, Histogram


# Verzia 1 funkcie counter obsahuje zamok na zaciatku a na konci funkcie.
# Dosiahneme tym take spravanie, ze tuto funkciu moze naraz vykonavat len jedno vlakno.
# Pri velkosti pola 1 000 000 sme je dosiahnutelne, ze na kazdej pozicii bude hodnota 1,
# pretoze druhe vlakno pristupi k polu az ked bude na kazdej pozicii hodnota 1 a counter bude na konci pola.
# Takyto pristup je pre paralelizaciu nevhodny. Ide o seriove vykonanie jednym vlaknom.
def counter(sh):
    sh.mutex.lock()
    while True:
        if sh.counter >= sh.end:
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
