from machine import Pin
from dht import DHT11
import network
import socket
import time

# Create DHT object
pin = Pin(17, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)

def connect():
    good_connection= False
    while good_connection == False:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect('gh', 'Jean&Keith')
        for ct in range(5):
            if wlan.isconnected() == True:
                good_connection= True
            else:
                print('Waiting for connection...', ct, end='\r')
                time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'WiFi Connected on {ip}')
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

# Start program
ip = connect()
connection = open_socket(ip)
while True:
    try:
        cl, addr = connection.accept()
        request = cl.recv(1024)
        print(request)
        # No need to unpack request in this example
        sensor.measure()
        sensor_data = f'{sensor.temperature()}:{sensor.humidity()}'
        cl.send(sensor_data)
        print("Sent: " + sensor_data)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')