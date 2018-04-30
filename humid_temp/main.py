from umqtt.simple import MQTTClient
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

    humitemp = dht.DHT11(machine.Pin(config["humitemp_pin"]))
    humitemp.measure()

    # Give enough time for reading from sensor
    time.sleep(1)

    humidity = humitemp.humidity()
    temperature = humitemp.temperature()

    print("humidity: " + str(humidity))
    print("temperature: " + str(temperature))

    now = utime.localtime()
    sensor_payload = {
        "humidity": humidity,
        "temperature": temperature
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
