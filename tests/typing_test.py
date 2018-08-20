from machine import I2C, Pin
from time import sleep_ms
from pcf8574 import PCF8574
from i2c_lcd import I2cLcd
from keypad import Keypad, Exit

DEFAULT_I2C_ADDR = 60
ADDR = 56

def test_main():
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)
    pcf = PCF8574(i2c, ADDR)
    keymap = [
        '123A',
        '456B',
        '789C',
        '*0#D'
    ]
    charmap = {
        '1': '.1',    '2': 'abc2', '3': 'def3',
        '4': 'ghi4',  '5': 'jkl5', '6': 'mno6',
        '7': 'pqrs7', '8': 'tuv8', '9': 'wxyz9',
                      '0': '_0',
    }
    keypad = Keypad(pcf, keymap, charmap)

    lcd.clear()
    lcd.show_cursor()
    try:
        word = keypad.get_word(lcd)
        print("Got {} as input".format(word))
    except Exit:
        print('Received exit')

    lcd.clear()
    try:
        word = keypad.get_word(lcd, True)
        print("Got {} as input".format(word))
    except Exit:
        print('Received exit')

test_main()
