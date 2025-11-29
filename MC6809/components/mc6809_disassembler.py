import dataclasses
from _collections_abc import Sequence

from MC6809.components.MC6809data.MC6809_op_data import OP_DATA


def build_opcode_lookup() -> dict:
    """
    >>> lookup = build_opcode_lookup()
    >>> lookup[0x44] == {'mnemonic': 'LSRA', 'bytes': 1, 'addr_mode': 'INHERENT', 'register': 'A'}
    True
    """
    opcode_lookup = {}
    for instr, data in OP_DATA.items():
        for mnemonic, mnemonic_data in data['mnemonic'].items():
            for op_code, op_data in mnemonic_data['ops'].items():
                op_data = {
                    'mnemonic': mnemonic,
                    'bytes': op_data['bytes'],
                    'addr_mode': op_data['addr_mode'],
                }
                for key, value in mnemonic_data.items():
                    if key == 'ops':
                        continue
                    if value is None or value is False:
                        continue
                    op_data[key] = value
                opcode_lookup[op_code] = op_data
    return opcode_lookup


OPCODE_LOOKUP = build_opcode_lookup()


@dataclasses.dataclass
class LineInfo:
    pc: int
    hex_bytes: str
    op_info: dict | None = None

    def __str__(self):
        if self.op_info:
            mnemonic = self.op_info['mnemonic']
        else:
            mnemonic = '???'
        return f'{self.pc:04X}| {self.hex_bytes:<10} {mnemonic}'


def disassemble(assembly: Sequence[int]):
    pc = 0
    code_len = len(assembly)
    while pc < code_len:
        opcode = assembly[pc]
        try:
            op_info = OPCODE_LOOKUP[opcode]
        except KeyError:
            yield LineInfo(
                pc=pc,
                hex_bytes=f'{assembly[pc]:02X}',
                op_info=None,
            )
            pc += 1
        else:
            instr_bytes = assembly[pc : pc + op_info['bytes']]
            hex_bytes = ' '.join(f'{b:02X}' for b in instr_bytes)
            yield LineInfo(
                pc=pc,
                hex_bytes=hex_bytes,
                op_info=op_info,
            )
            pc += op_info['bytes']
