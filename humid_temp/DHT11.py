import dht
import machine
import time


def measure_humid_temp(pin):
    humitemp = dht.DHT11(machine.Pin(pin))
    humitemp.measure()

    # Give enough time for reading from sensor
    time.sleep(1)

    humidity = humitemp.humidity()
    temperature = humitemp.temperature()

    result_dict = {
        "humidity": humidity,
        "temperature": temperature
    }

    return result_dict
