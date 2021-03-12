from random import randint
from time import sleep
from fei.ppds import Semaphore, Thread
from cv4.powerplant.barrier import BarrierUsingEvent
from cv4.powerplant.lightswitch import LightSwitch


def sensor_p_t(sensor_id, valid_data_barrier, turnstile, memory_lock):  # TODO
    while True:
        # every time pass turnstile
        turnstile.wait()
        turnstile.signal()

        # sleep
        sleep(randint(50, 60) / 1000)
        # update
        sleep(randint(10, 20) / 1000)

        valid_data_barrier.increment_and_wait()


def sensor_h(sensor_id, valid_data_barrier, no_operator, no_sensor):
    while True:
        # sleep
        sleep(randint(50, 60) / 1000)
        # lock turnstile
        no_operator.wait()
        # memory lock - operators can not read
        no_sensor.wait()
        # update
        sleep_time = randint(20, 25) / 1000
        print(f"cidlo {sensor_id}: pocet_zapisujucich_cidiel=TODO, trvanie_zapisu={sleep_time}") # TODO
        sleep(sleep_time)
        # memory unlock - operators can read
        no_sensor.signal()

        # unlock turnstile
        no_operator.signal()
        # signalization - write done
        valid_data_barrier.increment_and_wait()


def operator(operator_id, valid_data_barrier, no_operator, no_sensor, lightswitch):
    # wait until all sensors write data at least once
    valid_data_barrier.wait()
    while True:
        # turnstile
        no_operator.wait()
        no_operator.signal()
        # lock memory - sensors can not write
        monitor_cnt = lightswitch.lock(no_sensor)
        # wait for update
        sleep_time = randint(40, 50) / 1000
        print(f"monit:{operator_id} pocet_citajucich_monitorov={monitor_cnt}, trvanie_citania={sleep_time}")
        sleep(sleep_time)

        # unlock memory - sensors can write
        lightswitch.unlock(no_sensor)


if __name__ == '__main__':
    sensor_cnt = 3
    operator_cnt = 8
    turn = Semaphore(1)
    mem_lock = Semaphore(1)
    lightswitch_operator = LightSwitch()
    valid_data = BarrierUsingEvent(sensor_cnt)

    monitors = [Thread(operator, i, valid_data, turn, mem_lock, lightswitch_operator) for i in range(operator_cnt)]
    sensors = [Thread(sensor_h, i, valid_data, turn, mem_lock) for i in range(sensor_cnt)]

    for s in sensors:
        s.join()

    for m in monitors:
        m.join()
