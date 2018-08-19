import time

from machine import I2C, Pin
from pcf8574 import PCF8574

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=40000000)
pcf1 = PCF8574(i2c, 57)
pcf2 = PCF8574(i2c, 58)

# pcf.write8(0b00000000)
res1 = pcf1.read8(0b11111111)
res2 = pcf2.read8(0b11111111)

print('Opto read is {}, {}'.format(bin(res1), bin(res2)))

del pcf1
del pcf2
del i2c
