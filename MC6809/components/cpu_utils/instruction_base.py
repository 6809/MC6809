#!/usr/bin/env python

"""
    MC6809 - 6809 CPU emulator in Python
    =======================================

    :copyleft: 2013-2014 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function



class InstructionBase(object):
    def __init__(self, cpu, instr_func):
        self.cpu = cpu
        self.instr_func = instr_func

    def special(self, opcode):
        # e.g: RESET and PAGE 1/2
        return self.instr_func(opcode)


