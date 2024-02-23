import network
import socket
from time import sleep

ssid='Y?OUR NETWORK'
password='YOUR PASSWORD'
        
def connect():
    good_connection= False
    while good_connection == False:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        for ct in range(5):
            if wlan.isconnected() == True:
                good_connection= True
            else:
                print('Waiting for connection...', ct, end='\r')
                sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'WiFi Connected on {ip}')
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

if __name__ == '__main__':
    connect()
