#!/usr/bin/env python

"""
    MC6809 - 6809 CPU emulator in Python
    =======================================

    some code is borrowed from:
    XRoar emulator by Ciaran Anscomb (GPL license) more info, see README

    :copyleft: 2013-2015 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import logging


log = logging.getLogger("MC6809")


class ValueStorageBase:
    def __init__(self, name, initial_value):
        self.name = name
        self.value = initial_value

    def set(self, v):
        self.value = v

    def decrement(self, value=1):
        self.set(self.value - value)

    def increment(self, value=1):
        self.set(self.value + value)

    def __str__(self):
        return f"<{self.name}:${self.value:x}>"
    __repr__ = __str__


class UndefinedRegister(ValueStorageBase):
    # used in TFR and EXG
    WIDTH = 16  # 16 Bit
    name = "undefined!"
    value = 0xffff

    def __init__(self):
        pass

    def set(self, v):
        log.warning("Set value to 'undefined' register!")

    def get(self):
        return 0xffff


class ValueStorage8Bit(ValueStorageBase):
    WIDTH = 8  # 8 Bit

    def set(self, v):
        if v > 0xff:
            #            log.info(" **** Value $%x is to big for %s (8-bit)", v, self.name)
            v = v & 0xff
#            log.info(" ^^^^ Value %s (8-bit) wrap around to $%x", self.name, v)
        elif v < 0:
            #            log.info(" **** %s value $%x is negative", self.name, v)
            v = 0x100 + v
#            log.info(" **** Value %s (8-bit) wrap around to $%x", self.name, v)
        self.value = v

    def __str__(self):
        return f"{self.name}={self.value:02x}"


class ValueStorage16Bit(ValueStorageBase):
    WIDTH = 16  # 16 Bit

    def set(self, v):
        if v > 0xffff:
            #            log.info(" **** Value $%x is to big for %s (16-bit)", v, self.name)
            v = v & 0xffff
#            log.info(" ^^^^ Value %s (16-bit) wrap around to $%x", self.name, v)
        elif v < 0:
            #            log.info(" **** %s value $%x is negative", self.name, v)
            v = 0x10000 + v
#            log.info(" **** Value %s (16-bit) wrap around to $%x", self.name, v)
        self.value = v

    def __str__(self):
        return f"{self.name}={self.value:04x}"


class ConcatenatedAccumulator:
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

    @property
    def value(self):
        return self._a.value * 256 + self._b.value

    def __str__(self):
        return f"{self.name}={self.value:04x}"


def convert_differend_width(src_reg, dst_reg):
    """
    e.g.:
     8bit   $cd TFR into 16bit, results in: $ffcd
    16bit $1234 TFR into  8bit, results in:   $34

    >>> reg8 = ValueStorage8Bit(name="bar", initial_value=0xcd)
    >>> reg16 = ValueStorage16Bit(name="foo", initial_value=0x0000)
    >>> hex(convert_differend_width(src_reg=reg8, dst_reg=reg16))
    '0xffcd'

    >>> reg16 = ValueStorage16Bit(name="foo", initial_value=0x1234)
    >>> reg8 = ValueStorage8Bit(name="bar", initial_value=0xcd)
    >>> hex(convert_differend_width(src_reg=reg16, dst_reg=reg8))
    '0x34'

    TODO: verify this behaviour on real hardware
    see: http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=8&t=4886
    """
    src_value = src_reg.value
    if src_reg.WIDTH == 8 and dst_reg.WIDTH == 16:
        # e.g.: $cd -> $ffcd
        src_value += 0xff00
    elif src_reg.WIDTH == 16 and dst_reg.WIDTH == 8:
        # This not not really needed, because all 8Bit register will
        # limit the value, too.
        # e.g.: $1234 -> $34
        src_value = src_value & 0xff
    return src_value


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
