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

    :copyleft: 2013-2014 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.

    Based on:
        * ApplyPy by James Tauber (MIT license)
        * XRoar emulator by Ciaran Anscomb (GPL license)
    more info, see README
"""

from __future__ import absolute_import, division, print_function

try:
    # Python 3
    import queue
    import _thread
except ImportError:
    # Python 2
    import Queue as queue
    import thread as _thread
    range = xrange

import inspect
import logging
import sys
import threading
import time
import warnings


from MC6809.core.cpu_control_server import start_http_control_server
from MC6809.components.cpu_utils.MC6809_registers import (
    ValueStorage8Bit, ConcatenatedAccumulator,
    ValueStorage16Bit, ConditionCodeRegister, UndefinedRegister
)
from MC6809.components.cpu_utils.instruction_caller import OpCollection
from MC6809.utils.bits import is_bit_set, get_bit
from MC6809.utils.byte_word_values import signed8, signed16, signed5
from MC6809.components.MC6809data.MC6809_op_data import (
    REG_A, REG_B, REG_CC, REG_D, REG_DP, REG_PC,
    REG_S, REG_U, REG_X, REG_Y
)


log = logging.getLogger("MC6809")


# HTML_TRACE = True
HTML_TRACE = False


def opcode(*opcodes):
    """A decorator for opcodes"""
    def decorator(func):
        setattr(func, "_is_opcode", True)
        setattr(func, "_opcodes", opcodes)
        return func
    return decorator




undefined_reg = UndefinedRegister()


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


class CPU(object):

    SWI3_VECTOR = 0xfff2
    SWI2_VECTOR = 0xfff4
    FIRQ_VECTOR = 0xfff6
    IRQ_VECTOR = 0xfff8
    SWI_VECTOR = 0xfffa
    NMI_VECTOR = 0xfffc
    RESET_VECTOR = 0xfffe

    STARTUP_BURST_COUNT = 100

    def __init__(self, memory, cfg, cpu_status_queue=None):
        self.memory = memory
        self.memory.cpu = self # FIXME
        self.cfg = cfg

        self.running = True
        self.cycles = 0
        self.last_op_address = 0 # Store the current run opcode memory address
        self.outer_burst_op_count = self.STARTUP_BURST_COUNT

        if cpu_status_queue is not None:
            status_thread = CPUStatusThread(self, cpu_status_queue)
            status_thread.deamon = True
            status_thread.start()

        start_http_control_server(self, cfg)

        self.index_x = ValueStorage16Bit(REG_X, 0) # X - 16 bit index register
        self.index_y = ValueStorage16Bit(REG_Y, 0) # Y - 16 bit index register

        self.user_stack_pointer = ValueStorage16Bit(REG_U, 0) # U - 16 bit user-stack pointer
        self.user_stack_pointer.counter = 0

        # S - 16 bit system-stack pointer:
        # Position will be set by ROM code after detection of total installed RAM
        self.system_stack_pointer = ValueStorage16Bit(REG_S, 0)

        # PC - 16 bit program counter register
        self.program_counter = ValueStorage16Bit(REG_PC, 0)

        self.accu_a = ValueStorage8Bit(REG_A, 0) # A - 8 bit accumulator
        self.accu_b = ValueStorage8Bit(REG_B, 0) # B - 8 bit accumulator

        # D - 16 bit concatenated reg. (A + B)
        self.accu_d = ConcatenatedAccumulator(REG_D, self.accu_a, self.accu_b)

        # DP - 8 bit direct page register
        self.direct_page = ValueStorage8Bit(REG_DP, 0)

        # 8 bit condition code register bits: E F H I N Z V C
        self.cc = ConditionCodeRegister()

        self.register_str2object = {
            REG_X: self.index_x,
            REG_Y: self.index_y,

            REG_U: self.user_stack_pointer,
            REG_S: self.system_stack_pointer,

            REG_PC: self.program_counter,

            REG_A: self.accu_a,
            REG_B: self.accu_b,
            REG_D: self.accu_d,

            REG_DP: self.direct_page,
            REG_CC: self.cc,

            undefined_reg.name: undefined_reg, # for TFR, EXG
        }

        self.registers = [
            self.accu_d,
            self.index_x,
            self.index_y,
            self.user_stack_pointer,
            self.system_stack_pointer,
            self.program_counter,
            undefined_reg,
            undefined_reg,
            self.accu_a,
            self.accu_b,
            self.cc,
            self.direct_page,
            undefined_reg,
            undefined_reg,
            undefined_reg,
            undefined_reg,
        ]

#         log.debug("Add opcode functions:")
        self.opcode_dict = OpCollection(self).get_opcode_dict()

#         log.debug("illegal ops: %s" % ",".join(["$%x" % c for c in ILLEGAL_OPS]))
        # add illegal instruction
#         for opcode in ILLEGAL_OPS:
#             self.opcode_dict[opcode] = IllegalInstruction(self, opcode)

    def get_state(self):
        """
        used in unittests
        """
        return {
            REG_X: self.index_x.value,
            REG_Y: self.index_y.value,

            REG_U: self.user_stack_pointer.value,
            REG_S: self.system_stack_pointer.value,

            REG_PC: self.program_counter.value,

            REG_A: self.accu_a.value,
            REG_B: self.accu_b.value,

            REG_DP: self.direct_page.value,
            REG_CC: self.cc.value,

            "cycles": self.cycles,
            "RAM": tuple(self.memory._mem) # copy of array.array() values,
        }

    def set_state(self, state):
        """
        used in unittests
        """
        self.index_x.value = state[REG_X] & self.index_x.BASE
        self.index_y.value = state[REG_Y] & self.index_y.BASE

        self.user_stack_pointer.value = state[REG_U] & self.user_stack_pointer.BASE
        self.system_stack_pointer.value = state[REG_S] & self.system_stack_pointer.BASE

        self.program_counter.value = state[REG_PC] & self.program_counter.BASE

        self.accu_a.value = state[REG_A] & self.accu_a.BASE
        self.accu_b.value = state[REG_B] & self.accu_b.BASE

        self.direct_page.value = state[REG_DP] & self.direct_page.BASE
        self.cc.value = state[REG_CC]

        self.cycles = state["cycles"]
        self.memory.load(address=0x0000, data=state["RAM"])

    ####

    def reset(self):
        log.info("%04x| CPU reset:", self.program_counter.value)

        self.last_op_address = 0

        if self.cfg.__class__.__name__ == "SBC09Cfg":
            # first op is:
            # E400: 1AFF  reset  orcc #$FF  ;Disable interrupts.
#             log.debug("\tset CC register to 0xff")
#             self.cc.set(0xff)
            log.info("\tset CC register to 0x00")
            self.cc.value = 0
        else:
#             log.info("\tset cc.F=1: FIRQ interrupt masked")
#             self.cc.F = 1
#
#             log.info("\tset cc.I=1: IRQ interrupt masked")
#             self.cc.I = 1

            log.info("\tset E - 0x80 - bit 7 - Entire register state stacked")
            self.cc.E = 1

#         log.debug("\tset PC to $%x" % self.cfg.RESET_VECTOR)
#         self.program_counter = self.cfg.RESET_VECTOR

        log.info("\tread reset vector from $%04x", self.RESET_VECTOR)
        ea = self.memory.read_word(self.RESET_VECTOR)
        log.info("\tset PC to $%04x" % ea)
        if ea == 0x0000:
            log.critical("Reset vector is $%04x ??? ROM loading in the right place?!?", ea)
        self.program_counter.value = ea & 0xffff

    ####

    def get_and_call_next_op(self):
        opcode = self.read_pc_byte()
        cycles, instr_func = self.opcode_dict[opcode]
        instr_func(opcode)
        self.cycles += cycles

    def quit(self):
        log.critical("CPU quit() called.")
        self.running = False

    def call_instruction_func(self, opcode):
        cycles, instr_func = self.opcode_dict[opcode]
        instr_func(opcode)
        self.cycles += cycles


    ####

    # TODO: Move to __init__
    quickest_sync_callback_cycles = None
    sync_callbacks_cyles = {}
    sync_callbacks = []
    def add_sync_callback(self, callback_cycles, callback):
        """ Add a CPU cycle triggered callback """
        self.sync_callbacks_cyles[callback] = 0
        self.sync_callbacks.append([callback_cycles, callback])
        if self.quickest_sync_callback_cycles is None or \
                        self.quickest_sync_callback_cycles > callback_cycles:
            self.quickest_sync_callback_cycles = callback_cycles

    def call_sync_callbacks(self):
        """ Call every sync callback with CPU cycles trigger """
        current_cycles = self.cycles
        for callback_cycles, callback in self.sync_callbacks:
            # get the CPU cycles count of the last call
            last_call_cycles = self.sync_callbacks_cyles[callback]

            if current_cycles - last_call_cycles > callback_cycles:
                # this callback should be called

                # Save the current cycles, to trigger the next call
                self.sync_callbacks_cyles[callback] = self.cycles

                # Call the callback function
                callback(current_cycles - last_call_cycles)

    # TODO: Move to __init__
    inner_burst_op_count = 100 # How many ops calls, before next sync call
    def burst_run(self):
        """ Run CPU as fast as Python can... """
        # https://wiki.python.org/moin/PythonSpeed/PerformanceTips#Avoiding_dots...
        get_and_call_next_op = self.get_and_call_next_op

        for __ in range(self.outer_burst_op_count):
            for __ in range(self.inner_burst_op_count):
                get_and_call_next_op()

            self.call_sync_callbacks()

    # TODO: Move to __init__
    max_delay = 0.01 # maximum time.sleep() value per burst run
    delay = 0 # the current time.sleep() value per burst run
    def delayed_burst_run(self, target_cycles_per_sec):
        """ Run CPU not faster than given speedlimit """
        old_cycles = self.cycles
        start_time = time.time()

        self.burst_run()

        is_duration = time.time() - start_time
        new_cycles = self.cycles - old_cycles
        try:
            is_cycles_per_sec = new_cycles / is_duration
        except ZeroDivisionError:
            pass
        else:
            should_burst_duration = is_cycles_per_sec / target_cycles_per_sec
            target_duration = should_burst_duration * is_duration
            delay = target_duration - is_duration
            if delay > 0:
                if delay > self.max_delay:
                    self.delay = self.max_delay
                else:
                    self.delay = delay
                time.sleep(self.delay)

        self.call_sync_callbacks()

    # TODO: Move to __init__
    min_burst_count = 10 # minimum outer op count per burst
    max_burst_count = 10000 # maximum outer op count per burst
    def calc_new_count(self, burst_count, current_value, target_value):
        """
        >>> calc_new_count(burst_count=100, current_value=30, target_value=30)
        100
        >>> calc_new_count(burst_count=100, current_value=40, target_value=20)
        75
        >>> calc_new_count(burst_count=100, current_value=20, target_value=40)
        150
        """
        # log.critical(
        #     "%i op count current: %.4f target: %.4f",
        #     self.outer_burst_op_count, current_value, target_value
        # )
        try:
            new_burst_count = float(burst_count) / float(current_value) * target_value
            new_burst_count += 1 # At least we need one loop ;)
        except ZeroDivisionError:
            return burst_count * 2

        if new_burst_count > self.max_burst_count:
            return self.max_burst_count

        burst_count = (burst_count + new_burst_count) / 2
        if burst_count < self.min_burst_count:
            return self.min_burst_count
        else:
            return int(burst_count)

    def run(self, max_run_time=0.1, target_cycles_per_sec=None):
        now = time.time

        start_time = now()

        if target_cycles_per_sec is not None:
            # Run CPU not faster than given speedlimit
            self.delayed_burst_run(target_cycles_per_sec)
        else:
            # Run CPU as fast as Python can...
            self.delay = 0
            self.burst_run()

        # Calculate the outer_burst_count new, to hit max_run_time
        self.outer_burst_op_count = self.calc_new_count(self.outer_burst_op_count,
            current_value=now() - start_time - self.delay,
            target_value=max_run_time,
        )

    def test_run(self, start, end, max_ops=1000000):
#        log.warning("CPU test_run(): from $%x to $%x" % (start, end))
        self.program_counter.value = start & 0xffff
#        log.debug("-"*79)

        # https://wiki.python.org/moin/PythonSpeed/PerformanceTips#Avoiding_dots...
        get_and_call_next_op = self.get_and_call_next_op
        program_counter = self.program_counter

        for __ in range(max_ops):
            if program_counter.value == end:
                return
            get_and_call_next_op()
        log.critical("Max ops %i arrived!", max_ops)
        raise RuntimeError("Max ops %i arrived!" % max_ops)


    def test_run2(self, start, count):
#        log.warning("CPU test_run2(): from $%x count: %i" % (start, count))
        self.program_counter.value = start & 0xffff
#        log.debug("-"*79)

        _old_burst_count = self.outer_burst_op_count
        self.outer_burst_op_count = count

        _old_sync_count = self.inner_burst_op_count
        self.inner_burst_op_count = 1

        self.burst_run()

        self.outer_burst_op_count = _old_burst_count
        self.inner_burst_op_count = _old_sync_count


    ####


    @property
    def get_info(self):
        return "cc=%02x a=%02x b=%02x dp=%02x x=%04x y=%04x u=%04x s=%04x" % (
            self.cc.value,
            self.accu_a.value, self.accu_b.value,
            self.direct_page.value,
            self.index_x.value, self.index_y.value,
            self.user_stack_pointer.value, self.system_stack_pointer.value
        )

    ####

    def push_byte(self, stack_pointer, byte):
        """ pushed a byte onto stack """
        # FIXME: self.system_stack_pointer -= 1
        stack_pointer.decrement(1)
        addr = stack_pointer.value

#        log.info(
#         log.error(
#            "%x|\tpush $%x to %s stack at $%x\t|%s",
#            self.last_op_address, byte, stack_pointer.name, addr,
#            self.cfg.mem_info.get_shortest(self.last_op_address)
#        )
        self.memory.write_byte(addr, byte)

    def pull_byte(self, stack_pointer):
        """ pulled a byte from stack """
        addr = stack_pointer.value
        byte = self.memory.read_byte(addr)
#        log.info(
#         log.error(
#            "%x|\tpull $%x from %s stack at $%x\t|%s",
#            self.last_op_address, byte, stack_pointer.name, addr,
#            self.cfg.mem_info.get_shortest(self.last_op_address)
#        )
        stack_pointer.value += 1
        stack_pointer.value &= stack_pointer.BASE

        return byte

    def push_word(self, stack_pointer, word):
        stack_pointer.value -= 2
        stack_pointer.value &= stack_pointer.BASE

        addr = stack_pointer.value
#        log.info(
#         log.error(
#            "%x|\tpush word $%x to %s stack at $%x\t|%s",
#            self.last_op_address, word, stack_pointer.name, addr,
#            self.cfg.mem_info.get_shortest(self.last_op_address)
#        )

        self.memory.write_word(addr, word)

#         hi, lo = divmod(word, 0x100)
#         self.push_byte(hi)
#         self.push_byte(lo)

    def pull_word(self, stack_pointer):
        addr = stack_pointer.value
        word = self.memory.read_word(addr)
#        log.info(
#         log.error(
#            "%x|\tpull word $%x from %s stack at $%x\t|%s",
#            self.last_op_address, word, stack_pointer.name, addr,
#            self.cfg.mem_info.get_shortest(self.last_op_address)
#        )
        stack_pointer.value += 2
        stack_pointer.value &= stack_pointer.BASE
        return word

    ####

    def read_pc_byte(self):
        programm_counter = self.program_counter
        op_addr = programm_counter.value
        programm_counter.value = (op_addr + 1) & 0xffff
        self.cycles += 1
        return self.memory._mem[op_addr]

    def read_pc_word(self):
        programm_counter = self.program_counter
        op_addr = programm_counter.value
        programm_counter.value = (op_addr + 2) & 0xffff
        self.cycles += 2
        return (self.memory._mem[op_addr] << 8) + self.memory._mem[op_addr+1]

    ####

    def get_m_immediate(self):
        return self.read_pc_byte()

    def get_m_immediate_word(self):
        return self.read_pc_word()

    def get_ea_direct(self):
        return self.direct_page.value << 8 | self.read_pc_byte()

    def get_ea_m_direct(self):
        ea = self.get_ea_direct()
        return ea, self.memory.read_byte(ea)

    def get_m_direct(self):
        return self.memory.read_byte(self.get_ea_direct())

    def get_m_direct_word(self):
        return self.memory.read_word(self.get_ea_direct())

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
        postbyte = self.read_pc_byte()
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
            ea = register_obj.decrement(1)
        elif addr_mode == 0x3:
#             log.debug("\t0011 0x3 | ,R-- | decrement by 2")
            ea = register_obj.decrement(2)
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
            offset = signed8(self.read_pc_byte())
        elif addr_mode == 0x9:
#             log.debug("\t1001 0x9 | n, R | 16 bit offset")
            offset = signed16(self.read_pc_word())
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
            value = self.read_pc_byte()
            value_signed = signed8(value)
            ea = self.program_counter.value + value_signed
#             log.debug("\tea = pc($%x) + $%x = $%x (dez.: %i + %i = %i)",
#                 self.program_counter, value_signed, ea,
#                 self.program_counter, value_signed, ea,
#             )
        elif addr_mode == 0xd:
#             log.debug("\t1101 0xd | n, PCR | 16 bit offset from program counter")
            value = self.read_pc_word()
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
            ea = self.read_pc_word()
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
        return self.memory.read_byte(self.get_ea_indexed())

    def get_ea_m_indexed(self):
        ea = self.get_ea_indexed()
        return ea, self.memory.read_byte(ea)

    def get_m_indexed_word(self):
        return self.memory.read_word(self.get_ea_indexed())

    def get_ea_extended(self):
        """
        extended indirect addressing mode takes a 2-byte value from post-bytes
        """
        return self.read_pc_word()

    def get_m_extended(self):
        return self.memory.read_byte(self.get_ea_extended())

    def get_ea_m_extended(self):
        ea = self.get_ea_extended()
        return ea, self.memory.read_byte(ea)

    def get_m_extended_word(self):
        return self.memory.read_word(self.get_ea_extended())

    def get_ea_relative(self):
        return signed8(self.read_pc_byte()) + self.program_counter.value

    def get_ea_relative_word(self):
        return self.read_pc_word() + self.program_counter.value

    #### Op methods:

    @opcode(
        0x10, # PAGE 2 instructions
        0x11, # PAGE 3 instructions
    )
    def instruction_PAGE(self, opcode):
        """ call op from page 2 or 3 """
        self.call_instruction_func(opcode * 256 + self.read_pc_byte())

    @opcode(# Add B accumulator to X (unsigned)
        0x3a, # ABX (inherent)
    )
    def instruction_ABX(self, opcode):
        """
        Add the 8-bit unsigned value in accumulator B into index register X.

        source code forms: ABX

        CC bits "HNZVC": -----
        """
        self.index_x.increment(self.accu_b.value)

    @opcode(# Add memory to accumulator with carry
        0x89, 0x99, 0xa9, 0xb9, # ADCA (immediate, direct, indexed, extended)
        0xc9, 0xd9, 0xe9, 0xf9, # ADCB (immediate, direct, indexed, extended)
    )
    def instruction_ADC(self, opcode, m, register):
        """
        Adds the contents of the C (carry) bit and the memory byte into an 8-bit
        accumulator.

        source code forms: ADCA P; ADCB P

        CC bits "HNZVC": aaaaa
        """
        a = register.value
        r = a + m + self.cc.C
        register.value = r & register.BASE
#        log.debug("$%x %02x ADC %s: %i + %i + %i = %i (=$%x)" % (
#            self.program_counter, opcode, register.name,
#            a, m, self.cc.C, r, r
#        ))
        self.cc.clear_HNZVC()
        self.cc.update_HNZVC_8(a, m, r)

    @opcode(# Add memory to D accumulator
        0xc3, 0xd3, 0xe3, 0xf3, # ADDD (immediate, direct, indexed, extended)
    )
    def instruction_ADD16(self, opcode, m, register):
        """
        Adds the 16-bit memory value into the 16-bit accumulator

        source code forms: ADDD P

        CC bits "HNZVC": -aaaa
        """
        assert register.WIDTH == 16
        old = register.value
        r = old + m
        register.value = r & register.BASE
#        log.debug("$%x %02x %02x ADD16 %s: $%02x + $%02x = $%02x" % (
#            self.program_counter, opcode, m,
#            register.name,
#            old, m, r
#        ))
        self.cc.clear_NZVC()
        self.cc.update_NZVC_16(old, m, r)

    @opcode(# Add memory to accumulator
        0x8b, 0x9b, 0xab, 0xbb, # ADDA (immediate, direct, indexed, extended)
        0xcb, 0xdb, 0xeb, 0xfb, # ADDB (immediate, direct, indexed, extended)
    )
    def instruction_ADD8(self, opcode, m, register):
        """
        Adds the memory byte into an 8-bit accumulator.

        source code forms: ADDA P; ADDB P

        CC bits "HNZVC": aaaaa
        """
        assert register.WIDTH == 8
        old = register.value
        r = old + m
        register.value = r & register.BASE
#         log.debug("$%x %02x %02x ADD8 %s: $%02x + $%02x = $%02x" % (
#             self.program_counter, opcode, m,
#             register.name,
#             old, m, r
#         ))
        self.cc.clear_HNZVC()
        self.cc.update_HNZVC_8(old, m, r)

    @opcode(0xf, 0x6f, 0x7f) # CLR (direct, indexed, extended)
    def instruction_CLR_memory(self, opcode, ea):
        """
        Clear memory location
        source code forms: CLR
        CC bits "HNZVC": -0100
        """
        self.cc.update_0100()
        return ea, 0x00

    @opcode(0x4f, 0x5f) # CLRA / CLRB (inherent)
    def instruction_CLR_register(self, opcode, register):
        """
        Clear accumulator A or B

        source code forms: CLRA; CLRB
        CC bits "HNZVC": -0100
        """
        register.value = 0
        self.cc.update_0100()

    def COM(self, value):
        """
        CC bits "HNZVC": -aa01
        """
        value = ~value # the bits of m inverted
        self.cc.clear_NZ()
        self.cc.update_NZ01_8(value)
        return value

    @opcode(# Complement memory location
        0x3, 0x63, 0x73, # COM (direct, indexed, extended)
    )
    def instruction_COM_memory(self, opcode, ea, m):
        """
        Replaces the contents of memory location M with its logical complement.
        source code forms: COM Q
        """
        r = self.COM(value=m)
#        log.debug("$%x COM memory $%x to $%x" % (
#            self.program_counter, m, r,
#        ))
        return ea, r & 0xff

    @opcode(# Complement accumulator
        0x43, # COMA (inherent)
        0x53, # COMB (inherent)
    )
    def instruction_COM_register(self, opcode, register):
        """
        Replaces the contents of accumulator A or B with its logical complement.
        source code forms: COMA; COMB
        """
        register.value = self.COM(value=register.value) & register.BASE
#        log.debug("$%x COM %s" % (
#            self.program_counter, register.name,
#        ))

    @opcode(# Decimal adjust A accumulator
        0x19, # DAA (inherent)
    )
    def instruction_DAA(self, opcode):
        """
        The sequence of a single-byte add instruction on accumulator A (either
        ADDA or ADCA) and a following decimal addition adjust instruction
        results in a BCD addition with an appropriate carry bit. Both values to
        be added must be in proper BCD form (each nibble such that: 0 <= nibble
        <= 9). Multiple-precision addition must add the carry generated by this
        decimal addition adjust into the next higher digit during the add
        operation (ADCA) immediately prior to the next decimal addition adjust.

        source code forms: DAA

        CC bits "HNZVC": -aa0a

        Operation:
            ACCA' ← ACCA + CF(MSN):CF(LSN)

        where CF is a Correction Factor, as follows:
        the CF for each nibble (BCD) digit is determined separately,
        and is either 6 or 0.

        Least Significant Nibble
        CF(LSN) = 6 IFF 1)    C = 1
                     or 2)    LSN > 9

        Most Significant Nibble
        CF(MSN) = 6 IFF 1)    C = 1
                     or 2)    MSN > 9
                     or 3)    MSN > 8 and LSN > 9

        Condition Codes:
        H    -    Not affected.
        N    -    Set if the result is negative; cleared otherwise.
        Z    -    Set if the result is zero; cleared otherwise.
        V    -    Undefined.
        C    -    Set if a carry is generated or if the carry bit was set before the operation; cleared otherwise.
        """
        a = self.accu_a.value

        correction_factor = 0
        a_hi = a & 0xf0 # MSN - Most Significant Nibble
        a_lo = a & 0x0f # LSN - Least Significant Nibble

        if a_lo > 0x09 or self.cc.H: # cc & 0x20:
            correction_factor |= 0x06

        if a_hi > 0x80 and a_lo > 0x09:
            correction_factor |= 0x60

        if a_hi > 0x90 or self.cc.C: # cc & 0x01:
            correction_factor |= 0x60

        new_value = correction_factor + a
        self.accu_a.value = new_value & self.accu_a.BASE

        self.cc.clear_NZ() # V is undefined
        self.cc.update_NZC_8(new_value)

    def DEC(self, a):
        """
        Subtract one from the register. The carry bit is not affected, thus
        allowing this instruction to be used as a loop counter in multiple-
        precision computations. When operating on unsigned values, only BEQ and
        BNE branches can be expected to behave consistently. When operating on
        twos complement values, all signed branches are available.

        source code forms: DEC Q; DECA; DECB

        CC bits "HNZVC": -aaa-
        """
        a -= 1
        self.cc.clear_NZV()
        self.cc.update_NZ_8(a)
        if a == 0x7f:
            self.cc.V = 1
        return a

    @opcode(0xa, 0x6a, 0x7a) # DEC (direct, indexed, extended)
    def instruction_DEC_memory(self, opcode, ea, m):
        """ Decrement memory location """
        return ea, self.DEC(m) & 0xff

    @opcode(0x4a, 0x5a) # DECA / DECB (inherent)
    def instruction_DEC_register(self, opcode, register):
        """ Decrement accumulator """
        register.value = self.DEC(register.value) & register.BASE

    def INC(self, a):
        a += 1
        self.cc.clear_NZV()
        self.cc.update_NZ_8(a)
        if a == 0x80:
            self.cc.V = 1
        return a

    @opcode(# Increment accumulator
        0x4c, # INCA (inherent)
        0x5c, # INCB (inherent)
    )
    def instruction_INC_register(self, opcode, register):
        """
        Adds to the register. The carry bit is not affected, thus allowing this
        instruction to be used as a loop counter in multiple-precision
        computations. When operating on unsigned values, only the BEQ and BNE
        branches can be expected to behave consistently. When operating on twos
        complement values, all signed branches are correctly available.

        source code forms: INC Q; INCA; INCB

        CC bits "HNZVC": -aaa-
        """
        register.value = self.INC(register.value) & register.BASE

    @opcode(# Increment memory location
        0xc, 0x6c, 0x7c, # INC (direct, indexed, extended)
    )
    def instruction_INC_memory(self, opcode, ea, m):
        """
        Adds to the register. The carry bit is not affected, thus allowing this
        instruction to be used as a loop counter in multiple-precision
        computations. When operating on unsigned values, only the BEQ and BNE
        branches can be expected to behave consistently. When operating on twos
        complement values, all signed branches are correctly available.

        source code forms: INC Q; INCA; INCB

        CC bits "HNZVC": -aaa-
        """
        return ea, self.INC(m) & 0xff

    @opcode(# Load effective address into an indexable register
        0x32, # LEAS (indexed)
        0x33, # LEAU (indexed)
    )
    def instruction_LEA_pointer(self, opcode, ea, register):
        """
        Calculates the effective address from the indexed addressing mode and
        places the address in an indexable register.

        LEAU and LEAS do not affect the Z bit to allow cleaning up the stack
        while returning the Z bit as a parameter to a calling routine, and also
        for MC6800 INS/DES compatibility.

        LEAU -10,U   U-10 -> U     Subtracts 10 from U
        LEAS -10,S   S-10 -> S     Used to reserve area on stack
        LEAS 10,S    S+10 -> S     Used to 'clean up' stack
        LEAX 5,S     S+5 -> X      Transfers as well as adds

        source code forms: LEAS, LEAU

        CC bits "HNZVC": -----
        """
#         log.debug(
#             "$%04x LEA %s: Set %s to $%04x \t| %s" % (
#             self.program_counter,
#             register.name, register.name, ea,
#             self.cfg.mem_info.get_shortest(ea)
#         ))
        register.value = ea & register.BASE

    @opcode(# Load effective address into an indexable register
        0x30, # LEAX (indexed)
        0x31, # LEAY (indexed)
    )
    def instruction_LEA_register(self, opcode, ea, register):
        """ see instruction_LEA_pointer

        LEAX and LEAY affect the Z (zero) bit to allow use of these registers
        as counters and for MC6800 INX/DEX compatibility.

        LEAX 10,X    X+10 -> X     Adds 5-bit constant 10 to X
        LEAX 500,X   X+500 -> X    Adds 16-bit constant 500 to X
        LEAY A,Y     Y+A -> Y      Adds 8-bit accumulator to Y
        LEAY D,Y     Y+D -> Y      Adds 16-bit D accumulator to Y

        source code forms: LEAX, LEAY

        CC bits "HNZVC": --a--
        """
#         log.debug("$%04x LEA %s: Set %s to $%04x \t| %s" % (
#             self.program_counter,
#             register.name, register.name, ea,
#             self.cfg.mem_info.get_shortest(ea)
#         ))
        register.value = ea & register.BASE
        self.cc.Z = 0
        self.cc.set_Z16(ea)

    @opcode(# Unsigned multiply (A * B ? D)
        0x3d, # MUL (inherent)
    )
    def instruction_MUL(self, opcode):
        """
        Multiply the unsigned binary numbers in the accumulators and place the
        result in both accumulators (ACCA contains the most-significant byte of
        the result). Unsigned multiply allows multiple-precision operations.

        The C (carry) bit allows rounding the most-significant byte through the
        sequence: MUL, ADCA #0.

        source code forms: MUL

        CC bits "HNZVC": --a-a
        """
        r = self.accu_a.value * self.accu_b.value
        self.accu_d.value = r & self.accu_d.BASE
        self.cc.Z = 0 if r else 1
        self.cc.C = 1 if r & 0x80 else 0

    @opcode(# Negate accumulator
        0x40, # NEGA (inherent)
        0x50, # NEGB (inherent)
    )
    def instruction_NEG_register(self, opcode, register):
        """
        Replaces the register with its twos complement. The C (carry) bit
        represents a borrow and is set to the inverse of the resulting binary
        carry. Note that 80 16 is replaced by itself and only in this case is
        the V (overflow) bit set. The value 00 16 is also replaced by itself,
        and only in this case is the C (carry) bit cleared.

        source code forms: NEG Q; NEGA; NEG B

        CC bits "HNZVC": uaaaa
        """
        x = register.value
        r = x * -1 # same as: r = ~x + 1
        register.value = r & register.BASE
#        log.debug("$%04x NEG %s $%02x to $%02x" % (
#            self.program_counter, register.name, x, r,
#        ))
        self.cc.clear_NZVC()
        self.cc.update_NZVC_8(0, x, r)

    _wrong_NEG = 0
    @opcode(0x0, 0x60, 0x70) # NEG (direct, indexed, extended)
    def instruction_NEG_memory(self, opcode, ea, m):
        """ Negate memory """
        if opcode == 0x0 and ea == 0x0 and m == 0x0:
            self._wrong_NEG += 1
            if self._wrong_NEG > 10:
                raise RuntimeError("Wrong PC ???")
        else:
            self._wrong_NEG = 0

        r = m * -1 # same as: r = ~m + 1

#        log.debug("$%04x NEG $%02x from %04x to $%02x" % (
#             self.program_counter, m, ea, r,
#         ))
        self.cc.clear_NZVC()
        self.cc.update_NZVC_8(0, m, r)
        return ea, r & 0xff

    @opcode(0x12) # NOP (inherent)
    def instruction_NOP(self, opcode):
        """
        No operation

        source code forms: NOP

        CC bits "HNZVC": -----
        """
#        log.debug("\tNOP")



    @opcode(# Push A, B, CC, DP, D, X, Y, U, or PC onto stack
        0x36, # PSHU (immediate)
        0x34, # PSHS (immediate)
    )
    def instruction_PSH(self, opcode, m, register):
        """
        All, some, or none of the processor registers are pushed onto stack
        (with the exception of stack pointer itself).

        A single register may be placed on the stack with the condition codes
        set by doing an autodecrement store onto the stack (example: STX ,--S).

        source code forms: b7 b6 b5 b4 b3 b2 b1 b0 PC U Y X DP B A CC push order
        ->

        CC bits "HNZVC": -----
        """
        assert register in (self.system_stack_pointer, self.user_stack_pointer)

        def push(register_str, stack_pointer):
            register_obj = self.register_str2object[register_str]
            data = register_obj.value

#             log.debug("\tpush %s with data $%x", register_obj.name, data)

            if register_obj.WIDTH == 8:
                self.push_byte(register, data)
            else:
                assert register_obj.WIDTH == 16
                self.push_word(register, data)

#        log.debug("$%x PSH%s post byte: $%x", self.program_counter, register.name, m)

        # m = postbyte
        if m & 0x80: push(REG_PC, register) # 16 bit program counter register
        if m & 0x40: push(REG_U, register) #  16 bit user-stack pointer
        if m & 0x20: push(REG_Y, register) #  16 bit index register
        if m & 0x10: push(REG_X, register) #  16 bit index register
        if m & 0x08: push(REG_DP, register) #  8 bit direct page register
        if m & 0x04: push(REG_B, register) #   8 bit accumulator
        if m & 0x02: push(REG_A, register) #   8 bit accumulator
        if m & 0x01: push(REG_CC, register) #  8 bit condition code register


    @opcode(# Pull A, B, CC, DP, D, X, Y, U, or PC from stack
        0x37, # PULU (immediate)
        0x35, # PULS (immediate)
    )
    def instruction_PUL(self, opcode, m, register):
        """
        All, some, or none of the processor registers are pulled from stack
        (with the exception of stack pointer itself).

        A single register may be pulled from the stack with condition codes set
        by doing an autoincrement load from the stack (example: LDX ,S++).

        source code forms: b7 b6 b5 b4 b3 b2 b1 b0 PC U Y X DP B A CC = pull
        order

        CC bits "HNZVC": ccccc
        """
        assert register in (self.system_stack_pointer, self.user_stack_pointer)

        def pull(register_str, stack_pointer):
            reg_obj = self.register_str2object[register_str]
            if reg_obj.WIDTH == 8:
                data = self.pull_byte(stack_pointer)
            else:
                assert reg_obj.WIDTH == 16
                data = self.pull_word(stack_pointer)
            reg_obj.value = data & reg_obj.BASE

#        log.debug("$%x PUL%s:", self.program_counter, register.name)

        # m = postbyte
        if m & 0x01: pull(REG_CC, register) # 8 bit condition code register
        if m & 0x02: pull(REG_A, register) # 8 bit accumulator
        if m & 0x04: pull(REG_B, register) # 8 bit accumulator
        if m & 0x08: pull(REG_DP, register) # 8 bit direct page register
        if m & 0x10: pull(REG_X, register) # 16 bit index register
        if m & 0x20: pull(REG_Y, register) # 16 bit index register
        if m & 0x40: pull(REG_U, register) # 16 bit user-stack pointer
        if m & 0x80: pull(REG_PC, register) # 16 bit program counter register

    @opcode(# Subtract memory from accumulator with borrow
        0x82, 0x92, 0xa2, 0xb2, # SBCA (immediate, direct, indexed, extended)
        0xc2, 0xd2, 0xe2, 0xf2, # SBCB (immediate, direct, indexed, extended)
    )
    def instruction_SBC(self, opcode, m, register):
        """
        Subtracts the contents of memory location M and the borrow (in the C
        (carry) bit) from the contents of the designated 8-bit register, and
        places the result in that register. The C bit represents a borrow and is
        set to the inverse of the resulting binary carry.

        source code forms: SBCA P; SBCB P

        CC bits "HNZVC": uaaaa
        """
        a = register.value
        r = a - m - self.cc.C
        register.value = r & register.BASE
#        log.debug("$%x %02x SBC %s: %i - %i - %i = %i (=$%x)" % (
#            self.program_counter, opcode, register.name,
#            a, m, self.cc.C, r, r
#        ))
        self.cc.clear_NZVC()
        self.cc.update_NZVC_8(a, m, r)

    @opcode(# Sign Extend B accumulator into A accumulator
        0x1d, # SEX (inherent)
    )
    def instruction_SEX(self, opcode):
        """
        This instruction transforms a twos complement 8-bit value in accumulator
        B into a twos complement 16-bit value in the D accumulator.

        source code forms: SEX

        CC bits "HNZVC": -aa0-

            // 0x1d SEX inherent
            case 0x1d:
                WREG_A = (RREG_B & 0x80) ? 0xff : 0;
                CLR_NZ;
                SET_NZ16(REG_D);
                peek_byte(cpu, REG_PC);

        #define SIGNED(b) ((Word)(b&0x80?b|0xff00:b))
        case 0x1D: /* SEX */ tw=SIGNED(ibreg); SETNZ16(tw) SETDREG(tw) break;
        """
        if not self.accu_b.value & 0x80:
            self.accu_a.value = 0

        self.cc.clear_NZ()
        self.cc.update_NZ_16(self.accu_d.value)



    @opcode(# Subtract memory from accumulator
        0x80, 0x90, 0xa0, 0xb0, # SUBA (immediate, direct, indexed, extended)
        0xc0, 0xd0, 0xe0, 0xf0, # SUBB (immediate, direct, indexed, extended)
        0x83, 0x93, 0xa3, 0xb3, # SUBD (immediate, direct, indexed, extended)
    )
    def instruction_SUB(self, opcode, m, register):
        """
        Subtracts the value in memory location M from the contents of a
        register. The C (carry) bit represents a borrow and is set to the
        inverse of the resulting binary carry.

        source code forms: SUBA P; SUBB P; SUBD P

        CC bits "HNZVC": uaaaa
        """
        r = register.value
        r_new = r - m
        register.value = r_new & register.BASE
#        log.debug("$%x SUB8 %s: $%x - $%x = $%x (dez.: %i - %i = %i)" % (
#            self.program_counter, register.name,
#            r, m, r_new,
#            r, m, r_new,
#        ))
        self.cc.clear_NZVC()
        if register.WIDTH == 8:
            self.cc.update_NZVC_8(r, m, r_new)
        else:
            assert register.WIDTH == 16
            self.cc.update_NZVC_16(r, m, r_new)


    # ---- Register Changes - FIXME: Better name for this section?!? ----

    REGISTER_BIT2STR = {
        0x0: REG_D, # 0000 - 16 bit concatenated reg.(A B)
        0x1: REG_X, # 0001 - 16 bit index register
        0x2: REG_Y, # 0010 - 16 bit index register
        0x3: REG_U, # 0011 - 16 bit user-stack pointer
        0x4: REG_S, # 0100 - 16 bit system-stack pointer
        0x5: REG_PC, # 0101 - 16 bit program counter register
        0x6: undefined_reg.name, # undefined
        0x7: undefined_reg.name, # undefined
        0x8: REG_A, # 1000 - 8 bit accumulator
        0x9: REG_B, # 1001 - 8 bit accumulator
        0xa: REG_CC, # 1010 - 8 bit condition code register as flags
        0xb: REG_DP, # 1011 - 8 bit direct page register
        0xc: undefined_reg.name, # undefined
        0xd: undefined_reg.name, # undefined
        0xe: undefined_reg.name, # undefined
        0xf: undefined_reg.name, # undefined
    }

    def _get_register_obj(self, addr):
        return self.registers[addr]

    def _get_register_and_value(self, addr):
        reg = self._get_register_obj(addr)
        return reg, reg.value

    @opcode(0x1f) # TFR (immediate)
    def instruction_TFR(self, opcode, m):
        """
        source code forms: TFR R1, R2
        CC bits "HNZVC": ccccc
        """
        high, low = divmod(m, 16)
        src_reg = self.registers[high]
        dst_reg = self.registers[low]
        dst_reg.value = src_reg.value
        if src_reg.WIDTH != dst_reg.WIDTH:
            if src_reg.WIDTH == 16:
                dst_reg.value &= 0xff
            else:
                dst_reg.value |= 0xff00

    @opcode(# Exchange R1 with R2
        0x1e, # EXG (immediate)
    )
    def instruction_EXG(self, opcode, m):
        """
        source code forms: EXG R1,R2
        CC bits "HNZVC": ccccc
        """
        high, low = divmod(m, 16)
        reg1 = self.registers[high]
        reg2 = self.registers[low]
        reg1.value, reg2.value = reg2.value, reg1.value
        if reg1.WIDTH != reg2.WIDTH:
            if reg1.WIDTH == 8:
                reg1.value &= 0xff
                reg2.value |= 0xff00
            else:
                reg2.value &= 0xff
                reg1.value |= 0xff00

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
        register.value = m & register.BASE
        self.cc.clear_NZV()
        self.cc.update_NZ_16(m)

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
        register.value = m & register.BASE
        self.cc.clear_NZV()
        self.cc.update_NZ_8(m)

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
        self.cc.clear_NZV()
        self.cc.update_NZ_16(value)
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
        self.cc.clear_NZV()
        self.cc.update_NZ_8(value)
        return ea, value # write byte to Memory


    # ---- Logical Operations ----


    @opcode(# AND memory with accumulator
        0x84, 0x94, 0xa4, 0xb4, # ANDA (immediate, direct, indexed, extended)
        0xc4, 0xd4, 0xe4, 0xf4, # ANDB (immediate, direct, indexed, extended)
    )
    def instruction_AND(self, opcode, m, register):
        """
        Performs the logical AND operation between the contents of an
        accumulator and the contents of memory location M and the result is
        stored in the accumulator.

        source code forms: ANDA P; ANDB P

        CC bits "HNZVC": -aa0-
        """
        r = register.value & m
        register.value = r & register.BASE
        self.cc.clear_NZV()
        self.cc.update_NZ_8(r)
#        log.debug("\tAND %s: %i & %i = %i",
#            register.name, a, m, r
#        )

    @opcode(# Exclusive OR memory with accumulator
        0x88, 0x98, 0xa8, 0xb8, # EORA (immediate, direct, indexed, extended)
        0xc8, 0xd8, 0xe8, 0xf8, # EORB (immediate, direct, indexed, extended)
    )
    def instruction_EOR(self, opcode, m, register):
        """
        The contents of memory location M is exclusive ORed into an 8-bit
        register.

        source code forms: EORA P; EORB P

        CC bits "HNZVC": -aa0-
        """
        r = register.value ^ m
        register.value = r & register.BASE
        self.cc.clear_NZV()
        self.cc.update_NZ_8(r)
#        log.debug("\tEOR %s: %i ^ %i = %i",
#            register.name, a, m, r
#        )

    @opcode(# OR memory with accumulator
        0x8a, 0x9a, 0xaa, 0xba, # ORA (immediate, direct, indexed, extended)
        0xca, 0xda, 0xea, 0xfa, # ORB (immediate, direct, indexed, extended)
    )
    def instruction_OR(self, opcode, m, register):
        """
        Performs an inclusive OR operation between the contents of accumulator A
        or B and the contents of memory location M and the result is stored in
        accumulator A or B.

        source code forms: ORA P; ORB P

        CC bits "HNZVC": -aa0-
        """
        r = register.value | m
        register.value = r & register.BASE
        self.cc.clear_NZV()
        self.cc.update_NZ_8(r)
#         log.debug("$%04x OR %s: %02x | %02x = %02x",
#             self.program_counter, register.name, a, m, r
#         )


    # ---- CC manipulation ----


    @opcode(# AND condition code register
        0x1c, # ANDCC (immediate)
    )
    def instruction_ANDCC(self, opcode, m, register):
        """
        Performs a logical AND between the condition code register and the
        immediate byte specified in the instruction and places the result in the
        condition code register.

        source code forms: ANDCC #xx

        CC bits "HNZVC": ddddd
        """
        assert register == self.cc

        self.cc.value &= m


    @opcode(# OR condition code register
        0x1a, # ORCC (immediate)
    )
    def instruction_ORCC(self, opcode, m, register):
        """
        Performs an inclusive OR operation between the contents of the condition
        code registers and the immediate value, and the result is placed in the
        condition code register. This instruction may be used to set interrupt
        masks (disable interrupts) or any other bit(s).

        source code forms: ORCC #XX

        CC bits "HNZVC": ddddd
        """
        assert register == self.cc

        self.cc.value |= m

    # ---- Test Instructions ----


    @opcode(# Compare memory from stack pointer
        0x1083, 0x1093, 0x10a3, 0x10b3, # CMPD (immediate, direct, indexed, extended)
        0x118c, 0x119c, 0x11ac, 0x11bc, # CMPS (immediate, direct, indexed, extended)
        0x1183, 0x1193, 0x11a3, 0x11b3, # CMPU (immediate, direct, indexed, extended)
        0x8c, 0x9c, 0xac, 0xbc, # CMPX (immediate, direct, indexed, extended)
        0x108c, 0x109c, 0x10ac, 0x10bc, # CMPY (immediate, direct, indexed, extended)
    )
    def instruction_CMP16(self, opcode, m, register):
        """
        Compares the 16-bit contents of the concatenated memory locations M:M+1
        to the contents of the specified register and sets the appropriate
        condition codes. Neither the memory locations nor the specified register
        is modified unless autoincrement or autodecrement are used. The carry
        flag represents a borrow and is set to the inverse of the resulting
        binary carry.

        source code forms: CMPD P; CMPX P; CMPY P; CMPU P; CMPS P

        CC bits "HNZVC": -aaaa
        """
        r = register.value
        r_new = r - m
#        log.warning("$%x CMP16 %s $%x - $%x = $%x" % (
#             self.program_counter,
#             register.name,
#             r, m, r_new,
#         ))
        self.cc.clear_NZVC()
        self.cc.update_NZVC_16(r, m, r_new)

    @opcode(# Compare memory from accumulator
        0x81, 0x91, 0xa1, 0xb1, # CMPA (immediate, direct, indexed, extended)
        0xc1, 0xd1, 0xe1, 0xf1, # CMPB (immediate, direct, indexed, extended)
    )
    def instruction_CMP8(self, opcode, m, register):
        """
        Compares the contents of memory location to the contents of the
        specified register and sets the appropriate condition codes. Neither
        memory location M nor the specified register is modified. The carry flag
        represents a borrow and is set to the inverse of the resulting binary
        carry.

        source code forms: CMPA P; CMPB P

        CC bits "HNZVC": uaaaa
        """
        r = register.value
        r_new = r - m
#         log.warning("$%x CMP8 %s $%x - $%x = $%x" % (
#             self.program_counter,
#             register.name,
#             r, m, r_new,
#         ))
        self.cc.clear_NZVC()
        self.cc.update_NZVC_8(r, m, r_new)


    @opcode(# Bit test memory with accumulator
        0x85, 0x95, 0xa5, 0xb5, # BITA (immediate, direct, indexed, extended)
        0xc5, 0xd5, 0xe5, 0xf5, # BITB (immediate, direct, indexed, extended)
    )
    def instruction_BIT(self, opcode, m, register):
        """
        Performs the logical AND of the contents of accumulator A or B and the
        contents of memory location M and modifies the condition codes
        accordingly. The contents of accumulator A or B and memory location M
        are not affected.

        source code forms: BITA P; BITB P

        CC bits "HNZVC": -aa0-
        """
        self.cc.clear_NZV()
        self.cc.update_NZ_8(m & register.value)

    @opcode(# Test accumulator
        0x4d, # TSTA (inherent)
        0x5d, # TSTB (inherent)
    )
    def instruction_TST_register(self, opcode, register):
        """
        Set the N (negative) and Z (zero) bits according to the contents of
        accumulator A or B, and clear the V (overflow) bit. The TST instruction
        provides only minimum information when testing unsigned values; since no
        unsigned value is less than zero, BLO and BLS have no utility. While BHI
        could be used after TST, it provides exactly the same control as BNE,
        which is preferred. The signed branches are available.

        The MC6800 processor clears the C (carry) bit.

        source code forms: TST Q; TSTA; TSTB

        CC bits "HNZVC": -aa0-
        """
        self.cc.clear_NZV()
        self.cc.update_NZ_8(register.value)

    @opcode(0xd, 0x6d, 0x7d) # TST (direct, indexed, extended)
    def instruction_TST_memory(self, opcode, m):
        """ Test memory location """
#         log.debug("$%x TST m=$%02x" % (
#             self.program_counter, m
#         ))
        self.cc.clear_NZV()
        self.cc.update_NZ_8(m)

    # ---- Programm Flow Instructions ----


    @opcode(# Jump
        0xe, 0x6e, 0x7e, # JMP (direct, indexed, extended)
    )
    def instruction_JMP(self, opcode, ea):
        """
        Program control is transferred to the effective address.

        source code forms: JMP EA

        CC bits "HNZVC": -----
        """
#        log.info("%x|\tJMP to $%x \t| %s" % (
#            self.last_op_address,
#            ea, self.cfg.mem_info.get_shortest(ea)
#        ))
        self.program_counter.value = ea & 0xffff

    @opcode(# Return from subroutine
        0x39, # RTS (inherent)
    )
    def instruction_RTS(self, opcode):
        """
        Program control is returned from the subroutine to the calling program.
        The return address is pulled from the stack.

        source code forms: RTS

        CC bits "HNZVC": -----
        """
        ea = self.pull_word(self.system_stack_pointer)
#        log.info("%x|\tRTS to $%x \t| %s" % (
#            self.last_op_address,
#            ea,
#            self.cfg.mem_info.get_shortest(ea)
#        ))
        self.program_counter.value = ea & 0xffff

    @opcode(
        # Branch to subroutine:
        0x8d, # BSR (relative)
        0x17, # LBSR (relative)
        # Jump to subroutine:
        0x9d, 0xad, 0xbd, # JSR (direct, indexed, extended)
    )
    def instruction_BSR_JSR(self, opcode, ea):
        """
        Program control is transferred to the effective address after storing
        the return address on the hardware stack.

        A return from subroutine (RTS) instruction is used to reverse this
        process and must be the last instruction executed in a subroutine.

        source code forms: BSR dd; LBSR DDDD; JSR EA

        CC bits "HNZVC": -----
        """
#        log.info("%x|\tJSR/BSR to $%x \t| %s" % (
#            self.last_op_address,
#            ea, self.cfg.mem_info.get_shortest(ea)
#        ))
        self.push_word(self.system_stack_pointer, self.program_counter.value)
        self.program_counter.value = ea & 0xffff


    # ---- Branch Instructions ----


    @opcode(# Branch if equal
        0x27, # BEQ (relative)
        0x1027, # LBEQ (relative)
    )
    def instruction_BEQ(self, opcode, ea):
        """
        Tests the state of the Z (zero) bit and causes a branch if it is set.
        When used after a subtract or compare operation, this instruction will
        branch if the compared values, signed or unsigned, were exactly the
        same.

        source code forms: BEQ dd; LBEQ DDDD

        CC bits "HNZVC": -----
        """
        if self.cc.Z == 1:
#            log.info("$%x BEQ branch to $%x, because Z==1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))
            self.program_counter.value = ea & 0xffff
#        else:
#            log.debug("$%x BEQ: don't branch to $%x, because Z==0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(# Branch if greater than or equal (signed)
        0x2c, # BGE (relative)
        0x102c, # LBGE (relative)
    )
    def instruction_BGE(self, opcode, ea):
        """
        Causes a branch if the N (negative) bit and the V (overflow) bit are
        either both set or both clear. That is, branch if the sign of a valid
        twos complement result is, or would be, positive. When used after a
        subtract or compare operation on twos complement values, this
        instruction will branch if the register was greater than or equal to the
        memory register.

        source code forms: BGE dd; LBGE DDDD

        CC bits "HNZVC": -----
        """
        # Note these variantes are the same:
        #    self.cc.N == self.cc.V
        #    (self.cc.N ^ self.cc.V) == 0
        #    not operator.xor(self.cc.N, self.cc.V)
        if self.cc.N == self.cc.V:
#            log.info("$%x BGE branch to $%x, because N XOR V == 0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))
            self.program_counter.value = ea & 0xffff
#         else:
#             log.debug("$%x BGE: don't branch to $%x, because N XOR V != 0 \t| %s" % (
#                 self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#             ))

    @opcode(# Branch if greater (signed)
        0x2e, # BGT (relative)
        0x102e, # LBGT (relative)
    )
    def instruction_BGT(self, opcode, ea):
        """
        Causes a branch if the N (negative) bit and V (overflow) bit are either
        both set or both clear and the Z (zero) bit is clear. In other words,
        branch if the sign of a valid twos complement result is, or would be,
        positive and not zero. When used after a subtract or compare operation
        on twos complement values, this instruction will branch if the register
        was greater than the memory register.

        source code forms: BGT dd; LBGT DDDD

        CC bits "HNZVC": -----
        """
        # Note these variantes are the same:
        #    not ((self.cc.N ^ self.cc.V) == 1 or self.cc.Z == 1)
        #    not ((self.cc.N ^ self.cc.V) | self.cc.Z)
        #    self.cc.N == self.cc.V and self.cc.Z == 0
        # ;)
        if not self.cc.Z and self.cc.N == self.cc.V:
#            log.info("$%x BGT branch to $%x, because (N==V and Z==0) \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))
            self.program_counter.value = ea & 0xffff
#         else:
#            log.debug("$%x BGT: don't branch to $%x, because (N==V and Z==0) is False \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(# Branch if higher (unsigned)
        0x22, # BHI (relative)
        0x1022, # LBHI (relative)
    )
    def instruction_BHI(self, opcode, ea):
        """
        Causes a branch if the previous operation caused neither a carry nor a
        zero result. When used after a subtract or compare operation on unsigned
        binary values, this instruction will branch if the register was higher
        than the memory register.

        Generally not useful after INC/DEC, LD/TST, and TST/CLR/COM
        instructions.

        source code forms: BHI dd; LBHI DDDD

        CC bits "HNZVC": -----
        """
        if not self.cc.C and not self.cc.Z:
#            log.info("$%x BHI branch to $%x, because C==0 and Z==0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))
            self.program_counter.value = ea & 0xffff
#         else:
#            log.debug("$%x BHI: don't branch to $%x, because C and Z not 0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(# Branch if less than or equal (signed)
        0x2f, # BLE (relative)
        0x102f, # LBLE (relative)
    )
    def instruction_BLE(self, opcode, ea):
        """
        Causes a branch if the exclusive OR of the N (negative) and V (overflow)
        bits is 1 or if the Z (zero) bit is set. That is, branch if the sign of
        a valid twos complement result is, or would be, negative. When used
        after a subtract or compare operation on twos complement values, this
        instruction will branch if the register was less than or equal to the
        memory register.

        source code forms: BLE dd; LBLE DDDD

        CC bits "HNZVC": -----
        """
        if self.cc.N ^ self.cc.V or self.cc.Z:
#            log.info("$%x BLE branch to $%x, because N^V==1 or Z==1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))
            self.program_counter.value = ea & 0xffff
#         else:
#            log.debug("$%x BLE: don't branch to $%x, because N^V!=1 and Z!=1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(# Branch if lower or same (unsigned)
        0x23, # BLS (relative)
        0x1023, # LBLS (relative)
    )
    def instruction_BLS(self, opcode, ea):
        """
        Causes a branch if the previous operation caused either a carry or a
        zero result. When used after a subtract or compare operation on unsigned
        binary values, this instruction will branch if the register was lower
        than or the same as the memory register.

        Generally not useful after INC/DEC, LD/ST, and TST/CLR/COM instructions.

        source code forms: BLS dd; LBLS DDDD

        CC bits "HNZVC": -----
        """
#         if (self.cc.C|self.cc.Z) == 0:
        if self.cc.C or self.cc.Z:
#            log.info("$%x BLS branch to $%x, because C|Z==1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))
            self.program_counter.value = ea & 0xffff
#         else:
#            log.debug("$%x BLS: don't branch to $%x, because C|Z!=1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(# Branch if less than (signed)
        0x2d, # BLT (relative)
        0x102d, # LBLT (relative)
    )
    def instruction_BLT(self, opcode, ea):
        """
        Causes a branch if either, but not both, of the N (negative) or V
        (overflow) bits is set. That is, branch if the sign of a valid twos
        complement result is, or would be, negative. When used after a subtract
        or compare operation on twos complement binary values, this instruction
        will branch if the register was less than the memory register.

        source code forms: BLT dd; LBLT DDDD

        CC bits "HNZVC": -----
        """
        if self.cc.N ^ self.cc.V: # N xor V
#            log.info("$%x BLT branch to $%x, because N XOR V == 1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))
            self.program_counter.value = ea & 0xffff
#         else:
#            log.debug("$%x BLT: don't branch to $%x, because N XOR V != 1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(# Branch if minus
        0x2b, # BMI (relative)
        0x102b, # LBMI (relative)
    )
    def instruction_BMI(self, opcode, ea):
        """
        Tests the state of the N (negative) bit and causes a branch if set. That
        is, branch if the sign of the twos complement result is negative.

        When used after an operation on signed binary values, this instruction
        will branch if the result is minus. It is generally preferred to use the
        LBLT instruction after signed operations.

        source code forms: BMI dd; LBMI DDDD

        CC bits "HNZVC": -----
        """
        if self.cc.N:
#            log.info("$%x BMI branch to $%x, because N==1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))
            self.program_counter.value = ea & 0xffff
#         else:
#            log.debug("$%x BMI: don't branch to $%x, because N==0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(# Branch if not equal
        0x26, # BNE (relative)
        0x1026, # LBNE (relative)
    )
    def instruction_BNE(self, opcode, ea):
        """
        Tests the state of the Z (zero) bit and causes a branch if it is clear.
        When used after a subtract or compare operation on any binary values,
        this instruction will branch if the register is, or would be, not equal
        to the memory register.

        source code forms: BNE dd; LBNE DDDD

        CC bits "HNZVC": -----
        """
        if not self.cc.Z:
#            log.info("$%x BNE branch to $%x, because Z==0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))
            self.program_counter.value = ea & 0xffff
#        else:
#            log.debug("$%x BNE: don't branch to $%x, because Z==1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(# Branch if plus
        0x2a, # BPL (relative)
        0x102a, # LBPL (relative)
    )
    def instruction_BPL(self, opcode, ea):
        """
        Tests the state of the N (negative) bit and causes a branch if it is
        clear. That is, branch if the sign of the twos complement result is
        positive.

        When used after an operation on signed binary values, this instruction
        will branch if the result (possibly invalid) is positive. It is
        generally preferred to use the BGE instruction after signed operations.

        source code forms: BPL dd; LBPL DDDD

        CC bits "HNZVC": -----
        """
        if not self.cc.N:
#            log.info("$%x BPL branch to $%x, because N==0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))
            self.program_counter.value = ea & 0xffff
#         else:
#            log.debug("$%x BPL: don't branch to $%x, because N==1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(# Branch always
        0x20, # BRA (relative)
        0x16, # LBRA (relative)
    )
    def instruction_BRA(self, opcode, ea):
        """
        Causes an unconditional branch.

        source code forms: BRA dd; LBRA DDDD

        CC bits "HNZVC": -----
        """
#        log.info("$%x BRA branch to $%x \t| %s" % (
#            self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#        ))
        self.program_counter.value = ea & 0xffff

    @opcode(# Branch never
        0x21, # BRN (relative)
        0x1021, # LBRN (relative)
    )
    def instruction_BRN(self, opcode, ea):
        """
        Does not cause a branch. This instruction is essentially a no operation,
        but has a bit pattern logically related to branch always.

        source code forms: BRN dd; LBRN DDDD

        CC bits "HNZVC": -----
        """
        pass

    @opcode(# Branch if valid twos complement result
        0x28, # BVC (relative)
        0x1028, # LBVC (relative)
    )
    def instruction_BVC(self, opcode, ea):
        """
        Tests the state of the V (overflow) bit and causes a branch if it is
        clear. That is, branch if the twos complement result was valid. When
        used after an operation on twos complement binary values, this
        instruction will branch if there was no overflow.

        source code forms: BVC dd; LBVC DDDD

        CC bits "HNZVC": -----
        """
        if not self.cc.V:
#            log.info("$%x BVC branch to $%x, because V==0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))
            self.program_counter.value = ea & 0xffff
#         else:
#            log.debug("$%x BVC: don't branch to $%x, because V==1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(# Branch if invalid twos complement result
        0x29, # BVS (relative)
        0x1029, # LBVS (relative)
    )
    def instruction_BVS(self, opcode, ea):
        """
        Tests the state of the V (overflow) bit and causes a branch if it is
        set. That is, branch if the twos complement result was invalid. When
        used after an operation on twos complement binary values, this
        instruction will branch if there was an overflow.

        source code forms: BVS dd; LBVS DDDD

        CC bits "HNZVC": -----
        """
        if self.cc.V:
#            log.info("$%x BVS branch to $%x, because V==1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))
            self.program_counter.value = ea & 0xffff
#         else:
#            log.debug("$%x BVS: don't branch to $%x, because V==0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(# Branch if lower (unsigned)
        0x25, # BLO/BCS (relative)
        0x1025, # LBLO/LBCS (relative)
    )
    def instruction_BLO(self, opcode, ea):
        """
        CC bits "HNZVC": -----
        case 0x5: cond = REG_CC & CC_C; break; // BCS, BLO, LBCS, LBLO
        """
        if self.cc.C:
#            log.info("$%x BLO/BCS/LBLO/LBCS branch to $%x, because C==1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))
            self.program_counter.value = ea & 0xffff
#         else:
#            log.debug("$%x BLO/BCS/LBLO/LBCS: don't branch to $%x, because C==0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(# Branch if lower (unsigned)
        0x24, # BHS/BCC (relative)
        0x1024, # LBHS/LBCC (relative)
    )
    def instruction_BHS(self, opcode, ea):
        """
        CC bits "HNZVC": -----
        case 0x4: cond = !(REG_CC & CC_C); break; // BCC, BHS, LBCC, LBHS
        """
        if not self.cc.C:
#            log.info("$%x BHS/BCC/LBHS/LBCC branch to $%x, because C==0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))
            self.program_counter.value = ea & 0xffff
#        else:
#            log.debug("$%x BHS/BCC/LBHS/LBCC: don't branch to $%x, because C==1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))


    # ---- Logical shift: LSL, LSR ----


    def LSL(self, a):
        """
        Shifts all bits of accumulator A or B or memory location M one place to
        the left. Bit zero is loaded with a zero. Bit seven of accumulator A or
        B or memory location M is shifted into the C (carry) bit.

        This is a duplicate assembly-language mnemonic for the single machine
        instruction ASL.

        source code forms: LSL Q; LSLA; LSLB

        CC bits "HNZVC": naaas
        """
        r = a << 1
        self.cc.clear_NZVC()
        self.cc.update_NZVC_8(a, a, r)
        return r

    @opcode(0x8, 0x68, 0x78) # LSL/ASL (direct, indexed, extended)
    def instruction_LSL_memory(self, opcode, ea, m):
        """
        Logical shift left memory location / Arithmetic shift of memory left
        """
        return ea, self.LSL(m) & 0xff

    @opcode(0x48, 0x58) # LSLA/ASLA / LSLB/ASLB (inherent)
    def instruction_LSL_register(self, opcode, register):
        """
        Logical shift left accumulator / Arithmetic shift of accumulator
        """
        register.value = self.LSL(register.value) & register.BASE

    def LSR(self, a):
        """
        Performs a logical shift right on the register. Shifts a zero into bit
        seven and bit zero into the C (carry) bit.

        source code forms: LSR Q; LSRA; LSRB

        CC bits "HNZVC": -0a-s
        """
        r = a >> 1
        self.cc.clear_NZC()
        self.cc.C = a & 1
        self.cc.set_Z8(r)
        return r

    @opcode(0x4, 0x64, 0x74) # LSR (direct, indexed, extended)
    def instruction_LSR_memory(self, opcode, ea, m):
        """ Logical shift right memory location """
        return ea, self.LSR(m) & 0xff

    @opcode(0x44, 0x54) # LSRA / LSRB (inherent)
    def instruction_LSR_register(self, opcode, register):
        """ Logical shift right accumulator """
        register.value = self.LSR(register.value) & register.BASE

    def ASR(self, a):
        """
        ASR (Arithmetic Shift Right) alias LSR (Logical Shift Right)

        Shifts all bits of the register one place to the right. Bit seven is held
        constant. Bit zero is shifted into the C (carry) bit.

        source code forms: ASR Q; ASRA; ASRB

        CC bits "HNZVC": uaa-s
        """
        r = (a >> 1) | (a & 0x80)
        self.cc.clear_NZC()
        self.cc.C = a & 1
        self.cc.update_NZ_8(r)
        return r

    @opcode(0x7, 0x67, 0x77) # ASR (direct, indexed, extended)
    def instruction_ASR_memory(self, opcode, ea, m):
        """ Arithmetic shift memory right """
        return ea, self.ASR(m) & 0xff

    @opcode(0x47, 0x57) # ASRA/ASRB (inherent)
    def instruction_ASR_register(self, opcode, register):
        """ Arithmetic shift accumulator right """
        register.value = self.ASR(register.value) & register.BASE


    # ---- Rotate: ROL, ROR ----


    def ROL(self, a):
        """
        Rotates all bits of the register one place left through the C (carry)
        bit. This is a 9-bit rotation.

        source code forms: ROL Q; ROLA; ROLB

        CC bits "HNZVC": -aaas
        """
        r = (a << 1) | self.cc.C
        self.cc.clear_NZVC()
        self.cc.update_NZVC_8(a, a, r)
        return r

    @opcode(0x9, 0x69, 0x79) # ROL (direct, indexed, extended)
    def instruction_ROL_memory(self, opcode, ea, m):
        """ Rotate memory left """
        return ea, self.ROL(m) & 0xff

    @opcode(0x49, 0x59) # ROLA / ROLB (inherent)
    def instruction_ROL_register(self, opcode, register):
        """ Rotate accumulator left """
        register.value = self.ROL(register.value) & register.BASE

    def ROR(self, a):
        """
        Rotates all bits of the register one place right through the C (carry)
        bit. This is a 9-bit rotation.

        moved the carry flag into bit 8
        moved bit 7 into carry flag

        source code forms: ROR Q; RORA; RORB

        CC bits "HNZVC": -aa-s
        """
        r = (a >> 1) | (self.cc.C << 7)
        self.cc.clear_NZ()
        self.cc.update_NZ_8(r)
        self.cc.C = a & 1
        return r

    @opcode(0x6, 0x66, 0x76) # ROR (direct, indexed, extended)
    def instruction_ROR_memory(self, opcode, ea, m):
        """ Rotate memory right """
        return ea, self.ROR(m) & 0xff

    @opcode(0x46, 0x56) # RORA/RORB (inherent)
    def instruction_ROR_register(self, opcode, register):
        """ Rotate accumulator right """
        register.value = self.ROR(register.value) & register.BASE


    # ---- Not Implemented, yet. ----


    @opcode(# AND condition code register, then wait for interrupt
        0x3c, # CWAI (immediate)
    )
    def instruction_CWAI(self, opcode, m):
        """
        This instruction ANDs an immediate byte with the condition code register
        which may clear the interrupt mask bits I and F, stacks the entire
        machine state on the hardware stack and then looks for an interrupt.
        When a non-masked interrupt occurs, no further machine state information
        need be saved before vectoring to the interrupt handling routine. This
        instruction replaced the MC6800 CLI WAI sequence, but does not place the
        buses in a high-impedance state. A FIRQ (fast interrupt request) may
        enter its interrupt handler with its entire machine state saved. The RTI
        (return from interrupt) instruction will automatically return the entire
        machine state after testing the E (entire) bit of the recovered
        condition code register.

        The following immediate values will have the following results: FF =
        enable neither EF = enable IRQ BF = enable FIRQ AF = enable both

        source code forms: CWAI #$XX E F H I N Z V C

        CC bits "HNZVC": ddddd
        """
#        log.error("$%x CWAI not implemented, yet!", opcode)
        # Update CC bits: ddddd

    @opcode(# Undocumented opcode!
        0x3e, # RESET (inherent)
    )
    def instruction_RESET(self, opcode):
        """
        Build the ASSIST09 vector table and setup monitor defaults, then invoke
        the monitor startup routine.

        source code forms:

        CC bits "HNZVC": *****
        """
        raise NotImplementedError("$%x RESET" % opcode)
        # Update CC bits: *****

    # ---- Interrupt handling ----

    irq_enabled = False
    def irq(self):
        if not self.irq_enabled or self.cc.I:
            # log.critical("$%04x *** IRQ, ignore!\t%s" % (
            #     self.program_counter.value, self.cc.get_info
            # ))
            return

        if self.cc.E:
            self.push_irq_registers()
        else:
            self.push_firq_registers()

        ea = self.memory.read_word(self.IRQ_VECTOR)
        # log.critical("$%04x *** IRQ, set PC to $%04x\t%s" % (
        #     self.program_counter.value, ea, self.cc.get_info
        # ))
        self.program_counter.value = ea & 0xffff

    def push_irq_registers(self):
        """
        push PC, U, Y, X, DP, B, A, CC on System stack pointer
        """
        self.cycles += 1
        self.push_word(self.system_stack_pointer, self.program_counter.value) # PC
        self.push_word(self.system_stack_pointer, self.user_stack_pointer.value) # U
        self.push_word(self.system_stack_pointer, self.index_y.value) # Y
        self.push_word(self.system_stack_pointer, self.index_x.value) # X
        self.push_byte(self.system_stack_pointer, self.direct_page.value) # DP
        self.push_byte(self.system_stack_pointer, self.accu_b.value) # B
        self.push_byte(self.system_stack_pointer, self.accu_a.value) # A
        self.push_byte(self.system_stack_pointer, self.cc.value) # CC

    def push_firq_registers(self):
        """
        FIRQ - Fast Interrupt Request
        push PC and CC on System stack pointer
        """
        self.cycles += 1
        self.push_word(self.system_stack_pointer, self.program_counter.value) # PC
        self.push_byte(self.system_stack_pointer, self.cc.value) # CC

    @opcode(# Return from interrupt
        0x3b, # RTI (inherent)
    )
    def instruction_RTI(self, opcode):
        """
        The saved machine state is recovered from the hardware stack and control
        is returned to the interrupted program. If the recovered E (entire) bit
        is clear, it indicates that only a subset of the machine state was saved
        (return address and condition codes) and only that subset is recovered.

        source code forms: RTI

        CC bits "HNZVC": -----
        """
        self.cc.value = self.pull_byte(self.system_stack_pointer) # CC
        if self.cc.E:
            self.accu_a.value = self.pull_byte(self.system_stack_pointer) & self.accu_a.BASE # A
            self.accu_b.value = self.pull_byte(self.system_stack_pointer) & self.accu_b.BASE # B
            self.direct_page.value = self.pull_byte(self.system_stack_pointer) & self.direct_page.BASE # DP
            self.index_x.value = self.pull_word(self.system_stack_pointer) & self.index_x.BASE # X
            self.index_y.value = self.pull_word(self.system_stack_pointer) & self.index_y.BASE # Y
            self.user_stack_pointer.value = self.pull_word(self.system_stack_pointer) & self.user_stack_pointer.BASE # U
        self.program_counter.value = self.pull_word(self.system_stack_pointer) & self.program_counter.BASE # PC


    @opcode(# Software interrupt (absolute indirect)
        0x3f, # SWI (inherent)
    )
    def instruction_SWI(self, opcode):
        """
        All of the processor registers are pushed onto the hardware stack (with
        the exception of the hardware stack pointer itself), and control is
        transferred through the software interrupt vector. Both the normal and
        fast interrupts are masked (disabled).

        source code forms: SWI

        CC bits "HNZVC": -----
        """
        raise NotImplementedError("$%x SWI" % opcode)

    @opcode(# Software interrupt (absolute indirect)
        0x103f, # SWI2 (inherent)
    )
    def instruction_SWI2(self, opcode, ea, m):
        """
        All of the processor registers are pushed onto the hardware stack (with
        the exception of the hardware stack pointer itself), and control is
        transferred through the software interrupt 2 vector. This interrupt is
        available to the end user and must not be used in packaged software.
        This interrupt does not mask (disable) the normal and fast interrupts.

        source code forms: SWI2

        CC bits "HNZVC": -----
        """
        raise NotImplementedError("$%x SWI2" % opcode)

    @opcode(# Software interrupt (absolute indirect)
        0x113f, # SWI3 (inherent)
    )
    def instruction_SWI3(self, opcode, ea, m):
        """
        All of the processor registers are pushed onto the hardware stack (with
        the exception of the hardware stack pointer itself), and control is
        transferred through the software interrupt 3 vector. This interrupt does
        not mask (disable) the normal and fast interrupts.

        source code forms: SWI3

        CC bits "HNZVC": -----
        """
        raise NotImplementedError("$%x SWI3" % opcode)

    @opcode(# Synchronize with interrupt line
        0x13, # SYNC (inherent)
    )
    def instruction_SYNC(self, opcode):
        """
        FAST SYNC WAIT FOR DATA Interrupt! LDA DISC DATA FROM DISC AND CLEAR
        INTERRUPT STA ,X+ PUT IN BUFFER DECB COUNT IT, DONE? BNE FAST GO AGAIN
        IF NOT.

        source code forms: SYNC

        CC bits "HNZVC": -----
        """
        raise NotImplementedError("$%x SYNC" % opcode)



class TypeAssert(CPU):
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
        super(TypeAssert, self).__init__(*args, **kwargs)
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

# CPU = TypeAssert # Should be only activated for debugging!


#------------------------------------------------------------------------------


def test_run():
    import sys
    import os
    import subprocess
    cmd_args = [
        sys.executable,
        os.path.join("..", "DragonPy_CLI.py"),
#        "--verbosity", "5",
        "--log", "dragonpy.components.cpu6809,50",

        "--machine", "Dragon32", "run",
#        "--machine", "Vectrex", "run",
#        "--max_ops", "1",
#        "--trace",
    ]
    print("Startup CLI with: %s" % " ".join(cmd_args[1:]))
    subprocess.Popen(cmd_args, cwd="..").wait()

if __name__ == "__main__":
    test_run()
