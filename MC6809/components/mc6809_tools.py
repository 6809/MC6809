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


class CPUThreadedStatus(object):
    def __init__(self, *args, **kwargs):
        cpu_status_queue = kwargs.get("cpu_status_queue", None)
        if cpu_status_queue is not None:
            status_thread = CPUStatusThread(self, cpu_status_queue)
            status_thread.deamon = True
            status_thread.start()


class CPUTypeAssert(object):
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
        super(CPUTypeAssert, self).__init__(*args, **kwargs)
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