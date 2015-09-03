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

import inspect

import threading
import time
import sys
import warnings

if sys.version_info[0] == 3:
    # Python 3
    import queue
    import _thread
else:
    # Python 2
    import Queue as queue
    import thread as _thread
    range = xrange


class CPUStatusThread(threading.Thread):
    """
    Send cycles/sec information via cpu_status_queue to the GUi main thread.
    Just ignore if the cpu_status_queue is full.
    """
    def __init__(self, cpu, cpu_status_queue):
        super(CPUStatusThread, self).__init__(name="CPU-Status-Thread")
        self.cpu = cpu
        self.cpu_status_queue = cpu_status_queue

        self.last_cpu_cycles = None
        self.last_cpu_cycle_update = time.time()

    def _run(self):
        while self.cpu.running:
            try:
                self.cpu_status_queue.put(self.cpu.cycles, block=False)
            except queue.Full:
#                 log.critical("Can't put CPU status: Queue is full.")
                pass
            time.sleep(0.5)

    def run(self):
        try:
            self._run()
        except:
            self.cpu.running = False
            _thread.interrupt_main()
            raise


class CPUThreadedStatusMixin(object):
    def __init__(self, *args, **kwargs):
        cpu_status_queue = kwargs.get("cpu_status_queue", None)
        if cpu_status_queue is not None:
            status_thread = CPUStatusThread(self, cpu_status_queue)
            status_thread.deamon = True
            status_thread.start()


class CPUTypeAssertMixin(object):
    """
    assert that all attributes of the CPU class will remain as the same.

    We use no property, because it's slower. But without it, it's hard to find
    if somewhere not .set() or .incement() is used.

    With this helper a error will raise, if the type of a attribute will be
    changed, e.g.:
        cpu.index_x = ValueStorage16Bit(...)
        cpu.index_x = 0x1234 # will raised a error
    """
    __ATTR_DICT = {}
    def __init__(self, *args, **kwargs):
        super(CPUTypeAssertMixin, self).__init__(*args, **kwargs)
        self.__set_attr_dict()
        warnings.warn(
            "CPU TypeAssert used! (Should be only activated for debugging!)"
        )

    def __set_attr_dict(self):
        for name, obj in inspect.getmembers(self, lambda x:not(inspect.isroutine(x))):
            if name.startswith("_") or name == "cfg":
                continue
            self.__ATTR_DICT[name] = type(obj)

    def __setattr__(self, attr, value):
        if attr in self.__ATTR_DICT:
            obj = self.__ATTR_DICT[attr]
            assert isinstance(value, obj), \
                "Attribute %r is no more type %s (Is now: %s)!" % (
                    attr, obj, type(obj)
                )
        return object.__setattr__(self, attr, value)


def calc_new_count(min_value, value, max_value, trigger, target):
    """
    change 'value' between 'min_value' and 'max_value'
    so that 'trigger' will be match 'target'
    
    >>> calc_new_count(min_value=0, value=100, max_value=200, trigger=30, target=30)
    100

    >>> calc_new_count(min_value=0, value=100, max_value=200, trigger=50, target=5)
    55
    >>> calc_new_count(min_value=60, value=100, max_value=200, trigger=50, target=5)
    60

    >>> calc_new_count(min_value=0, value=100, max_value=200, trigger=20, target=40)
    150
    >>> calc_new_count(min_value=0, value=100, max_value=125, trigger=20, target=40)
    125
    """
    try:
        new_value = float(value) / float(trigger) * target
    except ZeroDivisionError:
        return value * 2

    if new_value > max_value:
        return max_value

    new_value = int((value + new_value) / 2)
    if new_value < min_value:
        return min_value
    return new_value