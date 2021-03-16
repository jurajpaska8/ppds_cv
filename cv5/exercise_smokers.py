from time import sleep
from random import randint

from fei.ppds import Semaphore, Thread, Mutex, print


class Shared:
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)

        self.agentSem = Semaphore(1)

        self.isTobacco = 0
        self.isPaper = 0
        self.isMatch = 0
        self.mutex = Mutex()

        self.smokerMatch = Semaphore(0)
        self.smokerPaper = Semaphore(0)
        self.smokerTobacco = Semaphore(0)


def make_cigarette(who):
    print(f"    makes cig: {who}")
    sleep(randint(0, 10) / 100)


def smoke(who):
    print(f"    smokes cig: {who}")
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

        shared.smokerMatch.wait()

        make_cigarette("smoker match")
        shared.agentSem.signal()
        smoke("smoker match")


def smoker_tobacco(shared):
    while True:
        sleep(randint(0, 10) / 100)

        shared.smokerTobacco.wait()

        make_cigarette("smoker tobacco")
        shared.agentSem.signal()
        smoke("smoker tobacco")


def smoker_paper(shared):
    while True:
        sleep(randint(0, 10) / 100)

        shared.smokerPaper.wait()

        make_cigarette("smoker paper")
        shared.agentSem.signal()
        smoke("smoker paper")


def dealer_tobacco(shared):
    while True:
        shared.tobacco.wait()

        shared.mutex.lock()
        if shared.isPaper:
            shared.isPaper -= 1
            shared.smokerMatch.signal()
        elif shared.isMatch:
            shared.isMatch -= 1
            shared.smokerPaper.signal()
        else:
            shared.isTobacco += 1
        shared.mutex.unlock()


def dealer_match(shared):
    while True:
        shared.match.wait()

        shared.mutex.lock()
        if shared.isPaper:
            shared.isPaper -= 1
            shared.smokerTobacco.signal()
        elif shared.isTobacco:
            shared.isTobacco -= 1
            shared.smokerPaper.signal()
        else:
            shared.isMatch += 1
        shared.mutex.unlock()


def dealer_paper(shared):
    while True:
        shared.paper.wait()

        shared.mutex.lock()
        if shared.isMatch:
            shared.isMatch -= 1
            shared.smokerTobacco.signal()
        elif shared.isTobacco:
            shared.isTobacco -= 1
            shared.smokerMatch.signal()
        else:
            shared.isPaper += 1
        shared.mutex.unlock()


def run_model():
    shared = Shared()

    smokers = [Thread(smoker_match, shared), Thread(smoker_tobacco, shared), Thread(smoker_paper, shared)]
    agents = [Thread(agent_1, shared), Thread(agent_2, shared), Thread(agent_3, shared)]
    dealers = [Thread(dealer_paper, shared), Thread(dealer_match, shared), Thread(dealer_tobacco, shared)]

    for s in smokers:
        s.join()

    for a in agents:
        a.join()

    for d in dealers:
        d.join()


if __name__ == '__main__':
    run_model()
