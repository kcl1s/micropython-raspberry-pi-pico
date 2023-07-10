from machine import Pin
import network
import socket
import time
from lcd1602cc import LCD

# create LCD object
lcd= LCD()
lcd.clear()
# setup button pin
but = Pin(16, Pin.IN, Pin.PULL_UP)
# initalize variables
but_state = 1
old_state = 1
data_list = [0,0]
cf = True
# function to connect to wifi
def connect():
    good_connection= False
    while good_connection == False:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect('your network','your password')
        for ct in range(5):
            if wlan.isconnected() == True:
                good_connection= True
            else:
                print('Waiting for connection...', ct, end='\r')
                time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'WiFi Connected on {ip}')
    return ip
# function to open socket and request data from server
def get_reading():
    s = socket.socket() # Open socket
    s.connect(('server IP<change>',80))
    s.send("Get DHT Data") # Send request
    DHT_data = s.recv(512)
    data_string = DHT_data.decode("utf-8")
    data_list[0], data_list[1] = data_string.split(':')
    # Print what we received
    print(data_list, time.ticks_ms())
    s.close()
# function to update LCD
def print_to_LCD(cf):
    if cf:
        line_1 = f'Temp = {data_list[0]}{chr(223)}C  '
    else:
        tempF = round(int(data_list[0])*9/5+32)
        line_1 = f'Temp = {tempF}{chr(223)}F  '
        #line_1 = f'{line_1:<16}'
    line_2 = f'Humidity = {data_list[1]}%  '
    lcd.write(0,0,line_1)
    lcd.write(0,1,line_2)
    
# start program    
ip = connect()
prev_time = time.ticks_ms()
while True:
    # is it time to get a reading?
    if time.ticks_diff(time.ticks_ms(), prev_time) > 2000:
        get_reading()
        print_to_LCD(cf)
        prev_time = time.ticks_ms()
    # check button every loop
    but_state = but.value()
    time.sleep(.1)
    if but_state < old_state:
        cf = not cf
        print_to_LCD(cf)
    old_state = but_state
