#!/usr/bin/env python3

"""
    MC6809 - 6809 CPU emulator in Python
    =======================================

    :copyleft: 2013-2015 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import os
import sys

from MC6809.components.MC6809data.MC6809_data_utils import MC6809OP_DATA_DICT
from MC6809.components.MC6809data.MC6809_op_data import (
    BYTE,
    OP_DATA,
    REG_A,
    REG_B,
    REG_CC,
    REG_D,
    REG_DP,
    REG_PC,
    REG_S,
    REG_U,
    REG_X,
    REG_Y,
    WORD,
)


SPECIAL_FUNC_NAME = "special"

REGISTER_DICT = {
    REG_X: "index_x",
    REG_Y: "index_y",

    REG_U: "user_stack_pointer",
    REG_S: "system_stack_pointer",

    REG_PC: "program_counter",

    REG_A: "accu_a",
    REG_B: "accu_b",
    REG_D: "accu_d",

    REG_DP: "direct_page",
    REG_CC: "cc_register",

    # undefined_reg.name:"undefined_reg", # for TFR", EXG
}


if __doc__:
    DOC = __doc__.rsplit("=", 1)[1]
else:
    DOC = ""  # e.g.: run with --OO

INIT_CODE = '''
"""
    This file was generated with: "%s"
    Please don't change it directly ;)
    %s
"""


from MC6809.components.cpu_utils.instruction_base import InstructionBase

class PrepagedInstructions(InstructionBase):
    def __init__(self, *args, **kwargs):
        super(PrepagedInstructions, self).__init__(*args, **kwargs)

        self.write_byte = self.cpu.memory.write_byte
        self.write_word = self.cpu.memory.write_word

''' % (os.path.basename(__file__), DOC)


def build_func_name(addr_mode, ea, register, read, write):
    #    print(addr_mode, ea, register, read, write

    if addr_mode is None:
        return SPECIAL_FUNC_NAME

    func_name = addr_mode.lower()

    if ea:
        func_name += "_ea"
    if register:
        func_name += f"_{register}"
    if read:
        func_name += f"_read{read}"
    if write:
        func_name += f"_write{write}"

#    print(func_name
    return func_name


def func_name_from_op_code(op_code):
    op_code_data = MC6809OP_DATA_DICT[op_code]
    addr_mode = op_code_data["addr_mode"]
    ea = op_code_data["needs_ea"]
    register = op_code_data["register"]
    read = op_code_data["read_from_memory"]
    write = op_code_data["write_to_memory"]
    return build_func_name(addr_mode, ea, register, read, write)


def generate_code(f):
    addr_modes = set()
    registers = set()
    variants = set()
    for instr_data in list(OP_DATA.values()):
        for mnemonic, mnemonic_data in list(instr_data["mnemonic"].items()):
            read_from_memory = mnemonic_data["read_from_memory"]
            write_to_memory = mnemonic_data["write_to_memory"]
            needs_ea = mnemonic_data["needs_ea"]
            register = mnemonic_data["register"]
            for op_code, op_data in list(mnemonic_data["ops"].items()):
                addr_mode = op_data["addr_mode"]
#                print(hex(op_code),

                if addr_mode is None:
                    # special function (RESET/ PAGE1,2) defined in InstructionBase
                    print("address mode is None:", mnemonic, op_data)
                    continue

                addr_mode = addr_mode.lower()

                variant = (addr_mode, needs_ea, register, read_from_memory, write_to_memory)
                # print(variant)
                variants.add(variant)

                if needs_ea and read_from_memory:
                    addr_modes.add(f"get_ea_m_{addr_mode}")
                elif needs_ea:
                    addr_modes.add(f"get_ea_{addr_mode}")
                elif read_from_memory:
                    addr_modes.add(f"get_m_{addr_mode}")

                if register is not None:
                    registers.add(register)

#                if (addr_mode and  needs_ea and  register and  read_from_memory and  write_to_memory) is None:

    variants = list(variants)
    variants.sort(key=lambda x: "".join("%s" % i for i in x))

    # for no, data in enumerate(variants):
    #     print(no, data)
    # print("+++++++++++++")

    for line in INIT_CODE.splitlines():
        f.write(f"{line}\n")

    for register in sorted([REGISTER_DICT[register] for register in registers]):
        f.write(
            "        self.{r}=self.cpu.{r}\n".format(
                r=register,
            )
        )
    f.write("\n")

    for addr_mode in sorted(addr_modes):
        f.write(
            "        self.{a}=self.cpu.{a}\n".format(a=addr_mode)
        )
    f.write("\n")

    for addr_mode, needs_ea, register, read_from_memory, write_to_memory in variants:
        func_name = build_func_name(addr_mode, needs_ea, register, read_from_memory, write_to_memory)

        f.write(f"    def {func_name}(self, opcode):\n")

        code = []

        if needs_ea and read_from_memory:
            code.append(f"ea, m = self.cpu.get_ea_m_{addr_mode}()")

        if write_to_memory:
            code.append("ea, value = self.instr_func(")
        else:
            code.append("self.instr_func(")
        code.append("    opcode=opcode,")

        if needs_ea and read_from_memory:
            code.append("    ea=ea,")
            code.append("    m=m,")
        elif needs_ea:
            code.append(f"    ea=self.get_ea_{addr_mode}(),")
        elif read_from_memory:
            code.append(f"    m=self.get_m_{addr_mode}(),")

        if register:
            code.append(
                f"    register=self.{REGISTER_DICT[register]},"
            )

        code.append(")")

        if write_to_memory == BYTE:
            code.append("self.write_byte(ea, value)")
        elif write_to_memory == WORD:
            code.append("self.write_word(ea, value)")

        for line in code:
            f.write(f"        {line}\n")

        f.write("\n")


def generate(filename):
    with open(filename, "w") as f:
        #        generate_code(sys.stdout)
        generate_code(f)
    sys.stderr.write(f"New {filename!r} generated.\n")


if __name__ == "__main__":
    # print("LDA immediate:", func_name_from_op_code(0x96))

    generate("instruction_call.py")
