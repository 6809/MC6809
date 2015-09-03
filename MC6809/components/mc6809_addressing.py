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


from MC6809.utils.bits import is_bit_set
from MC6809.utils.byte_word_values import signed8, signed16, signed5
from MC6809.components.MC6809data.MC6809_op_data import (
    REG_S, REG_U, REG_X, REG_Y
)

class AddressingMixin(object):

    def get_m_immediate(self):
        ea, m = self.read_pc_byte()
#        log.debug("\tget_m_immediate(): $%x from $%x", m, ea)
        return m

    def get_m_immediate_word(self):
        ea, m = self.read_pc_word()
#        log.debug("\tget_m_immediate_word(): $%x from $%x", m, ea)
        return m

    def get_ea_direct(self):
        op_addr, m = self.read_pc_byte()
        dp = self.direct_page.value
        ea = dp << 8 | m
#        log.debug("\tget_ea_direct(): ea = dp << 8 | m  =>  $%x=$%x<<8|$%x", ea, dp, m)
        return ea

    def get_ea_m_direct(self):
        ea = self.get_ea_direct()
        m = self.memory.read_byte(ea)
#        log.debug("\tget_ea_m_direct(): ea=$%x m=$%x", ea, m)
        return ea, m

    def get_m_direct(self):
        ea = self.get_ea_direct()
        m = self.memory.read_byte(ea)
#        log.debug("\tget_m_direct(): $%x from $%x", m, ea)
        return m

    def get_m_direct_word(self):
        ea = self.get_ea_direct()
        m = self.memory.read_word(ea)
#        log.debug("\tget_m_direct(): $%x from $%x", m, ea)
        return m

    INDEX_POSTBYTE2STR = {
        0x00: REG_X, # 16 bit index register
        0x01: REG_Y, # 16 bit index register
        0x02: REG_U, # 16 bit user-stack pointer
        0x03: REG_S, # 16 bit system-stack pointer
    }
    def get_ea_indexed(self):
        """
        Calculate the address for all indexed addressing modes
        """
        addr, postbyte = self.read_pc_byte()
#        log.debug("\tget_ea_indexed(): postbyte: $%02x (%s) from $%04x",
#             postbyte, byte2bit_string(postbyte), addr
#         )

        rr = (postbyte >> 5) & 3
        try:
            register_str = self.INDEX_POSTBYTE2STR[rr]
        except KeyError:
            raise RuntimeError("Register $%x doesn't exists! (postbyte: $%x)" % (rr, postbyte))

        register_obj = self.register_str2object[register_str]
        register_value = register_obj.value
#        log.debug("\t%02x == register %s: value $%x",
#             rr, register_obj.name, register_value
#         )

        if not is_bit_set(postbyte, bit=7): # bit 7 == 0
            # EA = n, R - use 5-bit offset from post-byte
            offset = signed5(postbyte & 0x1f)
            ea = register_value + offset
#             log.debug(
#                 "\tget_ea_indexed(): bit 7 == 0: reg.value: $%04x -> ea=$%04x + $%02x = $%04x",
#                 register_value, register_value, offset, ea
#             )
            return ea

        addr_mode = postbyte & 0x0f
        self.cycles += 1
        offset = None
        # TODO: Optimized this, maybe use a dict mapping...
        if addr_mode == 0x0:
#             log.debug("\t0000 0x0 | ,R+ | increment by 1")
            ea = register_value
            register_obj.increment(1)
        elif addr_mode == 0x1:
#             log.debug("\t0001 0x1 | ,R++ | increment by 2")
            ea = register_value
            register_obj.increment(2)
            self.cycles += 1
        elif addr_mode == 0x2:
#             log.debug("\t0010 0x2 | ,R- | decrement by 1")
            register_obj.decrement(1)
            ea = register_obj.value
        elif addr_mode == 0x3:
#             log.debug("\t0011 0x3 | ,R-- | decrement by 2")
            register_obj.decrement(2)
            ea = register_obj.value
            self.cycles += 1
        elif addr_mode == 0x4:
#             log.debug("\t0100 0x4 | ,R | No offset")
            ea = register_value
        elif addr_mode == 0x5:
#             log.debug("\t0101 0x5 | B, R | B register offset")
            offset = signed8(self.accu_b.value)
        elif addr_mode == 0x6:
#             log.debug("\t0110 0x6 | A, R | A register offset")
            offset = signed8(self.accu_a.value)
        elif addr_mode == 0x8:
#             log.debug("\t1000 0x8 | n, R | 8 bit offset")
            offset = signed8(self.read_pc_byte()[1])
        elif addr_mode == 0x9:
