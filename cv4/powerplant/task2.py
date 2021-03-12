from random import randint
from time import sleep
from fei.ppds import Semaphore, Thread
from cv4.powerplant.barrier import BarrierUsingEvent
from cv4.powerplant.lightswitch import LightSwitch


def sensor_h(sensor_id, valid_data_barrier, no_operator, no_sensor,
             lightswitch, interval_start, interval_stop):
    while True:
        # sleep
        sleep(randint(50, 60) / 1000)
        # lock turnstile
        sensor_counter = lightswitch.lock(no_operator)
        # memory lock - operators can not read
        no_sensor.wait()
        # update
        sleep_time = randint(interval_start, interval_stop) / 1000
        print(f"cidlo {sensor_id}: pocet_zapisujucich_cidiel={sensor_counter}"
              f", trvanie_zapisu={sleep_time}")
        sleep(sleep_time)
        # memory unlock - operators can read
        no_sensor.signal()

        # unlock turnstile
        lightswitch.unlock(no_operator)
        # signalization - write done
        valid_data_barrier.increment_and_wait()


def operator(operator_id, valid_data_barrier, no_operator, no_sensor,
             lightswitch):
    # wait until all sensors write data at least once
    valid_data_barrier.wait()
    while True:
        # turnstile
        no_operator.wait()
        # lock memory - sensors can not write
        monitor_cnt = lightswitch.lock(no_sensor)
        # free turnstile
        no_operator.signal()
        # wait for update
        sleep_time = randint(40, 50) / 1000
        print(f"monit:{operator_id} pocet_citajucich_monitorov={monitor_cnt}, "
              f"trvanie_citania={sleep_time}")
        sleep(sleep_time)

        # unlock memory - sensors can write
        lightswitch.unlock(no_sensor)


if __name__ == '__main__':
    sensor_cnt = 3
    operator_cnt = 8
    turn = Semaphore(1)
    mem_lock = Semaphore(1)
    lightswitch_operator = LightSwitch()
    lightswitch_sensor = LightSwitch()
    valid_data = BarrierUsingEvent(sensor_cnt)

    monitors = [Thread(operator, i, valid_data, turn, mem_lock,
                       lightswitch_operator)
                for i in range(operator_cnt)]
    # p, t sensors
    sensors = [Thread(sensor_h, i, valid_data, turn, mem_lock,
                      lightswitch_sensor, 10, 20)
               for i in range(sensor_cnt - 1)]
    # h sensor
    sensors.append(Thread(sensor_h, sensor_cnt - 1, valid_data, turn, mem_lock,
                          lightswitch_sensor, 20, 25))

    for s in sensors:
        s.join()

    for m in monitors:
        m.join()
