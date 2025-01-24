from machine import Pin
import array
from time import sleep
import random

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_init=rp2.PIO.OUT_LOW,
             out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    # 1 cycle = 0.2us (clock frequency must be set to 5MHz)    
    out(x, 1)           # 1 cycle at 0 (split low)
    set(pins, 1) [1]    # 2 cycles at 1
    mov(pins, x) [1]    # 2 cycles at x
    set(pins, 0)        # 1 cycle at 0
    
    
class pio_neo:
    sm = 0
    
    def __init__(self, pin, num_pix):
        self.pix_pin = Pin(pin, Pin.OUT)
        self.num_pix = num_pix
        self.color = [[0,0,0]] * self.num_pix
        self.brightness = 1
        self.sm_neo = rp2.StateMachine(pio_neo.sm, ws2812, freq=5000000,
                                       set_base=self.pix_pin, out_base=self.pix_pin) 
        self.sm_neo.active(1)
        self.ar = array.array("I", [0 for _ in range(self.num_pix)])
        pio_neo.sm += 1

    def show(self):
        self.sm_neo.put(self.ar, 8)
        
    def sb(self, color):
        r, g, b = color
        r = int(r * self.brightness)
        g = int(g * self.brightness)
        b = int(b * self.brightness)
        return (g<<16) + (r<<8) + b

    def fill_color(self, c, update = False):
        ac = self.sb(c)
        for x in range(self.num_pix):
            self.ar[x] = ac
        if update:
            self.show()

    def wipe(self, c, dwell = .1, ccw = False):
        ac = self.sb(c)
        for i in range(self.num_pix):
            if ccw:
                self.ar[self.num_pix-1-i] = ac
            else:
                self.ar[i] = ac
            self.show()
            sleep(dwell)
            
    def follow(self, c, loops = 3):
        ac = self.sb(c)
        self.fill_color([0,0,0])
        for i in range(self.num_pix*loops):
            self.ar[i % self.num_pix] = ac
            self.ar[(i-3) % self.num_pix] = self.sb([0,0,0])
            self.show()
            sleep(.1)
        self.fill_color([0,0,0], True)
        
    def follow_rwb(self, loops = 3):
        self.fill_color([0,0,0])
        for i in range(self.num_pix*loops):
            self.ar[i % self.num_pix] = self.sb([255,0,0])
            self.ar[(i-1) % self.num_pix] = self.sb([255,255,255])
            self.ar[(i-2) % self.num_pix] = self.sb([0,0,255])
            self.ar[(i-3) % self.num_pix] = self.sb([0,0,0])
            self.show()
            sleep(.2)
        self.fill_color([0,0,0], True)
                   
    def rand_pix(self, ct= 100, dwell= .1, clr_pix= True):
        self.fill_color([0,0,0], True)    
        for x in range(ct):
            p_pos = random.randint(0, p.num_pix - 1)
            p_color = random.randint(0, 255)
            self.ar[p_pos] = self.sb(self.wheel(p_color))
            self.show()
            sleep(dwell)
            if clr_pix:
                self.ar[p_pos] = self.sb([0,0,0])
        self.fill_color([0,0,0], True)

    def wheel(self, pos):
        if pos <= 85:
            return (255 - pos * 3, 0, pos * 3)  # Generate a red - blue color
        elif pos <= 170:
            pos -= 85
            return (0, pos * 3, 255 - pos * 3)  # Generate a blue - green color
        else:
            pos -= 170
            return (pos * 3, 255 - pos * 3, 0)  # Generate a green - red color

    def rainbow(self, dwell=.1, loops=3):
        for y in range(loops):
            for x in range(0,256,5):
                self.fill_color(self.wheel(x), True)
                sleep(dwell)
        self.fill_color([0,0,0], True)
    
    def rainbow_cycle(self):
        self.fill_color([0,0,0])
        for j in range(0,256*5,5):
            for i in range(self.num_pix):
                self.ar[i] = self.sb(self.wheel((int(i* 256 / self.num_pix) + j) % 255))
            self.show()
            sleep(.05)
        self.fill_color([0,0,0], True)
        
    def bounce(self, c, dwell=.2, loops=3):
        ac = self.sb(c)
        for x in range(self.num_pix * loops + 1):
            self.fill_color([0,0,0])
            self.ar[x % self.num_pix] = ac
            self.ar[(self.num_pix - x) % self.num_pix] = ac
            self.show()
            sleep(dwell)
        self.fill_color([0,0,0], True)

# end class--------------
if __name__ == '__main__':
    p = pio_neo(12,12)		# create a neopixel object
    p.brightness = .1		# set brightness
#    p2 = pio_neo(17,60)
#    p2.brightness = .2
    # demo of methods
#    p.fill_color([0,0,255], True)
#    sleep(1)
#    p.fill_color([255,0,0], True)
#    sleep(1)
#    p.fill_color([0,0,0], True)
#    sleep(1)
#    p.wipe([255,0,0])
#    p.wipe([0,0,0], ccw=True)
#    sleep(1)
#    p.wipe([255,255,255], .05, ccw=True)
#    sleep(1)
#    p.wipe([0,0,255], ccw=True)
#    sleep(2)
#    p.follow([0,255,0], 5)
#    p.follow_rwb()
#    p.rainbow()
#    p.rainbow_cycle()
    p.bounce([255,0,255],dwell=.05, loops=10)
#    p.rand_pix(clr_pix=False)
#    p2.rand_pix()