from machine import Pin
import asyncio
import time
import aio_neo

btn = Pin(22, Pin.IN, Pin.PULL_UP)

async def blink(led, period_ms):
    for x in range(20):
        led.on()
        await asyncio.sleep_ms(period_ms)
        led.off()
        await asyncio.sleep_ms(period_ms)
        
async def button():
    btn_prev = btn.value()
    while (btn.value() == 1) or (btn.value() == btn_prev):
        btn_prev = btn.value()
        await asyncio.sleep(.04)

async def ring():
    print('ring')
    await p.follow([0,255,0], 5)
    await p.wipe([255,0,0])
    await p.rand_pix(clr_pix=False)
    
async def strip():
    print('strip')
    for x in range(10):
        await p2.fill([255,0,0], True)
        await button()
        await p2.fill([0,0,255], True)
        await button()
    await p2.fill([0,0,0], True)
        
async def main():
    tasks = (ring(), strip(), blink(Pin(14), 400), blink(Pin(15), 700))
    await asyncio.gather(*tasks)
    
    
p = aio_neo.pio_neo(12,12)		# create a neopixel object
p.brightness = .1				# set brightness
p2 = aio_neo.pio_neo(17,60)
p2.brightness = .1
asyncio.run(main())
