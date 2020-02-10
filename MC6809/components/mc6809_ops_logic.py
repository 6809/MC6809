#!/usr/bin/env python

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


from MC6809.components.cpu_utils.instruction_caller import opcode
from MC6809.utils.bits import get_bit


class OpsLogicalMixin:
    # ---- Logical Operations ----

    @opcode(  # AND memory with accumulator
        0x84, 0x94, 0xa4, 0xb4,  # ANDA (immediate, direct, indexed, extended)
        0xc4, 0xd4, 0xe4, 0xf4,  # ANDB (immediate, direct, indexed, extended)
    )
    def instruction_AND(self, opcode, m, register):
        """
        Performs the logical AND operation between the contents of an
        accumulator and the contents of memory location M and the result is
        stored in the accumulator.

        source code forms: ANDA P; ANDB P

        CC bits "HNZVC": -aa0-
        """
        a = register.value
        r = a & m
        register.set(r)
        self.clear_NZV()
        self.update_NZ_8(r)
#        log.debug("\tAND %s: %i & %i = %i",
#            register.name, a, m, r
#        )

    @opcode(  # Exclusive OR memory with accumulator
        0x88, 0x98, 0xa8, 0xb8,  # EORA (immediate, direct, indexed, extended)
        0xc8, 0xd8, 0xe8, 0xf8,  # EORB (immediate, direct, indexed, extended)
    )
    def instruction_EOR(self, opcode, m, register):
        """
        The contents of memory location M is exclusive ORed into an 8-bit
        register.

        source code forms: EORA P; EORB P

        CC bits "HNZVC": -aa0-
        """
        a = register.value
        r = a ^ m
        register.set(r)
        self.clear_NZV()
        self.update_NZ_8(r)
#        log.debug("\tEOR %s: %i ^ %i = %i",
#            register.name, a, m, r
#        )

    @opcode(  # OR memory with accumulator
        0x8a, 0x9a, 0xaa, 0xba,  # ORA (immediate, direct, indexed, extended)
        0xca, 0xda, 0xea, 0xfa,  # ORB (immediate, direct, indexed, extended)
    )
    def instruction_OR(self, opcode, m, register):
        """
        Performs an inclusive OR operation between the contents of accumulator A
        or B and the contents of memory location M and the result is stored in
        accumulator A or B.

        source code forms: ORA P; ORB P

        CC bits "HNZVC": -aa0-
        """
        a = register.value
        r = a | m
        register.set(r)
        self.clear_NZV()
        self.update_NZ_8(r)
#         log.debug("$%04x OR %s: %02x | %02x = %02x",
#             self.program_counter, register.name, a, m, r
#         )

    # ---- CC manipulation ----

    @opcode(  # AND condition code register
        0x1c,  # ANDCC (immediate)
    )
    def instruction_ANDCC(self, opcode, m, register):
        """
        Performs a logical AND between the condition code register and the
        immediate byte specified in the instruction and places the result in the
        condition code register.

        source code forms: ANDCC #xx

        CC bits "HNZVC": ddddd
        """
        assert register == self.cc_register

        old_cc = self.get_cc_value()
        new_cc = old_cc & m
        self.set_cc(new_cc)
