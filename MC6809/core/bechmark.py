#!/usr/bin/env python

"""
    MC6809 - 6809 CPU emulator in Python
    =======================================

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014-2015 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import logging
import string
import time

from MC6809.tests.test_6809_program import Test6809_Program
from MC6809.utils.humanize import locale_format_number


log = logging.getLogger("MC6809")


class Test6809_Program2(Test6809_Program):
    def runTest(self):
        pass

    def bench(self, loops, multiply, func, msg):
        print(f"\n{msg} benchmark")

        self.setUp()
        self.cpu.cycles = 0

        txt = string.printable
        txt = bytes(txt, encoding="UTF-8")
        txt = txt * multiply

        print(f"\nStart {loops:d} {msg} loops with {len(txt):d} Bytes test string...")

        start_time = time.time()
        for __ in range(loops):
            self._crc32(txt)
        duration = time.time() - start_time

        print(f"{msg} benchmark runs {locale_format_number(self.cpu.cycles)} CPU cycles in {duration:.2f} sec")

        return duration, self.cpu.cycles

    def crc32_benchmark(self, loops, multiply):
        return self.bench(loops, multiply, self._crc32, "CRC32")

    def crc16_benchmark(self, loops, multiply):
        return self.bench(loops, multiply, self._crc16, "CRC16")


def run_benchmark(loops, multiply):
    total_duration = 0
    total_cycles = 0
    bench_class = Test6809_Program2()

    # --------------------------------------------------------------------------

    duration, cycles = bench_class.crc16_benchmark(loops, multiply)
    total_duration += duration
    total_cycles += cycles

    # --------------------------------------------------------------------------

    duration, cycles = bench_class.crc32_benchmark(loops, multiply)
    total_duration += duration
    total_cycles += cycles

    # --------------------------------------------------------------------------
    print("-" * 79)
    print(
        f"\nTotal of {loops:d} benchmak loops run in {total_duration:.2f} sec"
        f" {locale_format_number(total_cycles)} CPU cycles."
    )
    print(f"\tavg.: {locale_format_number(total_cycles / total_duration)} CPU cycles/sec")
