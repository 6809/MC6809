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


class OpsBranchesMixin:

    # ---- Programm Flow Instructions ----

    @opcode(  # Jump
        0xe, 0x6e, 0x7e,  # JMP (direct, indexed, extended)
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
        self.program_counter.set(ea)

    @opcode(  # Return from subroutine
        0x39,  # RTS (inherent)
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
        self.program_counter.set(ea)

    @opcode(
        # Branch to subroutine:
        0x8d,  # BSR (relative)
        0x17,  # LBSR (relative)
        # Jump to subroutine:
        0x9d, 0xad, 0xbd,  # JSR (direct, indexed, extended)
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
        self.program_counter.set(ea)

    # ---- Branch Instructions ----

    @opcode(  # Branch if equal
        0x27,  # BEQ (relative)
        0x1027,  # LBEQ (relative)
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
        if self.Z == 1:
            #            log.info("$%x BEQ branch to $%x, because Z==1 \t| %s" % (
            #                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
            #            ))
            self.program_counter.set(ea)
#        else:
#            log.debug("$%x BEQ: don't branch to $%x, because Z==0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(  # Branch if greater than or equal (signed)
        0x2c,  # BGE (relative)
        0x102c,  # LBGE (relative)
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
        #    self.N == self.V
        #    (self.N ^ self.V) == 0
        #    not operator.xor(self.N, self.V)
        if self.N == self.V:
            #            log.info("$%x BGE branch to $%x, because N XOR V == 0 \t| %s" % (
            #                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
            #            ))
            self.program_counter.set(ea)
#         else:
#             log.debug("$%x BGE: don't branch to $%x, because N XOR V != 0 \t| %s" % (
#                 self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#             ))

    @opcode(  # Branch if greater (signed)
        0x2e,  # BGT (relative)
        0x102e,  # LBGT (relative)
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
        #    not ((self.N ^ self.V) == 1 or self.Z == 1)
        #    not ((self.N ^ self.V) | self.Z)
        #    self.N == self.V and self.Z == 0
        # ;)
        if not self.Z and self.N == self.V:
            #            log.info("$%x BGT branch to $%x, because (N==V and Z==0) \t| %s" % (
            #                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
            #            ))
            self.program_counter.set(ea)
#         else:
#            log.debug("$%x BGT: don't branch to $%x, because (N==V and Z==0) is False \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(  # Branch if higher (unsigned)
        0x22,  # BHI (relative)
        0x1022,  # LBHI (relative)
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
        if self.C == 0 and self.Z == 0:
            #            log.info("$%x BHI branch to $%x, because C==0 and Z==0 \t| %s" % (
            #                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
            #            ))
            self.program_counter.set(ea)
#         else:
#            log.debug("$%x BHI: don't branch to $%x, because C and Z not 0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(  # Branch if less than or equal (signed)
        0x2f,  # BLE (relative)
        0x102f,  # LBLE (relative)
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
        if (self.N ^ self.V) == 1 or self.Z == 1:
            #            log.info("$%x BLE branch to $%x, because N^V==1 or Z==1 \t| %s" % (
            #                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
            #            ))
            self.program_counter.set(ea)
#         else:
#            log.debug("$%x BLE: don't branch to $%x, because N^V!=1 and Z!=1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(  # Branch if lower or same (unsigned)
        0x23,  # BLS (relative)
        0x1023,  # LBLS (relative)
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
#         if (self.C|self.Z) == 0:
        if self.C == 1 or self.Z == 1:
            #            log.info("$%x BLS branch to $%x, because C|Z==1 \t| %s" % (
            #                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
            #            ))
            self.program_counter.set(ea)
#         else:
#            log.debug("$%x BLS: don't branch to $%x, because C|Z!=1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(  # Branch if less than (signed)
        0x2d,  # BLT (relative)
        0x102d,  # LBLT (relative)
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
        if (self.N ^ self.V) == 1:  # N xor V
            #            log.info("$%x BLT branch to $%x, because N XOR V == 1 \t| %s" % (
            #                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
            #            ))
            self.program_counter.set(ea)
#         else:
#            log.debug("$%x BLT: don't branch to $%x, because N XOR V != 1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(  # Branch if minus
        0x2b,  # BMI (relative)
        0x102b,  # LBMI (relative)
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
        if self.N == 1:
            #            log.info("$%x BMI branch to $%x, because N==1 \t| %s" % (
            #                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
            #            ))
            self.program_counter.set(ea)
#         else:
#            log.debug("$%x BMI: don't branch to $%x, because N==0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(  # Branch if not equal
        0x26,  # BNE (relative)
        0x1026,  # LBNE (relative)
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
        if self.Z == 0:
            #            log.info("$%x BNE branch to $%x, because Z==0 \t| %s" % (
            #                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
            #            ))
            self.program_counter.set(ea)
#        else:
#            log.debug("$%x BNE: don't branch to $%x, because Z==1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(  # Branch if plus
        0x2a,  # BPL (relative)
        0x102a,  # LBPL (relative)
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
        if self.N == 0:
            #            log.info("$%x BPL branch to $%x, because N==0 \t| %s" % (
            #                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
            #            ))
            self.program_counter.set(ea)
#         else:
#            log.debug("$%x BPL: don't branch to $%x, because N==1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(  # Branch always
        0x20,  # BRA (relative)
        0x16,  # LBRA (relative)
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
        self.program_counter.set(ea)

    @opcode(  # Branch never
        0x21,  # BRN (relative)
        0x1021,  # LBRN (relative)
    )
    def instruction_BRN(self, opcode, ea):
        """
        Does not cause a branch. This instruction is essentially a no operation,
        but has a bit pattern logically related to branch always.

        source code forms: BRN dd; LBRN DDDD

        CC bits "HNZVC": -----
        """
        pass

    @opcode(  # Branch if valid twos complement result
        0x28,  # BVC (relative)
        0x1028,  # LBVC (relative)
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
        if self.V == 0:
            #            log.info("$%x BVC branch to $%x, because V==0 \t| %s" % (
            #                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
            #            ))
            self.program_counter.set(ea)
#         else:
#            log.debug("$%x BVC: don't branch to $%x, because V==1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(  # Branch if invalid twos complement result
        0x29,  # BVS (relative)
        0x1029,  # LBVS (relative)
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
        if self.V == 1:
            #            log.info("$%x BVS branch to $%x, because V==1 \t| %s" % (
            #                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
            #            ))
            self.program_counter.set(ea)
#         else:
#            log.debug("$%x BVS: don't branch to $%x, because V==0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(  # Branch if lower (unsigned)
        0x25,  # BLO/BCS (relative)
        0x1025,  # LBLO/LBCS (relative)
    )
    def instruction_BLO(self, opcode, ea):
        """
        CC bits "HNZVC": -----
        case 0x5: cond = REG_CC & CC_C; break; // BCS, BLO, LBCS, LBLO
        """
        if self.C == 1:
            #            log.info("$%x BLO/BCS/LBLO/LBCS branch to $%x, because C==1 \t| %s" % (
            #                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
            #            ))
            self.program_counter.set(ea)
#         else:
#            log.debug("$%x BLO/BCS/LBLO/LBCS: don't branch to $%x, because C==0 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))

    @opcode(  # Branch if lower (unsigned)
        0x24,  # BHS/BCC (relative)
        0x1024,  # LBHS/LBCC (relative)
    )
    def instruction_BHS(self, opcode, ea):
        """
        CC bits "HNZVC": -----
        case 0x4: cond = !(REG_CC & CC_C); break; // BCC, BHS, LBCC, LBHS
        """
        if self.C == 0:
            #            log.info("$%x BHS/BCC/LBHS/LBCC branch to $%x, because C==0 \t| %s" % (
            #                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
            #            ))
            self.program_counter.set(ea)
#        else:
#            log.debug("$%x BHS/BCC/LBHS/LBCC: don't branch to $%x, because C==1 \t| %s" % (
#                self.program_counter, ea, self.cfg.mem_info.get_shortest(ea)
#            ))
