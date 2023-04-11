import network, rp2, time
from utime import sleep
from machine import Pin, time_pulse_us, ADC

SOUND_SPEED=340
TRIG_PULSE_DURATION_US=10

class Tools:

    def __init__(self):
        self.settings = self.get_settings()
        self.led = Pin("LED", Pin.OUT)

        self.trig_pin = Pin(int(self.settings['SENSOR_TRIG']), Pin.OUT) # GP15
        self.echo_pin = Pin(int(self.settings['SENSOR_ECHO']), Pin.IN)  # GP14
        self.temp_sensor = ADC(4)

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
        self.trig_pin.value(0)
        time.sleep_us(5)
        self.trig_pin.value(1)
        time.sleep_us(TRIG_PULSE_DURATION_US)
        self.trig_pin.value(0)

        ultrason_duration = time_pulse_us(self.echo_pin, 1, 30000)
        distance_cm = SOUND_SPEED * ultrason_duration / 20000

        return distance_cm
    
    def get_temp(self):
        conversion_factor = 3.3 / (65535)
        reading = self.temp_sensor.read_u16() * conversion_factor 
        return 27 - (reading - 0.706)/0.001721