#        log.debug("\tANDCC: $%x AND $%x = $%x | set CC to %s",
#             old_cc, m, new_cc, self.get_cc_info()
#         )

    @opcode(  # OR condition code register
        0x1a,  # ORCC (immediate)
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
        assert register == self.cc_register

        old_cc = self.get_cc_value()
        new_cc = old_cc | m
        self.set_cc(new_cc)
#        log.debug("\tORCC: $%x OR $%x = $%x | set CC to %s",
#             old_cc, m, new_cc, self.get_cc_info()
#         )

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
        self.clear_NZVC()
        self.update_NZVC_8(a, a, r)
        return r

    @opcode(0x8, 0x68, 0x78)  # LSL/ASL (direct, indexed, extended)
    def instruction_LSL_memory(self, opcode, ea, m):
        """
        Logical shift left memory location / Arithmetic shift of memory left
        """
        r = self.LSL(m)
#        log.debug("$%x LSL memory value $%x << 1 = $%x and write it to $%x \t| %s" % (
#            self.program_counter,
#            m, r, ea,
#            self.cfg.mem_info.get_shortest(ea)
#        ))
        return ea, r & 0xff

    @opcode(0x48, 0x58)  # LSLA/ASLA / LSLB/ASLB (inherent)
    def instruction_LSL_register(self, opcode, register):
        """
        Logical shift left accumulator / Arithmetic shift of accumulator
        """
        a = register.value
        r = self.LSL(a)
#        log.debug("$%x LSL %s value $%x << 1 = $%x" % (
#            self.program_counter,
#            register.name, a, r
#        ))
        register.set(r)

    def LSR(self, a):
        """
        Performs a logical shift right on the register. Shifts a zero into bit
        seven and bit zero into the C (carry) bit.

        source code forms: LSR Q; LSRA; LSRB

        CC bits "HNZVC": -0a-s
        """
        r = a >> 1
        self.clear_NZC()
        self.C = get_bit(a, bit=0)  # same as: self.C |= (a & 1)
        self.set_Z8(r)
        return r

    @opcode(0x4, 0x64, 0x74)  # LSR (direct, indexed, extended)
    def instruction_LSR_memory(self, opcode, ea, m):
        """ Logical shift right memory location """
        r = self.LSR(m)
#        log.debug("$%x LSR memory value $%x >> 1 = $%x and write it to $%x \t| %s" % (
#            self.program_counter,
#            m, r, ea,
#            self.cfg.mem_info.get_shortest(ea)
#        ))
        return ea, r & 0xff

    @opcode(0x44, 0x54)  # LSRA / LSRB (inherent)
    def instruction_LSR_register(self, opcode, register):
        """ Logical shift right accumulator """
        a = register.value
        r = self.LSR(a)
#        log.debug("$%x LSR %s value $%x >> 1 = $%x" % (
#            self.program_counter,
#            register.name, a, r
#        ))
        register.set(r)

    def ASR(self, a):
        """
        ASR (Arithmetic Shift Right) alias LSR (Logical Shift Right)

        Shifts all bits of the register one place to the right. Bit seven is held
        constant. Bit zero is shifted into the C (carry) bit.

        source code forms: ASR Q; ASRA; ASRB

        CC bits "HNZVC": uaa-s
        """
        r = (a >> 1) | (a & 0x80)
        self.clear_NZC()
        self.C = get_bit(a, bit=0)  # same as: self.C |= (a & 1)
        self.update_NZ_8(r)
        return r

    @opcode(0x7, 0x67, 0x77)  # ASR (direct, indexed, extended)
    def instruction_ASR_memory(self, opcode, ea, m):
        """ Arithmetic shift memory right """
        r = self.ASR(m)
#        log.debug("$%x ASR memory value $%x >> 1 | Carry = $%x and write it to $%x \t| %s" % (
#            self.program_counter,
#            m, r, ea,
#            self.cfg.mem_info.get_shortest(ea)
#        ))
        return ea, r & 0xff

    @opcode(0x47, 0x57)  # ASRA/ASRB (inherent)
    def instruction_ASR_register(self, opcode, register):
        """ Arithmetic shift accumulator right """
        a = register.value
        r = self.ASR(a)
#        log.debug("$%x ASR %s value $%x >> 1 | Carry = $%x" % (
#            self.program_counter,
#            register.name, a, r
#        ))
        register.set(r)

    # ---- Rotate: ROL, ROR ----

    def ROL(self, a):
        """
        Rotates all bits of the register one place left through the C (carry)
        bit. This is a 9-bit rotation.

        source code forms: ROL Q; ROLA; ROLB

        CC bits "HNZVC": -aaas
        """
        r = (a << 1) | self.C
        self.clear_NZVC()
        self.update_NZVC_8(a, a, r)
        return r

    @opcode(0x9, 0x69, 0x79)  # ROL (direct, indexed, extended)
    def instruction_ROL_memory(self, opcode, ea, m):
        """ Rotate memory left """
        r = self.ROL(m)
#        log.debug("$%x ROL memory value $%x << 1 | Carry = $%x and write it to $%x \t| %s" % (
#            self.program_counter,
#            m, r, ea,
#            self.cfg.mem_info.get_shortest(ea)
#        ))
        return ea, r & 0xff

    @opcode(0x49, 0x59)  # ROLA / ROLB (inherent)
    def instruction_ROL_register(self, opcode, register):
        """ Rotate accumulator left """
        a = register.value
        r = self.ROL(a)
#        log.debug("$%x ROL %s value $%x << 1 | Carry = $%x" % (
#            self.program_counter,
#            register.name, a, r
#        ))
        register.set(r)

    def ROR(self, a):
        """
        Rotates all bits of the register one place right through the C (carry)
        bit. This is a 9-bit rotation.

        moved the carry flag into bit 8
        moved bit 7 into carry flag

        source code forms: ROR Q; RORA; RORB

        CC bits "HNZVC": -aa-s
        """
        r = (a >> 1) | (self.C << 7)
        self.clear_NZ()
        self.update_NZ_8(r)
        self.C = get_bit(a, bit=0)  # same as: self.C = (a & 1)
        return r

    @opcode(0x6, 0x66, 0x76)  # ROR (direct, indexed, extended)
    def instruction_ROR_memory(self, opcode, ea, m):
        """ Rotate memory right """
        r = self.ROR(m)
#        log.debug("$%x ROR memory value $%x >> 1 | Carry = $%x and write it to $%x \t| %s" % (
#            self.program_counter,
#            m, r, ea,
#            self.cfg.mem_info.get_shortest(ea)
#        ))
        return ea, r & 0xff

    @opcode(0x46, 0x56)  # RORA/RORB (inherent)
    def instruction_ROR_register(self, opcode, register):
        """ Rotate accumulator right """
        a = register.value
        r = self.ROR(a)
#        log.debug("$%x ROR %s value $%x >> 1 | Carry = $%x" % (
#            self.program_counter,
#            register.name, a, r
#        ))
        register.set(r)
