# Bibliotheken laden
from machine import Pin
from utime import sleep


import machine
led = machine.Pin("LED", machine.Pin.OUT)
led.off()
led.on()

# 5 Sekunden warten
sleep(5)

# LED ausschalten
led.off()