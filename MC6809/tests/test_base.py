#!/usr/bin/env python

"""
    6809 unittests
    ~~~~~~~~~~~~~~

    :created: 2013 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2013-2014 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import hashlib
import logging
import unittest

from MC6809.components.cpu6809 import CPU
from MC6809.components.memory import Memory
from MC6809.tests.test_config import TestCfg
from MC6809.utils.byte_word_values import bin2hexline


log = logging.getLogger("MC6809")


class BaseTestCase(unittest.TestCase):
    """
    Only some special assertments.
    """
    maxDiff = 3000

    def assertHexList(self, first, second, msg=None):
        first = [f"${value:x}" for value in first]
        second = [f"${value:x}" for value in second]
        self.assertEqual(first, second, msg)

    def assertEqualHex(self, hex1, hex2, msg=None):
        first = f"${hex1:x}"
        second = f"${hex2:x}"
        if msg is None:
            msg = f"{first} != {second}"
        self.assertEqual(first, second, msg)

    def assertIsByteRange(self, value):
        self.assertTrue(0x0 <= value, f"Value (dez: {value:d} - hex: {value:x}) is negative!")
        self.assertTrue(0xff >= value, f"Value (dez: {value:d} - hex: {value:x}) is greater than 0xff!")

    def assertIsWordRange(self, value):
        self.assertTrue(0x0 <= value, f"Value (dez: {value:d} - hex: {value:x}) is negative!")
        self.assertTrue(0xffff >= value, f"Value (dez: {value:d} - hex: {value:x}) is greater than 0xffff!")

    def assertEqualHexByte(self, hex1, hex2, msg=None):
        self.assertIsByteRange(hex1)
        self.assertIsByteRange(hex2)
        first = f"${hex1:02x}"
        second = f"${hex2:02x}"
        if msg is None:
            msg = f"{first} != {second}"
        self.assertEqual(first, second, msg)

    def assertEqualHexWord(self, hex1, hex2, msg=None):
        self.assertIsWordRange(hex1)
        self.assertIsWordRange(hex2)
        first = f"${hex1:04x}"
        second = f"${hex2:04x}"
        if msg is None:
            msg = f"{first} != {second}"
        self.assertEqual(first, second, msg)

    def assertBinEqual(self, bin1, bin2, msg=None, width=16):
        first = bin2hexline(bin1, width=width)
        second = bin2hexline(bin2, width=width)
        self.assertSequenceEqual(first, second, msg)

        # first = "\n".join(bin2hexline(bin1, width=width))
        # second = "\n".join(bin2hexline(bin2, width=width))
        # self.assertMultiLineEqual(first, second, msg)


class BaseCPUTestCase(BaseTestCase):
    UNITTEST_CFG_DICT = {
        "verbosity": None,
        "display_cycle": False,
        "trace": None,
        "bus_socket_host": None,
        "bus_socket_port": None,
        "ram": None,
        "rom": None,
        "max_ops": None,
        "use_bus": False,
    }

    def setUp(self):
        cfg = TestCfg(self.UNITTEST_CFG_DICT)
        memory = Memory(cfg)
        self.cpu = CPU(memory, cfg)

    def cpu_test_run(self, start, end, mem):
        for cell in mem:
            self.assertLess(-1, cell, f"${cell:x} < 0")
            self.assertGreater(0x100, cell, f"${cell:x} > 0xff")
        log.debug("memory load at $%x: %s", start,
                  ", ".join(f"${i:x}" for i in mem)
                  )
        self.cpu.memory.load(start, mem)
        if end is None:
            end = start + len(mem)
        self.cpu.test_run(start, end)
    cpu_test_run.__test__ = False  # Exclude from nose

    def cpu_test_run2(self, start, count, mem):
        for cell in mem:
            self.assertLess(-1, cell, f"${cell:x} < 0")
            self.assertGreater(0x100, cell, f"${cell:x} > 0xff")
        self.cpu.memory.load(start, mem)
        self.cpu.test_run2(start, count)
    cpu_test_run2.__test__ = False  # Exclude from nose

    def assertMemory(self, start, mem):
        for index, should_byte in enumerate(mem):
            address = start + index
            is_byte = self.cpu.memory.read_byte(address)

            msg = f"${is_byte:02x} is not ${should_byte:02x} at address ${address:04x} (index: {index:d})"
            self.assertEqual(is_byte, should_byte, msg)


class BaseStackTestCase(BaseCPUTestCase):
    INITIAL_SYSTEM_STACK_ADDR = 0x1000
    INITIAL_USER_STACK_ADDR = 0x2000

    def setUp(self):
        super().setUp()
        self.cpu.system_stack_pointer.set(self.INITIAL_SYSTEM_STACK_ADDR)
        self.cpu.user_stack_pointer.set(self.INITIAL_USER_STACK_ADDR)


# class TestCPU:
#     def __init__(self):
#         self.accu_a = ValueStorage8Bit("A", 0)  # A - 8 bit accumulator
#         self.accu_b = ValueStorage8Bit("B", 0)  # B - 8 bit accumulator
#         # 8 bit condition code register bits: E F H I N Z V C
#         self.cc = ConditionCodeRegister()


def print_cpu_state_data(state):
    print(f"cpu state data {state.__class__.__name__!r} (ID:{id(state):d}):")
    for k, v in sorted(state.items()):
        if k == "RAM":
            # v = ",".join(["$%x" % i for i in v])
            print("\tSHA from RAM:", hashlib.sha224(repr(v)).hexdigest())
            continue
        if isinstance(v, int):
            v = f"${v:x}"
        print(f"\t{k!r}: {v}")
