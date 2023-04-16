# Raspberry Pi Pico W + HC-SR04

A custom distance sensor using a Pi Pico + HC-SR04 for HomeAssistant.

See https://github.com/ochorocho/pico_distance_component for the HomeAssistant custom component.

### Connect the sensor to your Pico W:

![Connect Pi Pico W to the HC-SR04](fritzing/pico-HC-SR04_connect.png)

### Configuration

* Power up the Pico
* Wait for the Wifi access point "Pi distance sensor" to show up and connect to it (Password: `password`, IP: `192.168.4.1`)
* Open http://192.168.4.1/ and select a ssid and enter the password
* Choose which pins to use for the sensor. Most likely 14 for `echo_pin` and 15 for the `trig_pin`
* Set a interval e.g. 1 to update the sensor value every second
* Click "submit"

Once the wifi is connected the Browser will timeout afterwards


### Upload the following files:
    
* `main.py` - the entrypoint, thread for webserver/network, thread to get the HC-SR04 sensor value in cm
* `sensor.py` - get sensor data
* `wificonfig.py` - GUI for wifi and GPIO configuration

# Credits

 * Wifi manager from https://github.com/tayfunulu/WiFiManager