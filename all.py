import time
import socket
import json
import ntptime
from lib import hcsr04
import tools

setting = tools.get_settings()

# @todo: remove.........
print(setting['WIFI_NAME'])

led = tools.get_led()

led.on()
time.sleep(2)
led.off()

wlan = tools.wifi_connect()

status = wlan.ifconfig()
print( 'Current IP Address: ' + status[0] )


# The Webserver ....
addr = socket.getaddrinfo(status[0], 80)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)
print('Server is listening on', addr)

def close(connection = None):
    if connection:
        connection.close()
    server.close()
    print('Server stopped')

connection = None

# Listening to connection
while True:
    try:
        connection, addr = server.accept()
        print('HTTP-Request von Client', addr)
        request = connection.recv(1024)
        print('Request:', request)
        json_response = {
            'time': ntptime.time(),
            'distance': 'kljkjlk',
        }

        response = json.dumps(json_response)
        connection.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
        connection.send(response)
        connection.close()
        print('HTTP-Response gesendet')
        print()
    except OSError as e:
        close()
        break
    except (KeyboardInterrupt):
        close(connection)
        break
