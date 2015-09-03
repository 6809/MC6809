#!/usr/bin/env python

"""
    6809 unittests
    ~~~~~~~~~~~~~~

    Test shift / rotate

    :created: 2013-2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2013-2015 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

import logging
import sys
import unittest

PY2 = sys.version_info[0] == 2
if PY2:
    range = xrange

from MC6809.tests.test_base import BaseCPUTestCase
from MC6809.utils.bits import is_bit_set, get_bit


log = logging.getLogger("MC6809")


class Test6809_LogicalShift(BaseCPUTestCase):
    """
    unittests for:
        * LSL (Logical Shift Left) alias ASL (Arithmetic Shift Left)
        * LSR (Logical Shift Right) alias ASR (Arithmetic Shift Right)
    """
    def test_LSRA_inherent(self):
        """
        Example assembler code to test LSRA/ASRA

        CLRB        ; B is always 0
        TFR B,U     ; clear U
loop:
        TFR U,A     ; for next test
        TFR B,CC    ; clear CC
        LSRA
        NOP
        LEAU 1,U    ; inc U
        JMP loop
        """
        for i in range(0x100):
            self.cpu.accu_a.set(i)
            self.cpu.set_cc(0x00) # Clear all CC flags
            self.cpu_test_run(start=0x1000, end=None, mem=[
                0x44, # LSRA/ASRA Inherent
            ])
            r = self.cpu.accu_a.value
#             print "%02x %s > ASRA > %02x %s -> %s" % (
#                 i, '{0:08b}'.format(i),
#                 r, '{0:08b}'.format(r),
#                 self.cpu.get_cc_info()
#             )

            # test LSL result
            r2 = i >> 1 # shift right
            r2 = r2 & 0xff # wrap around
            self.assertEqualHex(r, r2)

            # test negative
            if 128 <= r <= 255:
                self.assertEqual(self.cpu.N, 1)
            else:
                self.assertEqual(self.cpu.N, 0)

            # test zero
            if r == 0:
                self.assertEqual(self.cpu.Z, 1)
            else:
                self.assertEqual(self.cpu.Z, 0)

            # test overflow
            self.assertEqual(self.cpu.V, 0)

            # test carry
            source_bit0 = get_bit(i, bit=0)
            self.assertEqual(self.cpu.C, source_bit0)

    def test_LSLA_inherent(self):
        for i in range(260):
            self.cpu.accu_a.set(i)
            self.cpu.set_cc(0x00) # Clear all CC flags
            self.cpu_test_run(start=0x1000, end=None, mem=[
                0x48, # LSLA/ASLA Inherent
            ])
            r = self.cpu.accu_a.value
#             print "%02x %s > LSLA > %02x %s -> %s" % (
#                 i, '{0:08b}'.format(i),
#                 r, '{0:08b}'.format(r),
#                 self.cpu.get_cc_info()
#             )

            # test LSL result
            r2 = i << 1 # shift left
            r2 = r2 & 0xff # wrap around
            self.assertEqualHex(r, r2)

            # test negative
            if 128 <= r <= 255:
                self.assertEqual(self.cpu.N, 1)
            else:
                self.assertEqual(self.cpu.N, 0)

            # test zero
            if r == 0:
                self.assertEqual(self.cpu.Z, 1)
            else:
                self.assertEqual(self.cpu.Z, 0)

            # test overflow
            if 64 <= i <= 191:
                self.assertEqual(self.cpu.V, 1)
            else:
                self.assertEqual(self.cpu.V, 0)

            # test carry
            if 128 <= i <= 255:
                self.assertEqual(self.cpu.C, 1)
            else:
                self.assertEqual(self.cpu.C, 0)

    def test_ASR_inherent(self):
        """
        Shifts all bits of the operand one place to the right.
        Bit seven is held constant. Bit zero is shifted into the C (carry) bit.
        """
        for src in range(0x100):
            self.cpu.accu_b.set(src)
            self.cpu.set_cc(0x00) # Set all CC flags
            self.cpu_test_run(start=0x1000, end=None, mem=[
                0x57, # ASRB/LSRB Inherent
            ])
            dst = self.cpu.accu_b.value

            src_bit_str = '{0:08b}'.format(src)
            dst_bit_str = '{0:08b}'.format(dst)

#             print "%02x %s > ASRB > %02x %s -> %s" % (
#                 src, src_bit_str,
#                 dst, dst_bit_str,
#                 self.cpu.get_cc_info()
#             )

            # Bit seven is held constant.
            if src_bit_str[0] == "1":
                excpeted_bits = "1%s" % src_bit_str[:-1]
            else:
                excpeted_bits = "0%s" % src_bit_str[:-1]

            # test ASRB/LSRB result
            self.assertEqual(dst_bit_str, excpeted_bits)

            # test negative
            if 128 <= dst <= 255:
                self.assertEqual(self.cpu.N, 1)
            else:
                self.assertEqual(self.cpu.N, 0)

            # test zero
            if dst == 0:
                self.assertEqual(self.cpu.Z, 1)
            else:
                self.assertEqual(self.cpu.Z, 0)

            # test overflow (is uneffected!)
            self.assertEqual(self.cpu.V, 0)

            # test carry
            source_bit0 = is_bit_set(src, bit=0)
            if source_bit0:
                self.assertEqual(self.cpu.C, 1)
            else:
                self.assertEqual(self.cpu.C, 0)


class Test6809_Rotate(BaseCPUTestCase):
    """
    unittests for:
        * ROL (Rotate Left) alias
        * ROR (Rotate Right) alias
    """

    def assertROL(self, src, dst, source_carry):
        src_bit_str = '{0:08b}'.format(src)
        dst_bit_str = '{0:08b}'.format(dst)
        print("%02x %s > ROLA > %02x %s -> %s" % (
            src, src_bit_str,
            dst, dst_bit_str,
            self.cpu.get_cc_info()
        ))

        # Carry was cleared and moved into bit 0
        excpeted_bits = "%s%s" % (src_bit_str[1:], source_carry)
        self.assertEqual(dst_bit_str, excpeted_bits)

        # test negative
        if dst >= 0x80:
            self.assertEqual(self.cpu.N, 1)
        else:
            self.assertEqual(self.cpu.N, 0)

        # test zero
        if dst == 0:
            self.assertEqual(self.cpu.Z, 1)
        else:
            self.assertEqual(self.cpu.Z, 0)

        # test overflow
        source_bit6 = is_bit_set(src, bit=6)
        source_bit7 = is_bit_set(src, bit=7)
        if source_bit6 == source_bit7: # V = bit 6 XOR bit 7
            self.assertEqual(self.cpu.V, 0)
        else:
            self.assertEqual(self.cpu.V, 1)

        # test carry
        if 0x80 <= src <= 0xff: # if bit 7 was set
            self.assertEqual(self.cpu.C, 1)
        else:
            self.assertEqual(self.cpu.C, 0)

    def test_ROLA_with_clear_carry(self):
        for a in range(0x100):
            self.cpu.set_cc(0x00) # clear all CC flags
            self.cpu.accu_a.set(a)
            a = self.cpu.accu_a.value
            self.cpu_test_run(start=0x0000, end=None, mem=[
                0x49, # ROLA
            ])
            r = self.cpu.accu_a.value
            self.assertROL(a, r, source_carry=0)

            # test half carry is uneffected!
            self.assertEqual(self.cpu.H, 0)

    def test_ROLA_with_set_carry(self):
        for a in range(0x100):
            self.cpu.set_cc(0xff) # set all CC flags
            self.cpu.accu_a.set(a)
            a = self.cpu.accu_a.value
            self.cpu_test_run(start=0x0000, end=None, mem=[
                0x49, # ROLA
            ])
            r = self.cpu.accu_a.value
            self.assertROL(a, r, source_carry=1)

            # test half carry is uneffected!
            self.assertEqual(self.cpu.H, 1)

    def test_ROL_memory_with_clear_carry(self):
        for a in range(0x100):
            self.cpu.set_cc(0x00) # clear all CC flags
            self.cpu.memory.write_byte(0x0050, a)
            self.cpu_test_run(start=0x0000, end=None, mem=[
                0x09, 0x50, # ROL #$50
            ])
            r = self.cpu.memory.read_byte(0x0050)
            self.assertROL(a, r, source_carry=0)

            # test half carry is uneffected!
            self.assertEqual(self.cpu.H, 0)

    def test_ROL_memory_with_set_carry(self):
        for a in range(0x100):
            self.cpu.set_cc(0xff) # set all CC flags
            self.cpu.memory.write_byte(0x0050, a)
            self.cpu_test_run(start=0x0000, end=None, mem=[
                0x09, 0x50, # ROL #$50
            ])
            r = self.cpu.memory.read_byte(0x0050)
            self.assertROL(a, r, source_carry=1)

            # test half carry is uneffected!
            self.assertEqual(self.cpu.H, 1)

    def assertROR(self, src, dst, source_carry):
            src_bit_str = '{0:08b}'.format(src)
            dst_bit_str = '{0:08b}'.format(dst)
#            print "%02x %s > RORA > %02x %s -> %s" % (
#                src, src_bit_str,
#                dst, dst_bit_str,
#                self.cpu.get_cc_info()
#            )

            # Carry was cleared and moved into bit 0
            excpeted_bits = "%s%s" % (source_carry, src_bit_str[:-1])
            self.assertEqual(dst_bit_str, excpeted_bits)

            # test negative
            if dst >= 0x80:
                self.assertEqual(self.cpu.N, 1)
            else:
                self.assertEqual(self.cpu.N, 0)

            # test zero
            if dst == 0:
                self.assertEqual(self.cpu.Z, 1)
            else:
                self.assertEqual(self.cpu.Z, 0)

            # test carry
            source_bit0 = is_bit_set(src, bit=0)
            if source_bit0: # if bit 0 was set
                self.assertEqual(self.cpu.C, 1)
            else:
                self.assertEqual(self.cpu.C, 0)

    def test_RORA_with_clear_carry(self):
        for a in range(0x100):
            self.cpu.set_cc(0x00) # clear all CC flags
            self.cpu.accu_a.set(a)
            a = self.cpu.accu_a.value
            self.cpu_test_run(start=0x0000, end=None, mem=[
                0x46, # RORA
            ])
            r = self.cpu.accu_a.value
            self.assertROR(a, r, source_carry=0)

            # test half carry and overflow, they are uneffected!
            self.assertEqual(self.cpu.H, 0)
            self.assertEqual(self.cpu.V, 0)

    def test_RORA_with_set_carry(self):
        for a in range(0x100):
            self.cpu.set_cc(0xff) # set all CC flags
            self.cpu.accu_a.set(a)
            a = self.cpu.accu_a.value
            self.cpu_test_run(start=0x0000, end=None, mem=[
                0x46, # RORA
            ])
            r = self.cpu.accu_a.value
            self.assertROR(a, r, source_carry=1)

            # test half carry and overflow, they are uneffected!
            self.assertEqual(self.cpu.H, 1)
            self.assertEqual(self.cpu.V, 1)

    def test_ROR_memory_with_clear_carry(self):
        for a in range(0x100):
            self.cpu.set_cc(0x00) # clear all CC flags
            self.cpu.memory.write_byte(0x0050, a)
            self.cpu_test_run(start=0x0000, end=None, mem=[
                0x06, 0x50,# ROR #$50
            ])
            r = self.cpu.memory.read_byte(0x0050)
            self.assertROR(a, r, source_carry=0)

            # test half carry and overflow, they are uneffected!
            self.assertEqual(self.cpu.H, 0)
            self.assertEqual(self.cpu.V, 0)

    def test_ROR_memory_with_set_carry(self):
        for a in range(0x100):
            self.cpu.set_cc(0xff) # set all CC flags
            self.cpu.memory.write_byte(0x0050, a)
            self.cpu_test_run(start=0x0000, end=None, mem=[
                0x06, 0x50,# ROR #$50
            ])
            r = self.cpu.memory.read_byte(0x0050)
            self.assertROR(a, r, source_carry=1)

            # test half carry and overflow, they are uneffected!
            self.assertEqual(self.cpu.H, 1)
            self.assertEqual(self.cpu.V, 1)


if __name__ == '__main__':
    unittest.main(
        argv=(
            sys.argv[0],
#            "Test6809_LogicalShift.test_ASR_inherent",
#            "Test6809_Rotate",
        ),
#         verbosity=1,
        verbosity=2,
#         failfast=True,
    )
