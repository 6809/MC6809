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


from MC6809.components.cpu_utils.instruction_caller import opcode


class InterruptMixin(object):

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
        if not self.irq_enabled or self.I == 1:
            # log.critical("$%04x *** IRQ, ignore!\t%s" % (
            #     self.program_counter.value, self.get_cc_info()
            # ))
            return

        if self.E:
            self.push_irq_registers()
        else:
            self.push_firq_registers()

        ea = self.memory.read_word(self.IRQ_VECTOR)
        # log.critical("$%04x *** IRQ, set PC to $%04x\t%s" % (
        #     self.program_counter.value, ea, self.get_cc_info()
        # ))
        self.program_counter.set(ea)


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
        self.push_byte(self.system_stack_pointer, self.get_cc_value()) # CC

    def push_firq_registers(self):
        """
        FIRQ - Fast Interrupt Request
        push PC and CC on System stack pointer
        """
        self.cycles += 1
        self.push_word(self.system_stack_pointer, self.program_counter.value) # PC
        self.push_byte(self.system_stack_pointer, self.get_cc_value()) # CC


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
        cc = self.pull_byte(self.system_stack_pointer) # CC
        self.set_cc(cc)
        if self.E:
            self.accu_a.set(
                self.pull_byte(self.system_stack_pointer) # A
            )
            self.accu_b.set(
                self.pull_byte(self.system_stack_pointer) # B
            )
            self.direct_page.set(
                self.pull_byte(self.system_stack_pointer) # DP
            )
            self.index_x.set(
                self.pull_word(self.system_stack_pointer) # X
            )
            self.index_y.set(
                self.pull_word(self.system_stack_pointer) # Y
            )
            self.user_stack_pointer.set(
                self.pull_word(self.system_stack_pointer) # U
            )

        self.program_counter.set(
            self.pull_word(self.system_stack_pointer) # PC
        )
#         log.critical("RTI to $%04x", self.program_counter.value)


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

