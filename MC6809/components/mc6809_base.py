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

import sys
import time
from MC6809.components.mc6809_tools import calc_new_count

if sys.version_info[0] == 3:
    # Python 3
    pass
else:
    # Python 2
    range = xrange

import logging

from MC6809.components.cpu_utils.instruction_caller import opcode

from MC6809.components.cpu_utils.MC6809_registers import (
    ValueStorage8Bit, ConcatenatedAccumulator,
    ValueStorage16Bit, UndefinedRegister,
    convert_differend_width)
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

undefined_reg = UndefinedRegister()





class CPUBase(object):

    SWI3_VECTOR = 0xfff2
    SWI2_VECTOR = 0xfff4
    FIRQ_VECTOR = 0xfff6
    IRQ_VECTOR = 0xfff8
    SWI_VECTOR = 0xfffa
    NMI_VECTOR = 0xfffc
    RESET_VECTOR = 0xfffe

    STARTUP_BURST_COUNT = 100
    min_burst_count = 10 # minimum outer op count per burst
    max_burst_count = 10000 # maximum outer op count per burst

    def __init__(self, memory, cfg):
        self.memory = memory
        self.memory.cpu = self # FIXME
        self.cfg = cfg

        self.running = True
        self.cycles = 0
        self.last_op_address = 0 # Store the current run opcode memory address
        self.outer_burst_op_count = self.STARTUP_BURST_COUNT

        #start_http_control_server(self, cfg) # TODO: Move into seperate Class

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

        super(CPUBase, self).__init__()

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
            REG_CC: self.cc_register,

            undefined_reg.name: undefined_reg, # for TFR, EXG
        }

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
            REG_CC: self.get_cc_value(),

            "cycles": self.cycles,
            "RAM": tuple(self.memory._mem) # copy of array.array() values,
        }

    def set_state(self, state):
        """
        used in unittests
        """
        self.index_x.set(state[REG_X])
        self.index_y.set(state[REG_Y])

        self.user_stack_pointer.set(state[REG_U])
        self.system_stack_pointer.set(state[REG_S])

        self.program_counter.set(state[REG_PC])

        self.accu_a.set(state[REG_A])
        self.accu_b.set(state[REG_B])

        self.direct_page.set(state[REG_DP])
        self.set_cc(state[REG_CC])

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
#             self.set_cc(0xff)
            log.info("\tset CC register to 0x00")
            self.set_cc(0x00)
        else:
#             log.info("\tset cc.F=1: FIRQ interrupt masked")
#             self.F = 1
#
#             log.info("\tset cc.I=1: IRQ interrupt masked")
#             self.I = 1

            log.info("\tset E - 0x80 - bit 7 - Entire register state stacked")
            self.E = 1

#         log.debug("\tset PC to $%x" % self.cfg.RESET_VECTOR)
#         self.program_counter = self.cfg.RESET_VECTOR

        log.info("\tread reset vector from $%04x", self.RESET_VECTOR)
        ea = self.memory.read_word(self.RESET_VECTOR)
        log.info("\tset PC to $%04x" % ea)
        if ea == 0x0000:
            log.critical("Reset vector is $%04x ??? ROM loading in the right place?!?", ea)
        self.program_counter.set(ea)

    ####

    def get_and_call_next_op(self):
        op_address, opcode = self.read_pc_byte()
        # try:
        self.call_instruction_func(op_address, opcode)
        # except Exception as err:
        #     try:
        #         msg = "%s - op address: $%04x - opcode: $%02x" % (err, op_address, opcode)
        #     except TypeError: # e.g: op_address or opcode is None
        #         msg = "%s - op address: %r - opcode: %r" % (err, op_address, opcode)
        #     exception = err.__class__ # Use origin Exception class, e.g.: KeyError
        #     raise exception(msg)

    def quit(self):
        log.critical("CPU quit() called.")
        self.running = False

    def call_instruction_func(self, op_address, opcode):
        self.last_op_address = op_address
        try:
            cycles, instr_func = self.opcode_dict[opcode]
        except KeyError:
            msg = "$%x *** UNKNOWN OP $%x" % (op_address, opcode)
            log.error(msg)
            sys.exit(msg)

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
        self.outer_burst_op_count = calc_new_count(
            min_value=self.min_burst_count,
            value=self.outer_burst_op_count,
            max_value=self.max_burst_count,
            trigger=now() - start_time - self.delay,
            target=max_run_time
        )

    def test_run(self, start, end, max_ops=1000000):
