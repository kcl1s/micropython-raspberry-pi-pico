from machine import Pin
from time import sleep

pix_pin = Pin(12, Pin.OUT)
num_pix = 12
pixels = [[0,0,0]] * num_pix
brightness = .1

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_init=rp2.PIO.OUT_LOW,
             out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    # 1 cycle = 0.2us (clock frequency must be set to 5MHz)    
    out(x, 1)           # 1 cycle at 0 (split low)   shifts one bit from osr to x
    set(pins, 1) [1]    # 2 cycles at 1
    mov(pins, x) [1]    # 2 cycles at x
    set(pins, 0)        # 1 cycle at 0
 
sm_neo = rp2.StateMachine(0, ws2812, freq=5000000, set_base=pix_pin, out_base=pix_pin)
sm_neo.active(1)

def show():
    for pixel in pixels:
        r = int(pixel[0]*brightness)
        g = int(pixel[1]*brightness)
        b = int(pixel[2]*brightness)
        grb = (g<<16) + (r<<8) + b  # or (g<<16) | (r<<8) | b
        sm_neo.put(grb, 8)

def fill_color(color, update = False):
    for x in range(num_pix):
        pixels[x] = color
    if update:
        show()

def wipe(color, dwell = .1, ccw = False):
    for i in range(num_pix):
        if ccw:
            pixels[num_pix-1-i] = color
        else:
            pixels[i] = color
        show()
        sleep(dwell)
        
def follow(color, loops = 3):
    fill_color([0,0,0])
    for i in range(num_pix*loops):
        pixels[i % num_pix] = color
        pixels[(i-3) % num_pix] = [0,0,0]
        show()
        sleep(.1)
    fill_color([0,0,0], True)

    
def follow_rwb(loops = 3):
    fill_color([0,0,0])
    for i in range(num_pix*loops):
        pixels[i % num_pix] = [255,0,0]
        pixels[(i-1) % num_pix] = [255,255,255]
        pixels[(i-2) % num_pix] = [0,0,255]
        pixels[(i-3) % num_pix] = [0,0,0]
        show()
        sleep(.2)
    fill_color([0,0,0], True)
    
def wheel(pos):
    if pos <= 85:
        return (255 - pos * 3, 0, pos * 3)  # Generate a red - blue color
    elif pos <= 170:
        pos -= 85
        return (0, pos * 3, 255 - pos * 3)  # Generate a blue - green color
    else:
        pos -= 170
        return (pos * 3, 255 - pos * 3, 0)  # Generate a green - red color
    
def rbc():
    fill_color([0,0,0])
    for j in range(256*5):
        for i in range(num_pix):
            pixels[i] = (wheel((int(i* 256 / num_pix) + j) % 255))
        show()
        sleep(.01)
    fill_color([0,0,0], True)

fill_color([0,0,255], True)
wipe([255,0,0])
sleep(1)
wipe([255,255,255], .05, ccw=True)
sleep(1)
wipe([0,0,255], ccw=True)
sleep(2)
follow([0,255,0], 5)
follow_rwb()
rbc()