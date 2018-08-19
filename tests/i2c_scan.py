from machine import I2C, Pin

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=40000000)
res = i2c.scan()
if res:
    res = ' '.join([str(i) for i in res])
    print('Devices with addresses '
          'are present on the bus {}'.format(res))
else:
    print('No I2C devices')

del i2c
