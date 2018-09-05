import os
from time import sleep_ms
from keypad import Keypad
from keypad import Exit
from machine import I2C, Pin, SPI
from pcf8574 import PCF8574
from i2c_lcd import I2cLcd
from menu import Menu, Navigation
from storrage import Storrage
from helpers import ShiftRegister


spi = SPI(1, baudrate=10000, polarity=0, phase=0)
stcp = Pin(15, Pin.OUT)
oe = Pin(16, Pin.OUT)
sr = ShiftRegister(spi, stcp)

BYTEARRAY = bytearray([0, 0, 0, 0])

oe.value(0)
sr.shift(BYTEARRAY)

KEY_ADDR = 56
LCD_ADDR = 60

KEYMAP = [
    '123A',
    '456B',
    '789C',
    '*0#D'
]
CHARMAP = {
    '1': '.1',    '2': 'abc2', '3': 'def3',
    '4': 'ghi4',  '5': 'jkl5', '6': 'mno6',
    '7': 'pqrs7', '8': 'tuv8', '9': 'wxyz9',
                  '0': '_0',
}

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=40000000)
pcf = PCF8574(i2c, KEY_ADDR)
keypad = Keypad(pcf, KEYMAP, CHARMAP)
lcd = I2cLcd(i2c, LCD_ADDR, 2, 16)
pcf1 = PCF8574(i2c, 57)
pcf2 = PCF8574(i2c, 58)
opto_mask = 0b11111111

storrage = Storrage()


class SettingsErr(Exception):
    pass


class CancelSignal(Exception):
    pass


def prep(banner):
    """ Prepare lcd screen """
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(banner)
    lcd.move_to(0, 1)


def create_program():
    prog = ''
    prep("NAME:")
    try:
        prog += keypad.get_word(lcd) + ','
        prep("HEAT TIME:")
        prog += keypad.get_word(lcd, True) + ','
        prep("COOL TIME:")
        prog += keypad.get_word(lcd, True) + ','
    except Exit:
        return

    if storrage.insert_ln(prog, storrage.programs):
        return 1
    else:
        return 0


def select_line(mode):

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
    fname = storrage.programs if mode in 'ld' else storrage.settings
    last_byte = os.stat(fname)[6] - 1
    f = open(fname, 'r')
    # last = len(f.readlines()) - 1
    f.seek(0)
    start = 0
    if mode in 'ld':
        prep('SELECT PROGRAM:')
    elif mode == 's':
        prep('SELECT SETTING:')

    prog = f.readline()
    prepln(prog)

    while True:
        key = keypad.getkey()
        if key == '8':
            if f.tell() > last_byte:
                f.seek(0, 0)
            start = f.tell()
            prog = f.readline()
            prepln(prog)
        elif key == '2':
            seek_back(f, start)
            start = f.tell()
            prog = f.readline()
            prepln(prog)
        elif key == 'C' or key == '4':  # NOTE added on site
            f.close()
            raise CancelSignal
        elif key == '5' or key == '6':
            f.close()
            return prog
        elif mode == 'd' and key == 'D':
            f.close()
            return prog
        else:
            pass


