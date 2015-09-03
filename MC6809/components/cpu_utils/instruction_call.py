
"""
    This file was generated with: "Instruction_generator.py"
    Please don't change it directly ;)
    

    :copyleft: 2013-2015 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.

"""


from MC6809.components.cpu_utils.instruction_base import InstructionBase

class PrepagedInstructions(InstructionBase):
    def __init__(self, *args, **kwargs):
        super(PrepagedInstructions, self).__init__(*args, **kwargs)

        self.write_byte = self.cpu.memory.write_byte
        self.write_word = self.cpu.memory.write_word

        self.accu_a=self.cpu.accu_a
        self.accu_b=self.cpu.accu_b
        self.accu_d=self.cpu.accu_d
        self.cc_register=self.cpu.cc_register
        self.index_x=self.cpu.index_x
        self.index_y=self.cpu.index_y
        self.system_stack_pointer=self.cpu.system_stack_pointer
        self.user_stack_pointer=self.cpu.user_stack_pointer

        self.get_ea_direct=self.cpu.get_ea_direct
        self.get_ea_extended=self.cpu.get_ea_extended
        self.get_ea_indexed=self.cpu.get_ea_indexed
        self.get_ea_m_direct=self.cpu.get_ea_m_direct
        self.get_ea_m_extended=self.cpu.get_ea_m_extended
        self.get_ea_m_indexed=self.cpu.get_ea_m_indexed
        self.get_ea_relative=self.cpu.get_ea_relative
        self.get_ea_relative_word=self.cpu.get_ea_relative_word
        self.get_m_direct=self.cpu.get_m_direct
        self.get_m_direct_word=self.cpu.get_m_direct_word
        self.get_m_extended=self.cpu.get_m_extended
        self.get_m_extended_word=self.cpu.get_m_extended_word
        self.get_m_immediate=self.cpu.get_m_immediate
        self.get_m_immediate_word=self.cpu.get_m_immediate_word
        self.get_m_indexed=self.cpu.get_m_indexed
        self.get_m_indexed_word=self.cpu.get_m_indexed_word

    def direct_A_read8(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_direct(),
            register=self.accu_a,
        )

    def direct_B_read8(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_direct(),
            register=self.accu_b,
        )

    def direct_read8(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_direct(),
        )

    def direct_ea_A_write8(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_direct(),
            register=self.accu_a,
        )
        self.write_byte(ea, value)

    def direct_ea_B_write8(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_direct(),
            register=self.accu_b,
        )
        self.write_byte(ea, value)

    def direct_ea_D_write16(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_direct(),
            register=self.accu_d,
        )
        self.write_word(ea, value)

    def direct_ea_read8_write8(self, opcode):
        ea, m = self.cpu.get_ea_m_direct()
        ea, value = self.instr_func(
            opcode=opcode,
            ea=ea,
            m=m,
        )
        self.write_byte(ea, value)

    def direct_ea_write8(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_direct(),
        )
        self.write_byte(ea, value)

    def direct_ea(self, opcode):
        self.instr_func(
            opcode=opcode,
            ea=self.get_ea_direct(),
        )

    def direct_ea_S_write16(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_direct(),
            register=self.system_stack_pointer,
        )
        self.write_word(ea, value)

    def direct_ea_U_write16(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_direct(),
            register=self.user_stack_pointer,
        )
        self.write_word(ea, value)

    def direct_ea_X_write16(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_direct(),
            register=self.index_x,
        )
        self.write_word(ea, value)

    def direct_ea_Y_write16(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_direct(),
            register=self.index_y,
        )
        self.write_word(ea, value)

    def direct_word_D_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_direct_word(),
            register=self.accu_d,
        )

    def direct_word_S_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_direct_word(),
            register=self.system_stack_pointer,
        )

    def direct_word_U_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_direct_word(),
            register=self.user_stack_pointer,
        )

    def direct_word_X_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_direct_word(),
            register=self.index_x,
        )

    def direct_word_Y_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_direct_word(),
            register=self.index_y,
        )

    def extended_A_read8(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_extended(),
            register=self.accu_a,
        )

    def extended_B_read8(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_extended(),
            register=self.accu_b,
        )

    def extended_read8(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_extended(),
        )

    def extended_ea_A_write8(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_extended(),
            register=self.accu_a,
        )
        self.write_byte(ea, value)

    def extended_ea_B_write8(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_extended(),
            register=self.accu_b,
        )
        self.write_byte(ea, value)

    def extended_ea_D_write16(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_extended(),
            register=self.accu_d,
        )
        self.write_word(ea, value)

    def extended_ea_read8_write8(self, opcode):
        ea, m = self.cpu.get_ea_m_extended()
        ea, value = self.instr_func(
            opcode=opcode,
            ea=ea,
            m=m,
        )
        self.write_byte(ea, value)

    def extended_ea_write8(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_extended(),
        )
        self.write_byte(ea, value)

    def extended_ea(self, opcode):
        self.instr_func(
            opcode=opcode,
            ea=self.get_ea_extended(),
        )

    def extended_ea_S_write16(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_extended(),
            register=self.system_stack_pointer,
        )
        self.write_word(ea, value)

    def extended_ea_U_write16(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_extended(),
            register=self.user_stack_pointer,
        )
        self.write_word(ea, value)

    def extended_ea_X_write16(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_extended(),
            register=self.index_x,
        )
        self.write_word(ea, value)

    def extended_ea_Y_write16(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_extended(),
            register=self.index_y,
        )
        self.write_word(ea, value)

    def extended_word_D_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_extended_word(),
            register=self.accu_d,
        )

    def extended_word_S_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_extended_word(),
            register=self.system_stack_pointer,
        )

    def extended_word_U_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_extended_word(),
            register=self.user_stack_pointer,
        )

    def extended_word_X_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_extended_word(),
            register=self.index_x,
        )

    def extended_word_Y_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_extended_word(),
            register=self.index_y,
        )

    def immediate_A_read8(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_immediate(),
            register=self.accu_a,
        )

    def immediate_B_read8(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_immediate(),
            register=self.accu_b,
        )

    def immediate_CC_read8(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_immediate(),
            register=self.cc_register,
        )

    def immediate_read8(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_immediate(),
        )

    def immediate_S_read8(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_immediate(),
            register=self.system_stack_pointer,
        )

    def immediate_U_read8(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_immediate(),
            register=self.user_stack_pointer,
        )

    def immediate_word_D_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_immediate_word(),
            register=self.accu_d,
        )

    def immediate_word_S_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_immediate_word(),
            register=self.system_stack_pointer,
        )

    def immediate_word_U_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_immediate_word(),
            register=self.user_stack_pointer,
        )

    def immediate_word_X_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_immediate_word(),
            register=self.index_x,
        )

    def immediate_word_Y_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_immediate_word(),
            register=self.index_y,
        )

    def indexed_A_read8(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_indexed(),
            register=self.accu_a,
        )

    def indexed_B_read8(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_indexed(),
            register=self.accu_b,
        )

    def indexed_read8(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_indexed(),
        )

    def indexed_ea_A_write8(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_indexed(),
            register=self.accu_a,
        )
        self.write_byte(ea, value)

    def indexed_ea_B_write8(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_indexed(),
            register=self.accu_b,
        )
        self.write_byte(ea, value)

    def indexed_ea_D_write16(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_indexed(),
            register=self.accu_d,
        )
        self.write_word(ea, value)

    def indexed_ea_read8_write8(self, opcode):
        ea, m = self.cpu.get_ea_m_indexed()
        ea, value = self.instr_func(
            opcode=opcode,
            ea=ea,
            m=m,
        )
        self.write_byte(ea, value)

    def indexed_ea_write8(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_indexed(),
        )
        self.write_byte(ea, value)

    def indexed_ea(self, opcode):
        self.instr_func(
            opcode=opcode,
            ea=self.get_ea_indexed(),
        )

    def indexed_ea_S_write16(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_indexed(),
            register=self.system_stack_pointer,
        )
        self.write_word(ea, value)

    def indexed_ea_S(self, opcode):
        self.instr_func(
            opcode=opcode,
            ea=self.get_ea_indexed(),
            register=self.system_stack_pointer,
        )

    def indexed_ea_U_write16(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_indexed(),
            register=self.user_stack_pointer,
        )
        self.write_word(ea, value)

    def indexed_ea_U(self, opcode):
        self.instr_func(
            opcode=opcode,
            ea=self.get_ea_indexed(),
            register=self.user_stack_pointer,
        )

    def indexed_ea_X_write16(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_indexed(),
            register=self.index_x,
        )
        self.write_word(ea, value)

    def indexed_ea_X(self, opcode):
        self.instr_func(
            opcode=opcode,
            ea=self.get_ea_indexed(),
            register=self.index_x,
        )

    def indexed_ea_Y_write16(self, opcode):
        ea, value = self.instr_func(
            opcode=opcode,
            ea=self.get_ea_indexed(),
            register=self.index_y,
        )
        self.write_word(ea, value)

    def indexed_ea_Y(self, opcode):
        self.instr_func(
            opcode=opcode,
            ea=self.get_ea_indexed(),
            register=self.index_y,
        )

    def indexed_word_D_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_indexed_word(),
            register=self.accu_d,
        )

    def indexed_word_S_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_indexed_word(),
            register=self.system_stack_pointer,
        )

    def indexed_word_U_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_indexed_word(),
            register=self.user_stack_pointer,
        )

    def indexed_word_X_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_indexed_word(),
            register=self.index_x,
        )

    def indexed_word_Y_read16(self, opcode):
        self.instr_func(
            opcode=opcode,
            m=self.get_m_indexed_word(),
            register=self.index_y,
        )

    def inherent_A(self, opcode):
        self.instr_func(
            opcode=opcode,
            register=self.accu_a,
        )

    def inherent_B(self, opcode):
        self.instr_func(
            opcode=opcode,
            register=self.accu_b,
        )

    def inherent(self, opcode):
        self.instr_func(
            opcode=opcode,
        )

    def relative_ea(self, opcode):
        self.instr_func(
            opcode=opcode,
            ea=self.get_ea_relative(),
        )

    def relative_word_ea(self, opcode):
        self.instr_func(
            opcode=opcode,
            ea=self.get_ea_relative_word(),
        )

