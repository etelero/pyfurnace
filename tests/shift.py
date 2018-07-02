from machine import SPI, Pin
from main import ShiftRegister
from time import sleep

spi = SPI(1, baudrate=10000, polarity=0, phase=0)
stcp = Pin(15, Pin.OUT)
oe = Pin(2, Pin.OUT)
sr = ShiftRegister(spi, stcp)

oe.value(0)
sr.shift(bytearray([0]))

print('[MANUAL] Shift test')
for j in range(10, 100, 20):
    for i in range(8):
        sr.shift(bytearray([0b1 << i]))
        sleep(1/j)

for i in range(256):
    sr.shift(bytearray([i]))
    sleep(0.01)
sr.shift(bytearray([0]))

# testing output enable pin
sr.shift(bytearray([0b11111111]))
sleep(0.5)
oe.value(0.1)
sleep(0.5)
oe.value(0)
sleep(0.5)
sr.shift(bytearray([0b0]))

spi.deinit()
del sr

print('... Shift test end')
