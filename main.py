import time
import socket
import json
import tools
import _thread

toolbox = tools.Tools()
distance = 0
temperature = 0

def close(connection = None):
    if connection:
        connection.close()
    if server:
        server.close()
    print('Server stopped')

connection = None
server = None

def core0_network():
    global server
    wlan = toolbox.wifi_connect()
    status = wlan.ifconfig()

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
            request = connection.recv(1024)
            json_response = {
                'distance': distance,
                'temperature': temperature,
            }

            response = json.dumps(json_response)
            connection.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
            connection.send(response)
            connection.close()
        except OSError as e:
            print(e)
            close()
            wlan.disconnect()
            wlan = toolbox.wifi_connect()
            if wlan.isconnected():
               core0_network() 
            break
        except (KeyboardInterrupt):
            close(connection)
            wlan.disconnect()
            break


def core1_sensor():
    global temperature
    global distance
    while True:
        temperature = toolbox.get_temp()
        distance = toolbox.get_distance()
        print(distance)
        time.sleep_ms(1000)

second_thread = _thread.start_new_thread(core1_sensor, ())

core0_network()