#        log.warning("CPU test_run(): from $%x to $%x" % (start, end))
        self.program_counter.set(start)
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
        self.program_counter.set(start)
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
            self.get_cc_value(),
            self.accu_a.value, self.accu_b.value,
            self.direct_page.value,
            self.index_x.value, self.index_y.value,
            self.user_stack_pointer.value, self.system_stack_pointer.value
        )

    ####


    def read_pc_byte(self):
        op_addr = self.program_counter.value
        m = self.memory.read_byte(op_addr)
        self.program_counter.value += 1
#        log.log(5, "read pc byte: $%02x from $%04x", m, op_addr)
        return op_addr, m

    def read_pc_word(self):
        op_addr = self.program_counter.value
        m = self.memory.read_word(op_addr)
        self.program_counter.value += 2
#        log.log(5, "\tread pc word: $%04x from $%04x", m, op_addr)
        return op_addr, m


    #### Op methods:

    @opcode(
        0x10, # PAGE 2 instructions
        0x11, # PAGE 3 instructions
    )
    def instruction_PAGE(self, opcode):
        """ call op from page 2 or 3 """
        op_address, opcode2 = self.read_pc_byte()
        paged_opcode = opcode * 256 + opcode2
#        log.debug("$%x *** call paged opcode $%x" % (
#            self.program_counter, paged_opcode
#        ))
        self.call_instruction_func(op_address - 1, paged_opcode)

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
        r = a + m + self.C
        register.set(r)
#        log.debug("$%x %02x ADC %s: %i + %i + %i = %i (=$%x)" % (
#            self.program_counter, opcode, register.name,
#            a, m, self.C, r, r
#        ))
        self.clear_HNZVC()
        self.update_HNZVC_8(a, m, r)

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
        register.set(r)
#        log.debug("$%x %02x %02x ADD16 %s: $%02x + $%02x = $%02x" % (
#            self.program_counter, opcode, m,
#            register.name,
#            old, m, r
#        ))
        self.clear_NZVC()
        self.update_NZVC_16(old, m, r)

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
        register.set(r)
#         log.debug("$%x %02x %02x ADD8 %s: $%02x + $%02x = $%02x" % (
#             self.program_counter, opcode, m,
#             register.name,
#             old, m, r
#         ))
        self.clear_HNZVC()
        self.update_HNZVC_8(old, m, r)

    @opcode(0xf, 0x6f, 0x7f) # CLR (direct, indexed, extended)
    def instruction_CLR_memory(self, opcode, ea):
        """
        Clear memory location
        source code forms: CLR
        CC bits "HNZVC": -0100
        """
        self.update_0100()
        return ea, 0x00

    @opcode(0x4f, 0x5f) # CLRA / CLRB (inherent)
    def instruction_CLR_register(self, opcode, register):
        """
        Clear accumulator A or B

        source code forms: CLRA; CLRB
        CC bits "HNZVC": -0100
        """
        register.set(0x00)
        self.update_0100()

    def COM(self, value):
        """
        CC bits "HNZVC": -aa01
        """
        value = ~value # the bits of m inverted
        self.clear_NZ()
        self.update_NZ01_8(value)
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
        register.set(self.COM(value=register.value))
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

        if a_lo > 0x09 or self.H: # cc & 0x20:
            correction_factor |= 0x06

        if a_hi > 0x80 and a_lo > 0x09:
            correction_factor |= 0x60

        if a_hi > 0x90 or self.C: # cc & 0x01:
            correction_factor |= 0x60

        new_value = correction_factor + a
        self.accu_a.set(new_value)

        self.clear_NZ() # V is undefined
        self.update_NZC_8(new_value)

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
        r = a - 1
        self.clear_NZV()
        self.update_NZ_8(r)
        if r == 0x7f:
            self.V = 1
        return r

    @opcode(0xa, 0x6a, 0x7a) # DEC (direct, indexed, extended)
    def instruction_DEC_memory(self, opcode, ea, m):
        """ Decrement memory location """
        r = self.DEC(m)
#        log.debug("$%x DEC memory value $%x -1 = $%x and write it to $%x \t| %s" % (
#            self.program_counter,
#            m, r, ea,
#            self.cfg.mem_info.get_shortest(ea)
#        ))
        return ea, r & 0xff

    @opcode(0x4a, 0x5a) # DECA / DECB (inherent)
    def instruction_DEC_register(self, opcode, register):
        """ Decrement accumulator """
        a = register.value
        r = self.DEC(a)