#             log.debug("\t1001 0x9 | n, R | 16 bit offset")
            offset = signed16(self.read_pc_word()[1])
            self.cycles += 1
        elif addr_mode == 0xa:
#             log.debug("\t1010 0xa | illegal, set ea=0")
            ea = 0
        elif addr_mode == 0xb:
#             log.debug("\t1011 0xb | D, R | D register offset")
            # D - 16 bit concatenated reg. (A + B)
            offset = signed16(self.accu_d.value) # FIXME: signed16() ok?
            self.cycles += 1
        elif addr_mode == 0xc:
#             log.debug("\t1100 0xc | n, PCR | 8 bit offset from program counter")
            __, value = self.read_pc_byte()
            value_signed = signed8(value)
            ea = self.program_counter.value + value_signed
#             log.debug("\tea = pc($%x) + $%x = $%x (dez.: %i + %i = %i)",
#                 self.program_counter, value_signed, ea,
#                 self.program_counter, value_signed, ea,
#             )
        elif addr_mode == 0xd:
#             log.debug("\t1101 0xd | n, PCR | 16 bit offset from program counter")
            __, value = self.read_pc_word()
            value_signed = signed16(value)
            ea = self.program_counter.value + value_signed
            self.cycles += 1
#             log.debug("\tea = pc($%x) + $%x = $%x (dez.: %i + %i = %i)",
#                 self.program_counter, value_signed, ea,
#                 self.program_counter, value_signed, ea,
#             )
        elif addr_mode == 0xe:
#             log.error("\tget_ea_indexed(): illegal address mode, use 0xffff")
            ea = 0xffff # illegal
        elif addr_mode == 0xf:
#             log.debug("\t1111 0xf | [n] | 16 bit address - extended indirect")
            __, ea = self.read_pc_word()
        else:
            raise RuntimeError("Illegal indexed addressing mode: $%x" % addr_mode)

        if offset is not None:
            ea = register_value + offset
#             log.debug("\t$%x + $%x = $%x (dez: %i + %i = %i)",
#                 register_value, offset, ea,
#                 register_value, offset, ea
#             )

        ea = ea & 0xffff

        if is_bit_set(postbyte, bit=4): # bit 4 is 1 -> Indirect
#             log.debug("\tIndirect addressing: get new ea from $%x", ea)
            ea = self.memory.read_word(ea)
#             log.debug("\tIndirect addressing: new ea is $%x", ea)

#        log.debug("\tget_ea_indexed(): return ea=$%x", ea)
        return ea

    def get_m_indexed(self):
        ea = self.get_ea_indexed()
        m = self.memory.read_byte(ea)
#        log.debug("\tget_m_indexed(): $%x from $%x", m, ea)
        return m

    def get_ea_m_indexed(self):
        ea = self.get_ea_indexed()
        m = self.memory.read_byte(ea)
#        log.debug("\tget_ea_m_indexed(): ea = $%x m = $%x", ea, m)
        return ea, m

    def get_m_indexed_word(self):
        ea = self.get_ea_indexed()
        m = self.memory.read_word(ea)
#        log.debug("\tget_m_indexed_word(): $%x from $%x", m, ea)
        return m

    def get_ea_extended(self):
        """
        extended indirect addressing mode takes a 2-byte value from post-bytes
        """
        attr, ea = self.read_pc_word()
#        log.debug("\tget_ea_extended() ea=$%x from $%x", ea, attr)
        return ea

    def get_m_extended(self):
        ea = self.get_ea_extended()
        m = self.memory.read_byte(ea)
#        log.debug("\tget_m_extended(): $%x from $%x", m, ea)
        return m

    def get_ea_m_extended(self):
        ea = self.get_ea_extended()
        m = self.memory.read_byte(ea)
#        log.debug("\tget_m_extended(): ea = $%x m = $%x", ea, m)
        return ea, m

    def get_m_extended_word(self):
        ea = self.get_ea_extended()
        m = self.memory.read_word(ea)
#        log.debug("\tget_m_extended_word(): $%x from $%x", m, ea)
        return m

    def get_ea_relative(self):
        addr, x = self.read_pc_byte()
        x = signed8(x)
        ea = self.program_counter.value + x
#        log.debug("\tget_ea_relative(): ea = $%x + %i = $%x \t| %s",
#            self.program_counter, x, ea,
#            self.cfg.mem_info.get_shortest(ea)
#        )
        return ea

    def get_ea_relative_word(self):
        addr, x = self.read_pc_word()
        ea = self.program_counter.value + x
#        log.debug("\tget_ea_relative_word(): ea = $%x + %i = $%x \t| %s",
#            self.program_counter, x, ea,
#            self.cfg.mem_info.get_shortest(ea)
#        )
        return ea
