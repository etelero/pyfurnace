import time
from keypad import Keypad

from machine import I2C, Pin
from pcf8574 import PCF8574

ADDR = 0x20
keymap = [
    '123A',
    '456B',
    '789C',
    '*0#D'
]
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=40000000)
pcf = PCF8574(i2c, ADDR)
keypad = Keypad(pcf, keymap)

# print('rows cols = [{}, {}]'.format(keypad.rows, keypad.cols))
start = time.ticks_ms()
while time.ticks_diff(time.ticks_ms(), start) < 5000:
    key = keypad.getkey()
    if key is not None:
        print('Key pressed {}'.format(key))

del pcf
del i2c
del keypad
