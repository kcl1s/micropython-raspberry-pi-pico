import time
from machine import Pin
import rp2

dist = 0
echo = Pin(21,Pin.IN)
trig = Pin(20,Pin.OUT)
pwr = Pin(19, Pin.OUT)
pwr.on()

def get_cm(x):
    global dist
    dist = 300 - sm.get()
    #print(dist,time.ticks_ms())

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def ping():
    mov(x,osr)       # mov isr back to x
    set(pins,0) [9]  # set trig to low 10 uSec
    set(pins,1) [9]  # set trig to high 10 uSec
    set(pins,0)      # set trig to low
    wait(1,pin,0)    # wait for echo input to go high    
    label('cm')
    jmp(x_dec,'ck_echo')    [28]   # ck for timeout < 300
    jmp('do_delay')        # if so jmp to 80 ms delay
    label('ck_echo')
    jmp(pin,'cm')   [28]   # while echo high jmp to cm
    mov(isr,x)             # when echo goes low send x to isr
    push()                 # then push to fifo
    irq(rel(0))            # trigger irq to "get" value
    label('do_delay')
    mov(isr,invert(null))    # start timing loop
    in_(null,12) # 12 bits = 4096 x 20 = 81920 cycles or ~80 ms
    mov(y,invert(isr))
    label("delay")
    jmp(y_dec, "delay")   [19]   # end timing loop

       
sm = rp2.StateMachine(0, ping, freq=1000000, set_base=trig, jmp_pin=echo, in_base=echo)
sm.irq(get_cm)
sm.put(300)        # new
sm.exec("pull()")  # lines
sm.active(1)

while True:
    time.sleep(.5)
    print(dist)
    
    