def operation(name, heat_time, cool_time):
    """
    Wait mask: 0b11101011
    """
    pr501 = 0b00000001
    door = 0b00000010
    fan = 0b00000100
    flow = 0b00001000
    walls = 0b00010000
    press = 0b00100000
    wiggl = 0b01000000
    loose = 0b10000000
    # Reg 2
    up = 0b00000001
    down = 0b00000010
    t_qty = 6
    t_dict = {'t' + str(i): None for i in range(t_qty)}

    def read_settings():
        with open(storrage.settings, 'r') as openedf:
            for line in openedf:
                # TODO make func:
                name, val = line.split(',')[:-1]
                try:
                    t_dict[name] = val
                except KeyError:
                    openedf.close()
                    raise SettingsErr
        openedf.close()

    def shift_mask(mask, reg=0,):
        BYTEARRAY[reg] ^= mask
        BYTEARRAY[reg+1] ^= mask
        sr.shift(BYTEARRAY)

    def wait_mask(mask):
        opto = 0
        while opto != mask:
            opto = pcf1.read8()

    def message(string, count=0):
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr(string)
        if count:
            lcd.move_to(0, 1)
            for t in range(count, 0, -1):
                lcd.putstr('{} sec left  '.format(t))
                sleep_ms(1000)
                lcd.move_to(0, 1)
            # message(string, count - 1)

    def wait(i):
        sleep_ms(int(t_dict[i]))

    try:
        read_settings()
    except SettingsErr:
        message('Wrong settings!')
        return

    message('Starting..\n{}'.format(name))
    wait('t0')  # Iddle
    # Turn pr 501 on
    message('Heating Oven...')
    shift_mask(pr501)
    while True:
        opto_1 = pcf1.read8()
        if opto_1 == 0b11101001 \
           or opto_1 == 0b11100001 \
           or opto_1 == 0b11111001:
            break
    # Open the door and go down
    message('Cycle ctarted!')
    shift_mask(door)
    wait('t1')  # Wait for door to open (3000)
    shift_mask(down, 2)
    wait_mask(0b11101101)  # down
    shift_mask(down, 2)
    shift_mask(door)
    # Waiting
    message('Heating glass.. \n', int(heat_time))
    # Going up
    message('Heated!')
    shift_mask(door | pr501)
    shift_mask(fan)
    wait('t2')  # Wait for door to open (3000)
    shift_mask(up, 2)
    # 1 sw
    message('Pressing...')
    wait_mask(0b11100011)
    shift_mask(up, 2)  # off
    shift_mask(door)  # close
    shift_mask(press)
    wait('t3')  # Press time (4000)
    shift_mask(press | loose)
    wait('t4')  # Wait for press to open (1000)
    # 2 sw
    shift_mask(up, 2)
    wait_mask(0b11111011)
    shift_mask(up, 2)
    shift_mask(walls)
    wait('t5')  # Wait for walls to close (2000)
    shift_mask(flow)
    shift_mask(wiggl)
    message('Cooling glass.. \n', int(cool_time))
    shift_mask(flow | walls | fan | wiggl | loose)  # switch closing pipe off
    message('Cycle ended!')
    sleep_ms(1000)
    lcd.clear


def load_program():
    try:
        prog = select_line('l')
    except CancelSignal:
        return
    if prog is not None:
        lcd.clear()
        lcd.move_to(0, 0)
        res = prog.split(',')[:-1]
        operation(*res)


def delete_program():
    try:
        prog = select_line('d')
    except CancelSignal:
        return
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(
        'Delete program?\n'
        'A:yes     C:no'
    )
    while True:
        key = keypad.getkey()
        if key == 'A':
            storrage.delete_ln(prog.strip('\n'), storrage.programs)
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr('  Deleted!')
            return
        elif key == 'C':
            return
        else:
            pass


def change_settings():
    try:
        setting = select_line('s')
    except CancelSignal:
        return
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr('New value(ms):\n')
    try:
        t = keypad.get_word(lcd, True)
    except Exit:
        return
    res = setting.split(',')[0] + ',{},'.format(t)
    storrage.delete_ln(setting.strip('\n'), storrage.settings)
    storrage.insert_ln(res, storrage.settings)


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
            'Timing',
            'Network',
]

#  Manually construct menu
menu_top = Menu("TOP MENU", menu_top_items)
menu_programs = Menu("PROGRAMS", menu_programs_items, menu_top)
menu_settings = Menu("SETTINGS", menu_settings_items, menu_top)
menu_top.items[0].child = menu_programs
menu_top.items[1].child = menu_settings
menu_programs.items[0].action = load_program
menu_programs.items[1].action = create_program
menu_programs.items[2].action = delete_program
menu_settings.items[0].action = change_settings
nav = Navigation(lcd, keypad, menu_top)


def run():
    nav.start()

    key = ''
    while True:
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
                    pass
                    # break
                else:
                    pass
