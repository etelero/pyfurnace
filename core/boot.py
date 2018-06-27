import ure

# Setup ----------------------------------------------------------------------
# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
import gc
# import webrepl
# webrepl.start()
gc.collect()


# Utils -----------------------------------------------------------------------


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    split = ure.compile('\d+').split(text)
    split += ure.compile('\D+').split(text)
    return [atoi(c) for c in split]  # if c not ''?


# Modules ---------------------------------------------------------------------


class Storrage:
    def __init__(
            self, programs='programs.csv', settings='settings.csv'
    ):
        self.programs = programs
        self.settings = settings

    def __search_alpha_pos(self, name):
        with open(self.programs, 'r') as openedf, int() as line_number:
            for line in openedf:
                if [name, line].sort(key=natural_keys)[0] == name:
                    return line_number
                else:
                    line_number += 1
        openedf.close()
