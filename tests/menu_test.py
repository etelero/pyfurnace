import time
from keypad import Keypad

from machine import I2C, Pin
from pcf8574 import PCF8574
from machine import I2C, Pin
from i2c_lcd import I2cLcd
from menu import MenuItem, Menu, Navigation

KEY_ADDR = 56
LCD_ADDR = 60

keymap = [
    '123A',
    '456B',
    '789C',
    '*0#D'
]

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=40000000)
pcf = PCF8574(i2c, KEY_ADDR)
keypad = Keypad(pcf, keymap)
lcd = I2cLcd(i2c, LCD_ADDR, 2, 16)

menu_top_items = [
        'Programs',
        'Settings',
]
menu_programs_items = [
            'Load',
            'Create',
            'Delete'
]
menu_settings_items = [
            'Network',
            'Machine'
]

menu_top = Menu("TOP MENU", menu_top_items)
menu_programs = Menu("PROGRAMS", menu_programs_items, menu_top)
menu_settings = Menu("SETTINGS", menu_settings_items, menu_top)
menu_top.items[0].child = menu_programs
menu_top.items[1].child = menu_settings
nav = Navigation(lcd, keypad, menu_top)

nav.start()

# start = time.ticks_ms()
# while time.ticks_diff(time.ticks_ms(), start) < 10000:
key = ''
while key != 'C':
    key = keypad.getkey()
    if key is not None:
        try:
            {
                '2': lambda x: x.up(),
                '8': lambda x: x.down(),
                '5': lambda x: x.enter(),
                '6': lambda x: x.enter(),
                '4': lambda x: x.level_up(),
            }[key](nav)
        except KeyError:
            if key == 'C':
                break
            else:
                pass

del pcf
del i2c
del keypad
del lcd

del menu_top_items
del menu_programs_items
del menu_settings_items
del menu_top
del menu_programs
del menu_settings
del nav
