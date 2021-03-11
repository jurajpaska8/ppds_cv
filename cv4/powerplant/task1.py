from random import randint
from time import sleep
from fei.ppds import Event, Semaphore, Thread
from cv4.powerplant.lightswitch import LightSwitch


def monitor(monitor_id, valid_data, turnstile, memory_lock, lightswitch_monitor):
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
        print('monitor "%02d": monitor count=%02d\n' % monitor_id, monitor_count)
        # unlock memory lock if monitor is the last one
        lightswitch_monitor.lock(memory_lock)


def sensor(sensor_id, valid_data, turnstile, memory_lock, lightswitch_sensor):
    while True:
        # pass through the turnstile
        turnstile.wait()
        turnstile.signal()

        # lock memory with ADT Lightswitch - multiple sensors can write simultaneously
        sensors_count = lightswitch_sensor.lock(memory_lock)
        #
        write_time = randint(10, 15)
        print('sensor "%02d": writing for =%02d seconds. Sensors count=%02d\n' % sensor_id, write_time, sensors_count)
        sleep(write_time)

        # signalization - at least one sensor updated data
        valid_data.signal()


if __name__ == '__main__':
    vd = Event()
    turn = Semaphore(1)
    mem_lock = Semaphore(1)
    switch_monitor = LightSwitch()
    switch_sensor = LightSwitch()

    sensor_count = 11
    monitor_count = 2

    sensors = [Thread(sensor, i, vd, turn, mem_lock, switch_sensor) for i in range(sensor_count)]
    monitors = [Thread(monitor, i, vd, turn, mem_lock, switch_monitor) for i in range(monitor_count)]

    for s in sensors:
        s.join()

    for m in monitors:
        m.join()

