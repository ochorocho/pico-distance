import network, rp2, time
from utime import sleep
from machine import Pin, time_pulse_us, ADC
import wificonfig

SOUND_SPEED=340
TRIG_PULSE_DURATION_US=10

class Distance:

    def __init__(self):
        settings = wificonfig.read_config()
        self.trig_pin = Pin(int(settings.get("trig_pin")), Pin.OUT)
        self.echo_pin = Pin(int(settings.get("echo_pin")), Pin.IN)
        self.temp_sensor = ADC(4)

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

