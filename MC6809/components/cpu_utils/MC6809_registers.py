#!/usr/bin/env python

"""
    MC6809 - 6809 CPU emulator in Python
    =======================================

    some code is borrowed from:
    XRoar emulator by Ciaran Anscomb (GPL license) more info, see README

    :copyleft: 2013-2014 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function


from MC6809.utils.humanize import cc_value2txt
import logging

log=logging.getLogger("MC6809")


class ValueStorage(object):
    BASE = 0
    def __init__(self, name, initial_value):
        self.name = name
        self.value = initial_value

    def set(self, v):
        self.value = v & self.BASE
        return self.value

    def decrement(self, value=1):
        self.value = (self.value - value) & self.BASE
        return self.value
    def increment(self, value=1):
        self.value = (self.value + value) & self.BASE
        return self.value

    def __str__(self):
        return "<%s:$%x>" % (self.name, self.value)
    __repr__ = __str__


class UndefinedRegister(ValueStorage):
    # used in TFR and EXG
    WIDTH = 16  # 16 Bit
    BASE = 0
    name = "undefined!"
    value = 0xffff
    def __init__(self):
        pass
    def set(self, v):
        log.warning("Set value to 'undefined' register!")
        pass


class ValueStorage8Bit(ValueStorage):
    WIDTH = 8  # 8 Bit
    BASE = 255

    def __str__(self):
        return "%s=%02x" % (self.name, self.value)


class ValueStorage16Bit(ValueStorage):
    WIDTH = 16  # 16 Bit
    BASE = 65535

    def __str__(self):
        return "%s=%04x" % (self.name, self.value)


class ConditionCodeRegister(object):
    """ CC - 8 bit condition code register bits """

    WIDTH = 8  # 8 Bit

    def __init__(self, *cmd_args, **kwargs):
        self.name = "CC"
        self._register = {}
        self.E = 0  # E - 0x80 - bit 7 - Entire register state stacked
        self.F = 0  # F - 0x40 - bit 6 - FIRQ interrupt masked
        self.H = 0  # H - 0x20 - bit 5 - Half-Carry
        self.I = 0  # I - 0x10 - bit 4 - IRQ interrupt masked
        self.N = 0  # N - 0x08 - bit 3 - Negative result (twos complement)
        self.Z = 0  # Z - 0x04 - bit 2 - Zero result
        self.V = 0  # V - 0x02 - bit 1 - Overflow
        self.C = 0  # C - 0x01 - bit 0 - Carry (or borrow)

    ####

    @property
    def value(self):
        return self.C | \
            self.V << 1 | \
            self.Z << 2 | \
            self.N << 3 | \
            self.I << 4 | \
            self.H << 5 | \
            self.F << 6 | \
            self.E << 7

    def set(self, status):
        self.E, self.F, self.H, self.I, self.N, self.Z, self.V, self.C = \
            [0 if status & x == 0 else 1 for x in (128, 64, 32, 16, 8, 4, 2, 1)]

    @property
    def get_info(self):
        """
        >>> cc=ConditionCodeRegister()
        >>> cc.set(0xa1)
        >>> cc.get_info
        'E.H....C'
        """
        return cc_value2txt(self.value)

    def __str__(self):
        return "%s=%s" % (self.name, self.get_info)

    ####

    """
    #define SET_Z(r)          ( REG_CC |= ((r) ? 0 : CC_Z) )
    #define SET_N8(r)         ( REG_CC |= (r&0x80)>>4 )
    #define SET_N16(r)        ( REG_CC |= (r&0x8000)>>12 )
    #define SET_H(a,b,r)      ( REG_CC |= ((a^b^r)&0x10)<<1 )
    #define SET_C8(r)         ( REG_CC |= (r&0x100)>>8 )
    #define SET_C16(r)        ( REG_CC |= (r&0x10000)>>16 )
    #define SET_V8(a,b,r)     ( REG_CC |= ((a^b^r^(r>>1))&0x80)>>6 )
    #define SET_V16(a,b,r)    ( REG_CC |= ((a^b^r^(r>>1))&0x8000)>>14 )
    """

    def set_H(self, a, b, r):
        if not self.H and (a ^ b ^ r) & 0x10:
            self.H = 1
#            log.debug("\tset_H(): set half-carry flag to %i: ($%02x ^ $%02x ^ $%02x) & 0x10 = $%02x",
#                self.H, a, b, r, r2
#            )
#        else:
#            log.debug("\rset_H(): leave old value 1")

    def set_Z8(self, r):
        if self.Z == 0:
            r2 = r & 0xff
            self.Z = 1 if r2 == 0 else 0
#            log.debug("\tset_Z8(): set zero flag to %i: $%02x & 0xff = $%02x",
#                self.Z, r, r2
#            )
#        else:
#            log.debug("\tset_Z8(): leave old value 1")

    def set_Z16(self, r):
        if not self.Z and not r & 0xffff:
            self.Z = 1
#            log.debug("\tset_Z16(): set zero flag to %i: $%04x & 0xffff = $%04x",
#                self.Z, r, r2
#            )
#        else:
#            log.debug("\tset_Z16(): leave old value 1")

    def set_N8(self, r):
        if not self.N and r & 0x80:
            self.N = 1
#            log.debug("\tset_N8(): set negative flag to %i: ($%02x & 0x80) = $%02x",
#                self.N, r, r2
#            )
#        else:
#            log.debug("\tset_N8(): leave old value 1")

    def set_N16(self, r):
        if not self.N and r & 0x8000:
            self.N = 1
#            log.debug("\tset_N16(): set negative flag to %i: ($%04x & 0x8000) = $%04x",
#                self.N, r, r2
#            )
#        else:
#            log.debug("\tset_N16(): leave old value 1")

    def set_C8(self, r):
        if not self.C and r & 0x100:
            self.C = 1
#            log.debug("\tset_C8(): carry flag to %i: ($%02x & 0x100) = $%02x",
#                self.C, r, r2
#            )
#         else:
#            log.debug("\tset_C8(): leave old value 1")

    def set_C16(self, r):
        if not self.C and r & 0x10000:
            self.C = 1
#            log.debug("\tset_C16(): carry flag to %i: ($%04x & 0x10000) = $%04x",
#                self.C, r, r2
#            )
#         else:
#            log.debug("\tset_C16(): leave old value 1")

    def set_V8(self, a, b, r):
        if not self.V and (a ^ b ^ r ^ (r >> 1)) & 0x80:
            self.V = 1
#            log.debug("\tset_V8(): overflow flag to %i: (($%02x ^ $%02x ^ $%02x ^ ($%02x >> 1)) & 0x80) = $%02x",
#                self.V, a, b, r, r, r2
#            )
#         else:
#            log.debug("\tset_V8(): leave old value 1")

    def set_V16(self, a, b, r):
        if not self.V and (a ^ b ^ r ^ (r >> 1)) & 0x8000:
            self.V = 1
#            log.debug("\tset_V16(): overflow flag to %i: (($%04x ^ $%04x ^ $%04x ^ ($%04x >> 1)) & 0x8000) = $%04x",
#                self.V, a, b, r, r, r2
#            )
#         else:
#            log.debug("\tset_V16(): leave old value 1")

    ####

    def clear_NZ(self):
#        log.debug("\tclear_NZ()")
        self.N = 0
        self.Z = 0

    def clear_NZC(self):
#        log.debug("\tclear_NZC()")
        self.N = 0
        self.Z = 0
        self.C = 0

    def clear_NZV(self):
#        log.debug("\tclear_NZV()")
        self.N = 0
        self.Z = 0
        self.V = 0

    def clear_NZVC(self):
#        log.debug("\tclear_NZVC()")
        self.N = 0
        self.Z = 0
        self.V = 0
        self.C = 0

    def clear_HNZVC(self):
#        log.debug("\tclear_HNZVC()")
        self.H = 0
        self.N = 0
        self.Z = 0
        self.V = 0
        self.C = 0

    ####

    def update_NZ_8(self, r):
        if not self.N and r & 0x80:
            self.N = 1
        if not self.Z and not r & 0xff:
            self.Z = 1

    def update_0100(self):
        """ CC bits "HNZVC": -0100 """
        self.N = 0
        self.Z = 1
        self.V = 0
        self.C = 0

    def update_NZ01_8(self, r):
        if not self.N and r & 0x80:
            self.N = 1
        if not self.Z and not r & 0xff:
            self.Z = 1
        self.V = 0
        self.C = 1

    def update_NZ_16(self, r):
        if not self.N and r & 0x8000:
            self.N = 1
        if not self.Z and not r & 0xffff:
            self.Z = 1

    def update_NZ0_8(self, r):
        if not self.N and r & 0x80:
            self.N = 1
        if not self.Z and not r & 0xff:
            self.Z = 1
        self.V = 0

    def update_NZ0_16(self, r):
        if not self.N and r & 0x8000:
            self.N = 1
        if not self.Z and not r & 0xffff:
            self.Z = 1
        self.V = 0

    def update_NZC_8(self, r):
        if not self.N and r & 0x80:
            self.N = 1
        if not self.Z and not r & 0xff:
            self.Z = 1
        if not self.C and r & 0x100:
            self.C = 1

    def update_NZVC_8(self, a, b, r):
        if not self.N and r & 0x80:
            self.N = 1
        if not self.Z and not r & 0xff:
            self.Z = 1
        if not self.V and (a ^ b ^ r ^ (r >> 1)) & 0x80:
            self.V = 1
        if not self.C and r & 0x100:
            self.C = 1

    def update_NZVC_16(self, a, b, r):
        if not self.N and r & 0x8000:
            self.N = 1
        if not self.Z and not r & 0xffff:
            self.Z = 1
        if not self.V and (a ^ b ^ r ^ (r >> 1)) & 0x8000:
            self.V = 1
        if not self.C and r & 0x10000:
            self.C = 1

    def update_HNZVC_8(self, a, b, r):
        if not self.H and (a ^ b ^ r) & 0x10:
            self.H = 1
        if not self.N and r & 0x80:
            self.N = 1
        if not self.Z and not r & 0xff:
            self.Z = 1
        if not self.V and (a ^ b ^ r ^ (r >> 1)) & 0x80:
            self.V = 1
        if not self.C and r & 0x100:
            self.C = 1


class ConcatenatedAccumulator(object):
    """
    6809 has register D - 16 bit concatenated reg. (A + B)
    """
    WIDTH = 16  # 16 Bit

    def __init__(self, name, a, b):
        self.name = name
        self._a = a
        self._b = b

    def set(self, value):
        self._a.set(value >> 8)
        self._b.set(value & 0xff)

    def __str__(self):
        return "%s=%04x" % (self.name, self.get())

    @property
    def value(self):
        return (self._a.value << 8) | self._b.value


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
