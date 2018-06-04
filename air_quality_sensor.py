from umqtt.simple import MQTTClient
from machine import SPI
from carbon_monoxoide.CO import get_co_percentage
from humid_temp.DHT11 import measure_humid_temp
import network
import json
import dht
import machine
import time
import utime


def wifi_connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Connected!')


def enter_deep_sleep():
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # Wake up device after 30 minutes
    rtc.alarm(rtc.ALARM0, 1000 * 60 * 30)

    # Wait 20 seconds before sleeping to avoid difficult to program boot loop
    time.sleep(20)

    # put the device to sleep
    print("Going to deep sleep")
    machine.deepsleep()


def main():
    config = json.load(open("config.json"))

    wifi_connect(config["wifi"]["ssid"], config["wifi"]["password"])

    mqtt_conn = MQTTClient(config["device_name"], config["mqtt_host_name"])
    mqtt_conn.connect()

    co_percentage = get_co_percentage(0)

    res_dict = measure_humid_temp(config["humitemp_pin"])

    print("humidity: " + str(res_dict["humidity"]))
    print("temperature: " + str(res_dict["temperature"]))

    sensor_payload = {
        "humidity": res_dict["humidity"],
        "temperature": res_dict["temperature"],
        "carbon monoxide": co_percentage
    }

    mqtt_conn.publish(config["device_name"], str(sensor_payload))

    mqtt_conn.disconnect()

    # Disable for now during development
    # enter_deep_sleep()


if __name__ == "__main__":
    print("board started")
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print('woke from a deep sleep')
    else:
        print('power on or hard reset')

    main()
