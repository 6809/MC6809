#!/usr/bin/env python

"""
    MC6809 - 6809 CPU emulator in Python
    =======================================

    :copyleft: 2013-2014 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import inspect

from MC6809.components.cpu6809_trace import InstructionTrace
from MC6809.components.cpu_utils.instruction_call import PrepagedInstructions
from MC6809.components.cpu_utils.Instruction_generator import func_name_from_op_code
from MC6809.components.MC6809data.MC6809_data_utils import MC6809OP_DATA_DICT


def opcode(*opcodes):
    """A decorator for opcodes"""
    def decorator(func):
        setattr(func, "_is_opcode", True)
        setattr(func, "_opcodes", opcodes)
        return func
    return decorator


class OpCollection:
    def __init__(self, cpu):
        self.cpu = cpu
        self.opcode_dict = {}
        self.collect_ops()

    def get_opcode_dict(self):
        return self.opcode_dict

    def collect_ops(self):
        # Get the members not from class instance, so that's possible to
        # exclude properties without "activate" them.
        cls = type(self.cpu)
        for name, cls_method in inspect.getmembers(cls):
            if name.startswith("_") or isinstance(cls_method, property):
                continue

            try:
                opcodes = getattr(cls_method, "_opcodes")
            except AttributeError:
                continue

            instr_func = getattr(self.cpu, name)
            self._add_ops(opcodes, instr_func)

    def _add_ops(self, opcodes, instr_func):
        #         log.debug("%20s: %s" % (
        #             instr_func.__name__, ",".join(["$%x" % c for c in opcodes])
        #         ))
        for op_code in opcodes:
            assert op_code not in self.opcode_dict, \
                f"Opcode ${op_code:x} ({instr_func.__name__}) defined more then one time!"

            op_code_data = MC6809OP_DATA_DICT[op_code]

            func_name = func_name_from_op_code(op_code)

            if self.cpu.cfg.trace:
                InstructionClass = InstructionTrace
            else:
                InstructionClass = PrepagedInstructions

            instrution_class = InstructionClass(self.cpu, instr_func)
            try:
                func = getattr(instrution_class, func_name)
            except AttributeError as err:
                raise AttributeError(f"{err} (op code: ${op_code:02x})")

            self.opcode_dict[op_code] = (op_code_data["cycles"], func)


if __name__ == "__main__":
    from dragonpy.Dragon32.config import Dragon32Cfg

    from MC6809.components.cpu6809 import CPU
    from MC6809.components.memory import Memory
    from MC6809.tests.test_base import BaseCPUTestCase

    cmd_args = BaseCPUTestCase.UNITTEST_CFG_DICT
    cfg = Dragon32Cfg(cmd_args)
    memory = Memory(cfg)
    cpu = CPU(memory, cfg)

    for op_code, data in sorted(cpu.opcode_dict.items()):
        cycles, func = data
        if op_code > 0xff:
            op_code = f"${op_code:04x}"
        else:
            op_code = f"  ${op_code:02x}"

        print(f"Op {op_code} - cycles: {cycles:2d} - func: {func.__name__}")

    print(" --- END --- ")
