#!/usr/bin/env python

"""
    MC6809 - 6809 CPU emulator in Python
    =======================================

    Create trace lines for every OP call.

    :copyleft: 2014 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import logging
import sys

from MC6809.components.cpu_utils.instruction_call import PrepagedInstructions
from MC6809.components.MC6809data.MC6809_data_utils import MC6809OP_DATA_DICT


log = logging.getLogger("DragonPy.cpu6809.trace")


class InstructionTrace(PrepagedInstructions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cfg = self.cpu.cfg
        self.get_mem_info = self.cpu.cfg.mem_info.get_shortest

        self.__origin_instr_func = self.instr_func
        self.instr_func = self.__call_instr_func

#    def __getattribute__(self, attr, *args, **kwargs):
#        if attr not in ("__call", "cpu", "memory", "instr_func"):
#            return InstructionTrace.__call
#            print attr, args, kwargs
#        return PrepagedInstructions.__getattribute__(self, attr, *args, **kwargs)
#
#    def __call(self, func, *args, **kwargs):
#        print func, args, kwargs
#        raise

    def __call_instr_func(self, opcode, *args, **kwargs):
        # call the op CPU code method
        result = self.__origin_instr_func(opcode, *args, **kwargs)

        if opcode in (0x10, 0x11):
            log.debug("Skip PAGE 2 and PAGE 3 instruction in trace")
            return

        op_code_data = MC6809OP_DATA_DICT[opcode]

        op_address = self.cpu.last_op_address

        ob_bytes = op_code_data["bytes"]

        op_bytes = "".join(
            f"{value:02x}"
            for __, value in self.cpu.memory.iter_bytes(op_address, op_address + ob_bytes)
        )

        kwargs_info = []
        if "register" in kwargs:
            kwargs_info.append(str(kwargs["register"]))
        if "ea" in kwargs:
            kwargs_info.append(f"ea:{kwargs['ea']:04x}")
        if "m" in kwargs:
            kwargs_info.append(f"m:{kwargs['m']:x}")

        msg = "{op_address:04x}| {op_bytes:<11} {mnemonic:<7} {kwargs:<19} {cpu} | {cc} | {mem}\n".format(
            op_address=op_address,
            op_bytes=op_bytes,
            mnemonic=op_code_data["mnemonic"],
            kwargs=" ".join(kwargs_info),
            cpu=self.cpu.get_info,
            cc=self.cpu.get_cc_info(),
            mem=self.get_mem_info(op_address)
        )
        sys.stdout.write(msg)

        if not op_bytes.startswith(f"{opcode:02x}"):
            self.cpu.memory.print_dump(op_address, op_address + ob_bytes)
            self.cpu.memory.print_dump(op_address - 10, op_address + ob_bytes + 10)
        assert op_bytes.startswith(f"{opcode:02x}"), f"{op_bytes} doesn't start with {self.opcode:02x}"

        return result


# ------------------------------------------------------------------------------


def test_run():
    import os
    import subprocess
    import sys
    cmd_args = [
        sys.executable,
        os.path.join("..", "DragonPy_CLI.py"),
        #        "--verbosity", " 1", # hardcode DEBUG ;)
        #        "--verbosity", "10", # DEBUG
        #        "--verbosity", "20", # INFO
        #        "--verbosity", "30", # WARNING
        #         "--verbosity", "40", # ERROR
        "--verbosity", "50",  # CRITICAL/FATAL
        "--machine", "Dragon32", "run",
        #        "--machine", "Vectrex", "run",
        #        "--max_ops", "1",
        "--trace",
    ]
    print(f"Startup CLI with: {' '.join(cmd_args[1:])}")
    subprocess.Popen(cmd_args, cwd="..").wait()


if __name__ == "__main__":
    test_run()
