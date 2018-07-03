from machine import I2C, Pin
from pcf8574 import PCF8574

ADDR = 0x20
keypad = [
    '123A',
    '456B',
    '789C',
    '*0#D'
]


def scan(pcf):
    pos = []
    pcf.write8(0b00001111)
    pos.append(pcf.read8(0b11110000))
    pcf.write8(0b11110000)
    pos.append(pcf.read8(0b00001111))
    return pos


def lookup(scan):
    if scan == [240, 15]:
        return None
    x, y = scan
    cols = [7, 11, 13, 14]
    rows = [112, 176, 208, 224]
    look = [cols.index(y), rows.index(x)]
    return keypad[look[1]][look[0]]


i2c = I2C(scl=Pin(5), sda=Pin(4), freq=40000000)
pcf = PCF8574(i2c, ADDR)

for i in range(1000):
    letter = lookup(scan(pcf))
    if letter is not None:
        print('key pressed: {}'.format(letter))
        break

del pcf
del i2c
