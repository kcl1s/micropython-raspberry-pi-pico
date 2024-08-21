from machine import Pin, Timer

class DB_irq:
    
    def __init__(self, pin, trigger, handler, debounce_ms = 50):
        if trigger == Pin.IRQ_RISING:
            self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)
            self.ck_state = 1
        if trigger == Pin.IRQ_FALLING:
            self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
            self.ck_state = 0
        self.pin.irq(trigger = trigger, handler = self.__handle)
        self.db_ms = debounce_ms
        self.handler = handler
        self.t = Timer()
        
    def __handle(self, pin):
        self.pin.irq(handler = None)
        self.t.init(mode=Timer.ONE_SHOT, period = self.db_ms, callback = self.__t_handle)
        
    def __t_handle(self, t):
        if self.pin.value() == self.ck_state:
            self.handler(self.pin)
        self.pin.irq(handler = self.__handle)
