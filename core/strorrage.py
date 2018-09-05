""" Module for filesystem operations """

import os


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

    def insert_ln(self, program, fname) -> int:
        pos = 0
        with open(fname, 'r') as pfo, open(fname + '_', 'w') as pfo_:
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
        os.remove(fname)
        os.rename(fname + '_', fname)
        return pos

    def delete_ln(self, program, fname):
        with open(fname, 'r') as pfo, open(fname + '_', 'w') as pfo_:
            for ln in pfo:
                if str(ln).strip('\n') == program:
                    pass
                else:
                    pfo_.write(ln)
        pfo.close()
        pfo_.close()
        os.remove(fname)
        os.rename(fname + '_', fname)
