import time
import socket
import json
from sensor import Distance
import _thread
import gc
import wificonfig

distance = 0
temperature = 0
connection = None
server = None

def close():
    if connection:
        connection.close()
    if server:
        server.close()
    print('Server stopped ...')

def core0_network():
    global server
    global connection
    
    wlan = wificonfig.get_connection()
    status = wlan.ifconfig()
    print(status)

    # The Webserver
    addr = socket.getaddrinfo(status[0], 80)[0][-1]
    server = socket.socket()
    # Avoid EADDRINUSE error (before bind()!!)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)
    server.listen(1)
    print('Server is listening on', addr)

    # Listening to connection
    while True:
        try:
            connection, addr = server.accept()
            json_response = {
                'distance': distance,
                'temperature': temperature,
            }

            connection.recv(1024)
            response = json.dumps(json_response)
            connection.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
            connection.send(response)
            connection.close()

            # Trigger garbage collection to avoid crashes
            gc.collect()
        except OSError as e:
            print(e)
            # In case of an error due to missing wificonnection or such,
            # close the connection/server and trigger the method again.
            close()
            core0_network() 
            break
        except (KeyboardInterrupt):
            close()
            wlan.disconnect()
            break


def core1_sensor():
    global temperature
    global distance
    global distance

    while not wificonfig.read_config().get("trig_pin") and not wificonfig.read_config().get("echo_pin"):
        time.sleep_ms(1000)

    interval = int(wificonfig.read_config().get("interval"))
    tools = Distance()

    while True:
        temperature = tools.get_temp()
        distance = tools.get_distance()
        print('Distance ' + str(distance) + ' Temp:' + str(temperature))
        time.sleep(interval)


second_thread = _thread.start_new_thread(core1_sensor, ())

core0_network()