import time
import os
from keypad import Keypad

from machine import I2C, Pin
from pcf8574 import PCF8574
from machine import I2C, Pin
from i2c_lcd import I2cLcd
from menu import MenuItem, Menu, Navigation
from main import Storrage


KEY_ADDR = 56
LCD_ADDR = 60

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

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=40000000)
pcf = PCF8574(i2c, KEY_ADDR)
keypad = Keypad(pcf, keymap, charmap)
lcd = I2cLcd(i2c, LCD_ADDR, 2, 16)
# f = open('programs.csv', 'w')
# f.close()
storrage = Storrage()

def prep(banner):
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(banner)
    lcd.move_to(0, 1)

def create_program():

    prog = ''
    prep("NAME:")
    prog += keypad.get_word(lcd) + ','
    prep("HEAT TIME:")
    prog += keypad.get_word(lcd, True) + ','
    prep("COOL TIME:")
    prog += keypad.get_word(lcd, True) + ','

    if storrage.insert_prog(prog):
        return 1
    else:
        return 0

def load_program():

    def prepln(ln):
        lcd.putstr(ln[:ln.find(',')])
        lcd.putstr(''.join([' ' for i in range(16 - len(ln))]))
        lcd.move_to(0, 1)

    def seek_back(f, st):
        f.seek(st)
        f.seek(-2, 1)
        while f.read(1) != '\n' and f.tell() > 1:
            f.seek(-2, 1)
        return f.tell()

    last_byte = os.stat(storrage.programs)[6] - 1
    f = open(storrage.programs, 'r')
    last = len(f.readlines()) - 1
    f.seek(0)
    start = 0
    prep('SELECT PROGRAM:')
    prog = f.readline()
    prepln(prog)

    while True:
        key = keypad.getkey()
        if key == '8':
            if f.tell() > last_byte:
                f.seek(0,0)
            start = f.tell()
            prog = f.readline()
            prepln(prog)
        elif key == '2':
            seek_back(f, start)
            start = f.tell()
            prog = f.readline()
            prepln(prog)
        elif key == 'C':
            f.close()
            return
        elif key == '5' or key == '6':
            f.close()
            return prog
        else:
            pass

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
menu_programs.items[0].action = load_program
menu_programs.items[1].action = create_program
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
del storrage
