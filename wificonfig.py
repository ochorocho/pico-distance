"""Heavily inspired by """
import network
import socket
import ure
import time
import json
import rp2, time
from utime import sleep
from component import page, form


ap_ssid = "Pico distance sensor"
ap_password = "password"
ap_authmode = 3

CONFIG_FILE = 'config.json'

# wlan_ap = network.WLAN(network.AP_IF)
# wlan_sta = network.WLAN(network.STA_IF)

server_socket = None
client = None
rp2.country('DE')


def get_connection() -> network.WLAN:
    wlan_sta = network.WLAN(network.STA_IF)

    try :
        wlan_sta = do_connect(wlan_sta)
    except:
        wlan_sta = start(wlan_sta, 80)

    while not wlan_sta.isconnected():
        break

    return wlan_sta
    

def read_config():
    try:
        with open(CONFIG_FILE) as file:
            json_content = file.read()
            time.sleep(1)
            config = json.loads(json_content)
    except OSError as e:
        config = {}

    return config


def write_config(config):

    print('WRITE CONFIG', config)

    config = json.dumps(config)

    with open(CONFIG_FILE, "w") as f:
        f.write(config)


def do_connect(wlan_sta) -> network.WLAN:
    global server_socket

    ssid = read_config().get("ssid")
    password = read_config().get("password")

    print('Trying to connect to %s...' % ssid)

    wlan_sta.active(True)
    sleep(3)

    wlan_sta.connect(ssid, password)
    # and (wificlient_if.ifconfig()[0] == '0.0.0.0')
    while not wlan_sta.isconnected() and wlan_sta.status() >= 3:
        print('.', end='')
        time.sleep(0.1)

    return wlan_sta


def send_header(client, status_code=200, content_length=None ):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    if content_length is not None:
      client.sendall("Content-Length: {}\r\n".format(content_length))
    client.sendall("\r\n")


def send_response(client, payload, status_code=200):
    content_length = len(payload)
    send_header(client, status_code, content_length)
    if content_length > 0:
        client.sendall(payload)
    client.close()


def handle_root(client, wlan_sta):
    wlan_sta.active(True)
    ssids = sorted(ssid.decode('utf-8') for ssid, *_ in wlan_sta.scan())
    send_header(client)

    html = page()
    
    client.sendall(html.replace("#content#", form(ssids)))
    client.close()


def handle_configure(client, request, wlan_sta):
    print(request)
    match = ure.search("ssid=([^&]*)&password=([^&]*)&echo_pin=([1-9]*)&trig_pin=([1-9]*)&interval=([1-9]*)", request)

    if match is None:
        html = page()
        send_response(client, html.replace("#content#", "⚠️ Parameters not found"), status_code=400)
        return False

    config_incoming = {
        "ssid": match.group(1).decode("utf-8"),
        "password": match.group(2).decode("utf-8"),
        "echo_pin": match.group(3).decode("utf-8"),
        "trig_pin": match.group(4).decode("utf-8"),
        "interval": match.group(5).decode("utf-8"),
        "mqtt_topic": "ochorocho/sensor",
        "mqtt_target": "192.168.178.1",
    }

    if len(str(config_incoming.get("ssid"))) == 0:
        send_response(client, "SSID must be provided", status_code=400)
        return False

    write_config(config_incoming)

    if do_connect(wlan_sta):
        time.sleep(5)
        config = read_config()

        # @todo: recreate AP and send IP!
        html = page()
        content = """
            SAFE DONE JIIIIHA!.... {}. 
            <form>
                <input type="button" class="button" value="Go back!" onclick="history.back()"></input>
            </form>
        """.format(config_incoming.get("ssid"))

        send_response(client, html.replace("#content#", content))
        time.sleep(5)

        return True
    else:
        html = page()
        content = """
            ❌ Could not connect to WiFi network {}. 
            <form>
                <input type="button" class="button" value="Go back!" onclick="history.back()"></input>
            </form>
        """.format(config_incoming.get("ssid"))

        send_response(client, html.replace("#content#", content))
        return False


def handle_not_found(client, url):
    html = page()    
    send_response(client, html.replace("#content#", "⚠️ Path not found: {}".format(url)), status_code=404)


def stop():
    global server_socket

    if server_socket:
        server_socket.close()
        server_socket = None


def start(wlan_sta, port=80):
    global server_socket
    global client
    addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]

    stop()
    wlan_sta.active(True)

    wlan_ap = network.WLAN(network.AP_IF)
    wlan_ap.config(essid=ap_ssid, password=ap_password)
    wlan_ap.active(True)

    server_socket = socket.socket()
    # Avoid EADDRINUSE error (before bind()!!)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(addr)
    server_socket.listen(1)

    print('Connect to WiFi ssid ' + ap_ssid + ', default password: ' + ap_password)
    print('and access the Pic W via your favorite web browser at 192.168.4.1.')
    print('Listening on:', addr)

    while not wlan_sta.isconnected():
        client, addr = server_socket.accept()
        print('Client connected from', addr)
        try:
            client.settimeout(5.0)

            request = b""
            try:
                while "\r\n\r\n" not in str(request):
                    request += client.recv(1024)
            except OSError:
                pass

            if "HTTP" not in str(request):
                continue

            # version 1.9 compatibility
            try:
                url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", str(request)).group(1).decode("utf-8").rstrip("/")
            except Exception:
                url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", str(request)).group(1).rstrip("/")

            if url == "":
                handle_root(client, wlan_sta)
            elif url == "configure":
                handle_configure(client, request, wlan_sta)
            else:
                handle_not_found(client, url)

        finally:
            client.close()
            # @todo: does this make sense at all?!
            wlan_ap.disconnect()

    return wlan_sta