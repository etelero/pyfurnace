import ure
import os

# Utils


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    split = ure.compile('\d+').split(text)
    split += ure.compile('\D+').split(text)
    return [atoi(c) for c in split]  # if c not ''?


# Modules


class Storrage:
    def __init__(
            self, programs='programs.csv', settings='settings.csv'
    ):
        self.programs = programs
        self.settings = settings

    def __search_alpha_pos(self, name, f):
        line_number = 0
        with open(f, 'r') as openedf:
            for line in openedf:
                if name < line:
                    openedf.close()
                    return line_number
                else:
                    line_number += 1
        openedf.close()
        return line_number

    def insert_prog(self, program) -> int:
        pf = self.programs
        pos = 0
        with open(pf, 'r') as pfo, open(pf + '_', 'w') as pfo_:
            found = 0
            for ln in pfo:
                if program < ln and not found:
                    found += 1
                    pfo_.write(program + '\n')
                    pfo_.write(ln)
                else:
                    pfo_.write(ln)
                if not found:
                    pos += 1
            if not found:
                pfo_.write(program + '\n')
                # pos += 1
        pfo.close()
        pfo_.close()
        os.remove(self.programs)
        os.rename(self.programs + '_', self.programs)
        return pos

    def delete_prog(self, program):
        pf = self.programs
        with open(pf, 'r') as pfo, open(pf + '_', 'w') as pfo_:
            for ln in pfo:
                if str(ln).strip('\n') == program:
                    pass
                else:
                    pfo_.write(ln)
        pfo.close()
        pfo_.close()
        os.remove(self.programs)
        os.rename(self.programs + '_', self.programs)


class ShiftRegister:
    def __init__(self, spi, latch_pin):
        self.spi = spi
        self.latch = latch_pin

    def shift(self, buf):
        self.spi.write(buf)
        self.latch.on()
        self.latch.off()
