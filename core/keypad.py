from time import sleep_ms


class SlowPress(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Keypad:
    def __init__(self, pcf, matrix):
        self.pcf = pcf
        self.matrix = matrix
        self.mask = 0b1111
        self.cols = len(matrix)
        self.rows = len(matrix[0])

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
            raise SlowPress('')
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
            sleep_ms(1)
            pressed = self._lookup(self._scan())

        # Catching button up condition:
        letter = pressed
        if pressed is not None:
            while pressed is not None:
                try:
                    pressed = self._lookup(self._scan())
                except SlowPress:
                    sleep_ms(1)
                    pressed = self._lookup(self._scan())
            return letter
        else:
            return None
