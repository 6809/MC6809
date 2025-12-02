import dataclasses
from _collections_abc import Sequence

from MC6809.components.MC6809data.MC6809_op_data import BRANCH_MNEMONICS, EXTENDED, OP_DATA
from MC6809.utils.byte_word_values import bytes2word


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


def iter_opcodes(assembly: Sequence[int], start_address=0x0):
    """
    Parse a sequence of bytes into opcodes and their arguments.
    """
    pc = 0
    code_len = len(assembly)
    while pc < code_len:
        op_code = assembly[pc]

        if op_code in {0x10, 0x11}:
            op_code_len = 2
            try:
                op_code = (op_code << 8) | assembly[pc + 1]
            except IndexError:
                raise RuntimeError('Unknown opcode at end of assembly')
        else:
            op_code_len = 1

        try:
            op_info = OPCODE_LOOKUP[op_code]
        except KeyError:
            raise RuntimeError(
                f'Unknown opcode ${op_code:02X} at address ${start_address + pc:04X} (Position {pc} bytes)'
            )

        num_bytes = op_info['bytes']
        op_args = tuple(assembly[pc + op_code_len : pc + num_bytes])
        yield (pc, op_code, op_info, op_args)
        pc += num_bytes


@dataclasses.dataclass
class LineInfo:
    pc: int
    effective_address: int
    addr_label: str | None
    op_code: int
    op_args: Sequence[int]
    op_args_label: str | None
    op_info: dict | None = None

    def __str__(self):
        if self.op_info:
            mnemonic = self.op_info['mnemonic']
        else:
            mnemonic = '???'
        hex_bytes = [self.op_code] + list(self.op_args)
        hex_bytes = ' '.join(f'{b:02X}' for b in hex_bytes)

        if self.op_args_label:
            op_args = f' {self.op_args_label}'
        elif self.op_args:
            op_args = ''.join(f'{b:02X}' for b in self.op_args)
            op_args = f' ${op_args}'
        else:
            op_args = ''
        addr_label = self.addr_label or ''
        return f'{self.effective_address:04X}| {addr_label:<16}{hex_bytes:<16} {mnemonic}{op_args}'


@dataclasses.dataclass
class Disassembly:
    branch_labels: dict[int, str]
    lines: list[LineInfo]


def iter_disassembly_lines(disassembly: Disassembly, with_header=True):
    branch_labels = disassembly.branch_labels

    if with_header:
        yield ';'
        yield '; Disassembly'
        yield '; ===================='
        address2label = {}
        if not branch_labels:
            yield '; (no branch labels)'
        else:
            for index, (op_args, label) in enumerate(sorted(branch_labels.items())):
                address = bytes2word(op_args)
                address2label[address] = label
                yield f'; {label} = ${address:04X}'
        yield '; ===================='
        yield ';'

    for line_info in disassembly.lines:
        yield str(line_info)


def disassemble(assembly: Sequence[int], start_address=0x0) -> Disassembly:
    parsed = list(iter_opcodes(assembly, start_address))

    branch_addresses = set()
    for pc, op_code, op_info, op_args in parsed:
        mnemonic = op_info['mnemonic']
        if mnemonic in BRANCH_MNEMONICS:
            addr_mode = op_info['addr_mode']

            if addr_mode == EXTENDED:
                branch_addresses.add(op_args)

    address2label = {}
    branch_labels = {}
    for index, op_args in enumerate(sorted(branch_addresses)):
        label = f'LABEL{index:03d}'
        address = bytes2word(op_args)
        address2label[address] = label
        branch_labels[op_args] = label

    lines = []
    for pc, op_code, op_info, op_args in parsed:
        effective_address = pc + start_address
        lines.append(
            LineInfo(
                pc=pc,
                effective_address=effective_address,
                addr_label=address2label.get(effective_address),
                op_code=op_code,
                op_args=op_args,
                op_args_label=branch_labels.get(op_args),
                op_info=op_info,
            )
        )

    return Disassembly(
        branch_labels=branch_labels,
        lines=lines,
    )
