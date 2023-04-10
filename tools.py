import network, rp2, time
from utime import sleep
from machine import Pin, time_pulse_us
from lib import hcsr04

class Tools:

    def __init__(self):
        self.settings = self.get_settings()
        self.led = Pin("LED", Pin.OUT)
        self.sensor = hcsr04.HCSR04(int(self.settings['SENSOR_TRIG']), int(self.settings['SENSOR_ECHO']))


    def get_settings(self):
        settings = {}
        with open('.env') as f:
            for line in f:
                key, value = line.strip().split('=', 1)
                settings[key] = value

        return settings


    def wifi_connect(self):
        self.led.on()
        rp2.country('DE')
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        sleep(3)
        # set power mode to get WiFi power-saving off (if needed)
        wlan.config(pm = 0xa11140)
        wlan.connect(self.settings['WIFI_NAME'], self.settings['WIFI_PASSWORD'])

        while not wlan.isconnected() and wlan.status() >= 3:
            print("Waiting to connect ...")
            time.sleep(1)

        self.led.off()
        return wlan

    def get_distance(self):
        return self.sensor.distance_cm()
