#!/usr/bin/env python

"""
    6809 unittests
    ~~~~~~~~~~~~~~

    :created: 2013 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2013-2014 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

import unittest
import sys

PY2 = sys.version_info[0] == 2
if PY2:
    range = xrange

from MC6809.tests.test_base import BaseCPUTestCase
from MC6809.utils.byte_word_values import signed8


class CCTestCase(BaseCPUTestCase):
    def test_set_get(self):
        for i in range(256):
            self.cpu.set_cc(i)
            status_byte = self.cpu.get_cc_value()
            self.assertEqual(status_byte, i)

    def test_HNZVC_8(self):
        for i in range(280):
            self.cpu.set_cc(0x00)
            r = i + 1 # e.g. ADDA 1 loop
            self.cpu.update_HNZVC_8(a=i, b=1, r=r)
            # print r, self.cpu.get_cc_info()

            # test half carry
            if r % 16 == 0:
                self.assertEqual(self.cpu.H, 1)
            else:
                self.assertEqual(self.cpu.H, 0)

            # test negative
            if 128 <= r <= 255:
                self.assertEqual(self.cpu.N, 1)
            else:
                self.assertEqual(self.cpu.N, 0)

            # test zero
            if signed8(r) == 0:
                self.assertEqual(self.cpu.Z, 1)
            else:
                self.assertEqual(self.cpu.Z, 0)

            # test overflow
            if r == 128 or r > 256:
                self.assertEqual(self.cpu.V, 1)
            else:
                self.assertEqual(self.cpu.V, 0)

            # test carry
            if r > 255:
                self.assertEqual(self.cpu.C, 1)
            else:
                self.assertEqual(self.cpu.C, 0)

            # Test that CC registers doesn't reset automaticly
            self.cpu.set_cc(0xff)
            r = i + 1 # e.g. ADDA 1 loop
            self.cpu.update_HNZVC_8(a=i, b=1, r=r)
            # print "+++", r, self.cpu.get_cc_info()
            self.assertEqualHex(self.cpu.get_cc_value(), 0xff)


    def test_update_NZ_8_A(self):
        self.cpu.update_NZ_8(r=0x12)
        self.assertEqual(self.cpu.N, 0)
        self.assertEqual(self.cpu.Z, 0)

    def test_update_NZ_8_B(self):
        self.cpu.update_NZ_8(r=0x0)
        self.assertEqual(self.cpu.N, 0)
        self.assertEqual(self.cpu.Z, 1)

    def test_update_NZ_8_C(self):
        self.cpu.update_NZ_8(r=0x80)
        self.assertEqual(self.cpu.N, 1)
        self.assertEqual(self.cpu.Z, 0)

    def test_update_NZ0_16_A(self):
        self.cpu.update_NZ0_16(r=0x7fff) # 0x7fff == 32767
        self.assertEqual(self.cpu.N, 0)
        self.assertEqual(self.cpu.Z, 0)
        self.assertEqual(self.cpu.V, 0)

    def test_update_NZ0_16_B(self):
        self.cpu.update_NZ0_16(r=0x00)
        self.assertEqual(self.cpu.N, 0)
        self.assertEqual(self.cpu.Z, 1)
        self.assertEqual(self.cpu.V, 0)

    def test_update_NZ0_16_C(self):
        self.cpu.update_NZ0_16(r=0x8000) # signed 0x8000 == -32768
        self.assertEqual(self.cpu.N, 1)
        self.assertEqual(self.cpu.Z, 0)
        self.assertEqual(self.cpu.V, 0)

    def test_update_NZ0_8_A(self):
        self.cpu.update_NZ0_8(0x7f)
        self.assertEqual(self.cpu.N, 0)
        self.assertEqual(self.cpu.Z, 0)
        self.assertEqual(self.cpu.V, 0)

    def test_update_NZ0_8_B(self):
        self.cpu.update_NZ0_8(0x100)
        self.assertEqual(self.cpu.N, 0)
        self.assertEqual(self.cpu.Z, 1)
        self.assertEqual(self.cpu.V, 0)

    def test_update_NZV_8_B(self):
        self.cpu.update_NZ0_8(0x100)
        self.assertEqual(self.cpu.N, 0)
        self.assertEqual(self.cpu.Z, 1)
        self.assertEqual(self.cpu.V, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)


