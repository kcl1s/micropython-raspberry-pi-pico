import asyncio
import time
import aio_neo

async def ring():
    print('ring')
    await p.follow([0,255,0], 5)
    await p.wipe([255,0,0])
    await p.rand_pix(clr_pix=False)
    
async def strip():
    print('strip')
    for x in range(10):
        await p2.fill([255,0,0], True)
        await asyncio.sleep(1)
        await p2.fill([0,0,255], True)
        await asyncio.sleep(1)
    await p2.fill([0,0,0], True)
        
async def main():
    t = (ring(), strip())
    await asyncio.gather(*t)
    
p = aio_neo.pio_neo(12,12)		# create a neopixel object
p.brightness = .1				# set brightness
p2 = aio_neo.pio_neo(17,60)
p2.brightness = .1
asyncio.run(main())
