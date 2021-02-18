from fei.ppds import Thread
from ulohy_z_cvicenia import Shared, Histogram


# Verzia 2 funkcie counter obsahuje zamok pred inkrementaciou countera a pred inkrementaciou pola
# Pri velkosti pola 1 000 000 je dosiahnutelne, ze na kazdej pozicii bude hodnota 1, ak program nepadne
# Tym ze sa inkrementuju obe premenne naraz(atomarne) sme dosiahli, ze v ziadnom policku nebude hodnota vacsia ako 1
# Tym ze porovnanie countra s velkostou pola je vykonane bez uzamknutia vsak moze dojst k tomu,
# ze zatial co jedno vlakno vykonava poslednu iteraciu, druhe vlakno caka na uvolnenie zamku uz za if podmienkou
# To sposobi ze navysenie hodnoty countra o 1 jednym vlaknom, bude mat po uvolneni zamku za nasledok dereferencovanie
# adresy za rozsahom pola vlaknom dva
def counter(sh):
    while True:
        if sh.counter >= sh.end:
            break
        sh.mutex.lock()
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
