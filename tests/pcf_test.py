from machine import I2C, Pin
from pcf8574 import PCF8574
from time import sleep_ms

pcf_int = Pin(0, Pin.IN)

ADDR = 0x20
keypad = [
    '123A',
    '456B',
    '789C',
    '*0#D'
]
interrupted = 0


def inter(a):
    # print(a)
    global interrupted
    interrupted += 1


pcf_int.irq(trigger=Pin.IRQ_RISING, handler=inter)


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
    try:
        pressed = lookup(scan(pcf))
    except ValueError:
        print('lookup error')
        sleep_ms(1)
    if pressed is not None:
        letter = pressed
        while pressed is not None:
            try:
                pressed = lookup(scan(pcf))
            except ValueError:
                print('lookup error')
                sleep_ms(1)

        print('key pressed: {}'.format(letter))
        letter = None

print("interrupted {} times".format(interrupted))

del pcf
del i2c
