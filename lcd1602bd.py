import machine
import time
### added for big digits KCL
custChar = [[31, 31, 31, 0, 0, 0, 0, 0],      # Small top line - 0
			[0, 0, 0, 0, 0, 31, 31, 31],      # Small bottom line - 1
			[31, 31, 0, 0, 0, 0, 31, 31],       # Small lines top and bottom -2
			[0, 0, 0, 0, 0, 0,  31, 31],       # Thin bottom line - 3
			[31, 31, 31, 31, 31, 31, 15, 7],  # Left bottom chamfer full - 4
			[28, 30, 31, 31, 31, 31, 31, 31], # Right top chamfer full -5
			[31, 31, 31, 31, 31, 31, 30, 28], # Right bottom chamfer full -6
			[7, 15, 31, 31, 31, 31, 31, 31]]  # Left top chamfer full -7

bigNums = [ [7, 0, 5, 4, 1, 6],         #0
			[0, 5, 254, 1, 255, 1],     #1
			[0, 2, 5, 7, 3, 1],         #2
			[0, 2, 5, 1, 3, 6],         #3
			[7, 3, 255, 254, 254, 255], #4
			[255, 2, 0, 1, 3, 6],       #5
			[7, 2, 0, 4, 3, 6],         #6
			[0, 0, 5, 254, 7, 254],     #7
			[7, 2, 5, 4, 3, 6],         #8
			[7, 2, 5, 1, 3, 6]]         #9

class LCD():
    def __init__(self, addr=None, blen=1):
        sda = machine.Pin(6)
        scl = machine.Pin(7)
        self.bus = machine.I2C(1,sda=sda, scl=scl, freq=400000)
        #print(self.bus.scan())
        self.addr = self.scanAddress(addr)
        self.blen = blen
        self.send_command(0x33) # Must initialize to 8-line mode at first
        time.sleep(0.005)
        self.send_command(0x32) # Then initialize to 4-line mode
        time.sleep(0.005)
        self.send_command(0x28) # 2 Lines & 5*7 dots
        time.sleep(0.005)
        self.send_command(0x0C) # Enable display without cursor
        time.sleep(0.005)
        self.send_command(0x01) # Clear Screen
        self.bus.writeto(self.addr, bytearray([0x08]))
        #### add custom chars for big digits KCL
        for x in range(8):
            self.send_command(0x40 | (x << 3))
            for i in range(8):
                self.send_data(custChar[x][i])
        self.send_command(0x01)
        
    def scanAddress(self, addr):
        devices = self.bus.scan()
        if len(devices) == 0:
            raise Exception("No LCD found")
        if addr is not None:
            if addr in devices:
                return addr
            else:
                raise Exception(f"LCD at 0x{addr:2X} not found")
        elif 0x27 in devices:
            return 0x27
        elif 0x3F in devices:
            return 0x3F
        else:
            raise Exception("No LCD found")

    def write_word(self, data):
        temp = data
        if self.blen == 1:
            temp |= 0x08
        else:
            temp &= 0xF7
        self.bus.writeto(self.addr, bytearray([temp]))
    
    def send_command(self, cmd):
        # Send bit7-4 firstly
        buf = cmd & 0xF0
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        self.write_word(buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.write_word(buf)

        # Send bit3-0 secondly
        buf = (cmd & 0x0F) << 4
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        self.write_word(buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.write_word(buf)
    
    def send_data(self, data):
        # Send bit7-4 firstly
        buf = data & 0xF0
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        self.write_word(buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.write_word(buf)

        # Send bit3-0 secondly
        buf = (data & 0x0F) << 4
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        self.write_word(buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.write_word(buf)
    
    def clear(self):
        self.send_command(0x01) # Clear Screen
        
    def openlight(self):  # Enable the backlight
        self.bus.writeto(self.addr,bytearray([0x08]))
        # self.bus.close()
    
    def write(self, x, y, str):
        if x < 0:
            x = 0
        if x > 15:
            x = 15
        if y < 0:
            y = 0
        if y > 1:
            y = 1

        # Move cursor
        addr = 0x80 + 0x40 * y + x
        self.send_command(addr)

        for chr in str:
            self.send_data(ord(chr))
    
    def message(self, text):
        #print("message: %s"%text)
        for char in text:
            if char == '\n':
                self.send_command(0xC0) # next line
            else:
                self.send_data(ord(char))
                
    # New method for BD KCL
    def bigDigit(self,col, digit):			# (col, digit 0-9)
        col = min(15, max(0, int(col)))		#constrain col value 0 to 15
        digit = min(9, max(0, int(digit)))	#constrain digit col value 0 to 9

        # Move cursor top row
        curPos = 0x80 + col			#same as 0x80 + 0x40 * (row = 0) + col
        self.send_command(curPos)
        for cc in range(0,3):
            self.send_data(bigNums[digit][cc])
        
        # Move cursor second row
        curPos = 0x80 + 0x40 + col	#same as 0x80 + 0x40 * (row = 1) + col
        self.send_command(curPos)
        for cc in range(3,6):
            self.send_data(bigNums[digit][cc])
