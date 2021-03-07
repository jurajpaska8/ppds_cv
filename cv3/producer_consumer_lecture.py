from time import sleep

from fei.ppds import randint
from light_switch import LightSwitch


class Warehouse(object):
    def __init__(self):
        self.lightSwitch = LightSwitch()


def producent(shared):
    # produkcia
    sleep(randint(0, 10) / 10)
    # kontrola volneho miesta v sklade
    shared.free.wait()
    # pristup do skladu
    shared.mutex.lock()
    # ulozenie vyrobku do skladu
    sleep(randint(0, 1) / 10)
    # odidenie zo skladu
    shared.mutex.unlock()
    # zvysenie poctu vyrobkov v sklade
    shared.items.signal()


def consumer(shared):
    # kontrola existencie vyrobku v sklade
    shared.items.wait()
    # ziskanie pristupu v sklade
    shared.mutex.lock()
    # ziskanie vyrobku
    sleep(randint(0, 1) / 10)
    # odidenie zo skladu
    shared.mutex.unlock()
    # spracovanie vyrobku
    sleep(randint(0, 10) / 10)
