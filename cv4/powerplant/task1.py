from random import randint
from time import sleep
from fei.ppds import Event, Semaphore, Thread
from cv4.powerplant.lightswitch import LightSwitch


def monitor(monitor_id, valid_data, turnstile, memory_lock, lightswitch_monitor):
    # monitor waiting for at least one sensor access
    valid_data.wait()

    while True:
        # wait 0.5s for actualization
        sleep(0.5)
        # wait until all sensors leave critical area
        turnstile.wait()
        # lock memory with ADT Lightswitch - multiple monitors can read simultaneously
        monitor_count = lightswitch_monitor.lock(memory_lock)
        # leave turnstile
        turnstile.signal()

        # ... MONITOR CODE ... #
        print(f'MONITOR {monitor_id}: monitor count={monitor_count}')

        # unlock memory lock if monitor is the last one
        lightswitch_monitor.unlock(memory_lock)


def sensor(sensor_id, valid_data, turnstile, memory_lock, lightswitch_sensor):
    while True:
        # pass through the turnstile
        turnstile.wait()
        turnstile.signal()

        # lock memory with ADT Lightswitch - multiple sensors can write simultaneously
        sensors_count = lightswitch_sensor.lock(memory_lock)

        # ... SENSOR CODE ... #
        write_time = randint(10, 15)
        print(f'SENSOR {sensor_id}: writing for {write_time} seconds. Sensors count={sensors_count}')
        sleep(write_time)

        # signalization - at least one sensor updated data
        valid_data.signal()
        # unlock memory
        lightswitch_sensor.unlock(memory_lock)


if __name__ == '__main__':
    vd = Event()
    turn = Semaphore(1)
    mem_lock = Semaphore(1)
    switch_monitor = LightSwitch()
    switch_sensor = LightSwitch()

    sensor_cnt = 11
    monitor_cnt = 2

    sensors = [Thread(sensor, i, vd, turn, mem_lock, switch_sensor) for i in range(sensor_cnt)]
    monitors = [Thread(monitor, i, vd, turn, mem_lock, switch_monitor) for i in range(monitor_cnt)]

    for s in sensors:
        s.join()

    for m in monitors:
        m.join()

