import network
import time
from machine import Pin


def get_led():
    return Pin("LED", Pin.OUT)


def get_settings():
    settings = {}
    with open('.env') as f:
        for line in f:
            key, value = line.strip().split('=', 1)
            settings[key] = value

    return settings


def wifi_connect():
    led = get_led()
    setting = get_settings()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(setting['WIFI_NAME'], setting['WIFI_PASSWORD'])

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

        if wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            led.off()
            print('connected')
            status = wlan.ifconfig()
            print( 'Current IP Address:' + status[0] )

    return wlan
