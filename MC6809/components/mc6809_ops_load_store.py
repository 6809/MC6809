#!/usr/bin/env python
# coding: utf-8

"""
    MC6809 - 6809 CPU emulator in Python
    =======================================

    6809 is Big-Endian

    Links:
        http://dragondata.worldofdragon.org/Publications/inside-dragon.htm
        http://www.burgins.com/m6809.html
        http://koti.mbnet.fi/~atjs/mc6809/

    :copyleft: 2013-2015 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.

    Based on:
        * ApplyPy by James Tauber (MIT license)
        * XRoar emulator by Ciaran Anscomb (GPL license)
    more info, see README
"""

from __future__ import absolute_import, division, print_function


from MC6809.components.cpu_utils.instruction_caller import opcode


class OpsLoadStoreMixin(object):

    # ---- Store / Load ----

    @opcode(# Load register from memory
        0xcc, 0xdc, 0xec, 0xfc, # LDD (immediate, direct, indexed, extended)
        0x10ce, 0x10de, 0x10ee, 0x10fe, # LDS (immediate, direct, indexed, extended)
        0xce, 0xde, 0xee, 0xfe, # LDU (immediate, direct, indexed, extended)
        0x8e, 0x9e, 0xae, 0xbe, # LDX (immediate, direct, indexed, extended)
        0x108e, 0x109e, 0x10ae, 0x10be, # LDY (immediate, direct, indexed, extended)
    )
    def instruction_LD16(self, opcode, m, register):
        """
        Load the contents of the memory location M:M+1 into the designated
        16-bit register.

        source code forms: LDD P; LDX P; LDY P; LDS P; LDU P

        CC bits "HNZVC": -aa0-
        """
#        log.debug("$%x LD16 set %s to $%x \t| %s" % (
#            self.program_counter,
#            register.name, m,
#            self.cfg.mem_info.get_shortest(m)
#        ))
        register.set(m)
        self.clear_NZV()
        self.update_NZ_16(m)

    @opcode(# Load accumulator from memory
        0x86, 0x96, 0xa6, 0xb6, # LDA (immediate, direct, indexed, extended)
        0xc6, 0xd6, 0xe6, 0xf6, # LDB (immediate, direct, indexed, extended)
    )
    def instruction_LD8(self, opcode, m, register):
        """
        Loads the contents of memory location M into the designated register.

        source code forms: LDA P; LDB P

        CC bits "HNZVC": -aa0-
        """
#        log.debug("$%x LD8 %s = $%x" % (
#            self.program_counter,
#            register.name, m,
#        ))
        register.set(m)
        self.clear_NZV()
        self.update_NZ_8(m)

    @opcode(# Store register to memory
        0xdd, 0xed, 0xfd, # STD (direct, indexed, extended)
        0x10df, 0x10ef, 0x10ff, # STS (direct, indexed, extended)
        0xdf, 0xef, 0xff, # STU (direct, indexed, extended)
        0x9f, 0xaf, 0xbf, # STX (direct, indexed, extended)
        0x109f, 0x10af, 0x10bf, # STY (direct, indexed, extended)
    )
    def instruction_ST16(self, opcode, ea, register):
        """
        Writes the contents of a 16-bit register into two consecutive memory
        locations.

        source code forms: STD P; STX P; STY P; STS P; STU P

        CC bits "HNZVC": -aa0-
        """
        value = register.value
#        log.debug("$%x ST16 store value $%x from %s at $%x \t| %s" % (
#             self.program_counter,
#             value, register.name, ea,
#             self.cfg.mem_info.get_shortest(ea)
#         ))
        self.clear_NZV()
        self.update_NZ_16(value)
        return ea, value # write word to Memory

    @opcode(# Store accumulator to memory
        0x97, 0xa7, 0xb7, # STA (direct, indexed, extended)
        0xd7, 0xe7, 0xf7, # STB (direct, indexed, extended)
    )
    def instruction_ST8(self, opcode, ea, register):
        """
        Writes the contents of an 8-bit register into a memory location.

        source code forms: STA P; STB P

        CC bits "HNZVC": -aa0-
        """
        value = register.value
#        log.debug("$%x ST8 store value $%x from %s at $%x \t| %s" % (
#             self.program_counter,
#             value, register.name, ea,
#             self.cfg.mem_info.get_shortest(ea)
#         ))
        self.clear_NZV()
        self.update_NZ_8(value)
        return ea, value # write byte to Memory


