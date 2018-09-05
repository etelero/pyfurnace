import time


class Exit(Exception):
    pass


class Accept(Exception):
    pass


class Delete(Exception):
    pass


class CharSwitch(Exception):
    pass


class Caps(Exception):
    pass


class Unknown(Exception):
    pass


class SlowPress(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Keypad:
    def __init__(self, pcf, matrix, charmap=None):
        self.pcf = pcf
        self.matrix = matrix
        self.charmap = charmap
        self.mask = 0b1111
        self.cols = len(matrix)
        self.rows = len(matrix[0])
        self.caps = False
        self.lcd_pos = 0

    def _scan(self):
        press = bytearray(2)
        self.pcf.write8(self.mask)
        press[0] = self.pcf.read8(self.mask << 4) >> 4
        self.pcf.write8(self.mask << 4)
        press[1] = self.pcf.read8(self.mask)
        return press

    def _lookup(self, press):
        y, x = press
        if press == b'\x0f\x0f':  # NOTE Magic
            return None
        if x == self.mask or y == self.mask:
            return None
            # raise SlowPress('')
        key = ''
        for c in range(self.cols):
            if y == self.mask ^ 1 << c:
                key = self.matrix[~c]
                break
            if c+1 >= self.cols:
                return None  # KeyChord
        for r in range(self.rows):
            if x == self.mask ^ 1 << r:
                key = key[~r]
                break
            if r+1 >= self.rows:
                return None  # KeyChord
        return key

    def getkey(self):
        try:
            pressed = self._lookup(self._scan())
        except SlowPress:
            time.sleep_ms(1)
            pressed = self._lookup(self._scan())

        # Catching button up condition:
        letter = pressed
        if pressed is not None:
            while pressed is not None:
                try:
                    pressed = self._lookup(self._scan())
                except SlowPress:
                    time.sleep_ms(1)
                    pressed = self._lookup(self._scan())
            return letter
        else:
            return None

    def get_word(self, lcd, num=False):

        def control(key, char=None):
            if key == 'C':
                raise Exit
            elif key == 'A':
                raise Accept(char)
            elif key == 'D':
                raise Delete(char)
            elif key == '#':
                raise Caps(char)
            elif key in 'B*':
                raise Unknown(char)

        def get_char(fkey):
            alpha = self.charmap[fkey]
            pos = 0
            pos_max = len(alpha) - 1
            char = alpha[pos] if not self.caps else alpha[pos].upper()
            lcd.move_to(self.lcd_pos, 1)
            lcd.putstr(char)
            start = time.ticks_ms()
            while time.ticks_diff(time.ticks_ms(), start) < 1000:
                key = self.getkey()
                if key is not None:
                    if key == fkey:
                        start = time.ticks_ms()
                        lcd.move_to(self.lcd_pos, 1)
                        pos = pos + 1 if pos < pos_max else 0
                        char = alpha[pos] if not self.caps \
                            else alpha[pos].upper()
                        lcd.putstr(char)
                        key = None
                    elif 48 <= ord(key) <= 57:
                        self.lcd_pos += 1
                        raise CharSwitch(char + key)
                    else:
                        control(key, char)
            self.lcd_pos += 1
            return char

        word = ''
        key = None
        lcd.move_to(self.lcd_pos, 1)
        try:
            while True:
                while key is None:
                    key = self.getkey()
                try:
                    control(key)
                    if not num:
                        char = get_char(key)
                    else:
                        char = key
                        lcd.putstr(key)
                        self.lcd_pos += 1
                    word += char
                    key = None
                except CharSwitch as ck:
                    ck = str(ck)
                    word += ck[0]
                    key = ck[1]
                except Delete as ck:
                    if ck.args[0] is None:
                        word = word[:-1]
                        self.lcd_pos -= 1
                    lcd.move_to(self.lcd_pos, 1)
                    lcd.putstr(' ')
                    if num:
                        lcd.move_to(self.lcd_pos, 1)
                    key = None
                except Caps as c:
                    if c.args[0] is not None:
                        word += str(c)
                        lcd.move_to(self.lcd_pos, 1)
                        self.lcd_pos += 1
                    self.caps = not self.caps
                    key = None
                except Unknown:
                    self.lcd_pos += 1
                    key = None

        except Accept as c:
            word = word + str(c) if c.args[0] is not None else word
            self.lcd_pos = 0
            return word
