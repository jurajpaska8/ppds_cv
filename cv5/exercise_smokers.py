from time import sleep
from random import randint

from fei.ppds import Semaphore, Thread


class Shared:
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)

        self.agentSem = Semaphore(1)


def make_cigarette():
    sleep(randint(0, 10) / 100)


def smoke():
    sleep(randint(0, 10) / 100)


def agent_1(shared):
    while True:
        # poprehadzuj - aby nebolo rovnake poradie
        sleep(randint(0, 10) / 100)
        shared.agentSem.wait()
        print("agent: tobacco, paper")
        shared.tobacco.signal()
        shared.paper.signal()


# kody sa opakuju - uvazujme znovupouzitelnost
def agent_2(shared):
    while True:
        # poprehadzuj - aby nebolo rovnake poradie
        sleep(randint(0, 10) / 100)
        shared.agentSem.wait()
        print("agent: paper, match")
        shared.paper.signal()
        shared.match.signal()


def agent_3(shared):
    while True:
        # poprehadzuj - aby nebolo rovnake poradie
        sleep(randint(0, 10) / 100)
        shared.agentSem.wait()
        print("agent: tobacco, match")
        shared.tobacco.signal()
        shared.match.signal()


def smoker_match(shared):
    while True:
        sleep(randint(0, 10) / 100)

        shared.paper.wait()
        print("smoker M : paper taken")
        shared.tobacco.wait()
        print("smoker M : tobacco taken")

        make_cigarette()
        shared.agentSem.signal()
        smoke()


def smoker_tobacco(shared):
    while True:
        sleep(randint(0, 10) / 100)

        shared.match.wait()
        print("smoker T : match taken")
        shared.paper.wait()
        print("smoker T : paper taken")

        make_cigarette()
        shared.agentSem.signal()
        smoke()


def smoker_paper(shared):
    while True:
        sleep(randint(0, 10) / 100)

        shared.tobacco.wait()
        print("smoker P : tobacco taken")
        shared.match.wait()
        print("smoker P : match taken")

        make_cigarette()
        shared.agentSem.signal()
        smoke()


def run_model():
    shared = Shared()

    smokers = [Thread(smoker_match, shared), Thread(smoker_tobacco, shared), Thread(smoker_paper, shared)]
    agents = [Thread(agent_1, shared), Thread(agent_2, shared), Thread(agent_3, shared)]

    for s in smokers:
        s.join()

    for a in agents:
        a.join()


if __name__ == '__main__':
    run_model()