#        log.debug("$%x DEC %s value $%x -1 = $%x" % (
#            self.program_counter,
#            register.name, a, r
#        ))
        register.set(r)

    def INC(self, a):
        r = a + 1
        self.clear_NZV()
        self.update_NZ_8(r)
        if r == 0x80:
            self.V = 1
        return r

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
        a = register.value
        r = self.INC(a)
        r = register.set(r)

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
        r = self.INC(m)
        return ea, r & 0xff

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
        register.set(ea)

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
        register.set(ea)
        self.Z = 0
        self.set_Z16(ea)

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
        self.accu_d.set(r)
        self.Z = 1 if r == 0 else 0
        self.C = 1 if r & 0x80 else 0

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
        register.set(r)
#        log.debug("$%04x NEG %s $%02x to $%02x" % (
#            self.program_counter, register.name, x, r,
#        ))
        self.clear_NZVC()
        self.update_NZVC_8(0, x, r)

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
        self.clear_NZVC()
        self.update_NZVC_8(0, m, r)
        return ea, r & 0xff

    @opcode(0x12) # NOP (inherent)
    def instruction_NOP(self, opcode):
        """
        No operation

        source code forms: NOP

        CC bits "HNZVC": -----
        """
#        log.debug("\tNOP")


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
        r = a - m - self.C
        register.set(r)
#        log.debug("$%x %02x SBC %s: %i - %i - %i = %i (=$%x)" % (
#            self.program_counter, opcode, register.name,
#            a, m, self.C, r, r
#        ))
        self.clear_NZVC()
        self.update_NZVC_8(a, m, r)

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
        b = self.accu_b.value
        if b & 0x80 == 0:
            self.accu_a.set(0x00)

        d = self.accu_d.value

#        log.debug("SEX: b=$%x ; $%x&0x80=$%x ; d=$%x", b, b, (b & 0x80), d)

        self.clear_NZ()
        self.update_NZ_16(d)



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
        register.set(r_new)
#        log.debug("$%x SUB8 %s: $%x - $%x = $%x (dez.: %i - %i = %i)" % (
#            self.program_counter, register.name,
#            r, m, r_new,
#            r, m, r_new,
#        ))
        self.clear_NZVC()
        if register.WIDTH == 8:
            self.update_NZVC_8(r, m, r_new)
        else:
            assert register.WIDTH == 16
            self.update_NZVC_16(r, m, r_new)


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
        addr_str = self.REGISTER_BIT2STR[addr]
        reg_obj = self.register_str2object[addr_str]
#         log.debug("get register obj: addr: $%x addr_str: %s -> register: %s" % (
#             addr, addr_str, reg_obj.name
#         ))
#         log.debug(repr(self.register_str2object))
        return reg_obj

    def _get_register_and_value(self, addr):
        reg = self._get_register_obj(addr)
        reg_value = reg.value
        return reg, reg_value

    @opcode(0x1f) # TFR (immediate)
    def instruction_TFR(self, opcode, m):
        """
        source code forms: TFR R1, R2
        CC bits "HNZVC": ccccc
        """
        high, low = divmod(m, 16)
        dst_reg = self._get_register_obj(low)
        src_reg = self._get_register_obj(high)
        src_value = convert_differend_width(src_reg, dst_reg)
        dst_reg.set(src_value)
#         log.debug("\tTFR: Set %s to $%x from %s",
#             dst_reg, src_value, src_reg.name
#         )

    @opcode(# Exchange R1 with R2
        0x1e, # EXG (immediate)
    )
    def instruction_EXG(self, opcode, m):
        """
        source code forms: EXG R1,R2
        CC bits "HNZVC": ccccc
        """
        high, low = divmod(m, 0x10)
        reg1 = self._get_register_obj(high)
        reg2 = self._get_register_obj(low)

        new_reg1_value = convert_differend_width(reg2, reg1)
        new_reg2_value = convert_differend_width(reg1, reg2)

        reg1.set(new_reg1_value)
        reg2.set(new_reg2_value)

#         log.debug("\tEXG: %s($%x) <-> %s($%x)",
#             reg1.name, reg1_value, reg2.name, reg2_value
#         )








