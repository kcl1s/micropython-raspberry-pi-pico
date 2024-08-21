from machine import Pin
from db_irq import DB_irq

ct = 0
ct2 = 0

led = Pin('LED', Pin.OUT)

def cb_gb(pin):
    global ct
    ct += 1
    print('Toggle', ct)
    led.toggle()

def cb_rb(pin):
    global ct2
    ct2 += 1
    print('Toggle Red', ct2)
    
red_but = DB_irq(pin = 15, trigger = Pin.IRQ_RISING, handler = cb_rb, debounce_ms = 50)
green_but = DB_irq(pin = 16, trigger = Pin.IRQ_FALLING, handler = cb_gb)

while True:
    pass
