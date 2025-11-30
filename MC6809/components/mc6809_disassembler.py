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
    effective_address: int
    op_code: int
    op_args: Sequence[int]
    op_info: dict | None = None

    def __str__(self):
        if self.op_info:
            mnemonic = self.op_info['mnemonic']
        else:
            mnemonic = '???'
        hex_bytes = [self.op_code] + list(self.op_args)
        hex_bytes = ' '.join(f'{b:02X}' for b in hex_bytes)
        if self.op_args:
            op_args = ''.join(f'{b:02X}' for b in self.op_args)
            op_args = f' ${op_args}'
        else:
            op_args = ''
        return f'{self.effective_address:04X}| {hex_bytes:<11} {mnemonic}{op_args}'


def disassemble(assembly: Sequence[int], start_address=0x0):
    pc = 0
    code_len = len(assembly)
    while pc < code_len:
        op_code = assembly[pc]

        if op_code in {0x10, 0x11}:
            # Handle two-byte opcodes
            op_code_len = 2
            try:
                op_code = (op_code << 8) | assembly[pc + 1]
            except KeyError:
                raise RuntimeError('Unexpected end of assembly while reading two-byte opcode')
        else:
            op_code_len = 1

        try:
            op_info = OPCODE_LOOKUP[op_code]
        except KeyError:
            raise RuntimeError(f'Unknown opcode {op_code:02X} at address {pc + start_address:04X}')

        num_bytes = op_info['bytes']
        op_args = assembly[pc + op_code_len: pc + num_bytes]
        yield LineInfo(
            pc=pc,
            effective_address=pc + start_address,
            op_code=op_code,
            op_args=op_args,
            op_info=op_info,
        )
        pc += num_bytes
