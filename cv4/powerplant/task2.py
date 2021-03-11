from random import randint
from time import sleep
from fei.ppds import Semaphore


def sensor_p_t(sensor_id):
    while True:
        # sleep
        sleep(randint(50, 60) / 1000)
        # update
        sleep(randint(10, 20) / 1000)


def sensor_h(sensor_id):
    while True:
        # sleep
        sleep(randint(50, 60) / 1000)
        # update
        sleep(randint(20, 25) / 1000)


def operator(operator_id):
    while True:
        sleep(randint(40, 50) / 1000)


def monitor(monitor_id):
    # wait for all sensors send data at least one time
    all_sensors_send_data.wait()

    # infinit loop
    while True:
        sleep(randint(40, 50) / 1000)


if __name__ == '__main__':
    turnstile = Semaphore(1)
    all_sensors_send_data = Semaphore(1)
    print("HIO")
