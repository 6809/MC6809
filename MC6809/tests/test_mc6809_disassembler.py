import unittest
from types import GeneratorType

from MC6809.components.mc6809_disassembler import OPCODE_LOOKUP, LineInfo, disassemble


def assembly2lines(*assembly) -> list[str]:
    disassembled = disassemble(assembly)
    return [str(line) for line in disassembled]


class TestDisassemble(unittest.TestCase):
    maxDiff = True

    def test_opcode_lookup(self):
        self.assertEqual(
            OPCODE_LOOKUP[0x44],
            {
                'addr_mode': 'INHERENT',
                'bytes': 1,
                'mnemonic': 'LSRA',
                'register': 'A',
            },
        )
        self.assertEqual(
            OPCODE_LOOKUP[0x35],
            {
                'addr_mode': 'IMMEDIATE',
                'bytes': 2,
                'mnemonic': 'PULS',
                'read_from_memory': '8',
                'register': 'S',
            },
        )
        self.assertEqual(
            OPCODE_LOOKUP[0x79],
            {
                'addr_mode': 'EXTENDED',
                'bytes': 3,
                'mnemonic': 'ROL',
                'needs_ea': True,
                'read_from_memory': '8',
                'write_to_memory': '8',
            },
        )

    def test_happy_path(self):
        disassembler = disassemble(
            assembly=[
                0x44,  # 0120|           LSRA             ; shift CRC right, beginning with high word
                0x56,  # 0121|           RORB
                0x1E,
                0x01,  # 0122|           EXG   d,x
                0x46,  # 0124|           RORA             ; low word
                0x56,  # 0125|           RORB
                0x24,
                0x12,  # 0126|           BCC   cl
            ]
        )
        self.assertIsInstance(disassembler, GeneratorType)

        disassembled = list(disassembler)
        self.assertEqual(
            [str(line) for line in disassembled],
            [
                '0000| 44         LSRA',
                '0001| 56         RORB',
                '0002| 1E 01      EXG',
                '0004| 46         RORA',
                '0005| 56         RORB',
                '0006| 24 12      BCC',
            ],
        )
        self.assertEqual(
            disassembled[0],
            LineInfo(
                pc=0,
                hex_bytes='44',
                op_info={
                    'addr_mode': 'INHERENT',
                    'bytes': 1,
                    'mnemonic': 'LSRA',
                    'register': 'A',
                },
            ),
        )

    @unittest.expectedFailure
    def test_puls(self):
        self.assertEqual(
            OPCODE_LOOKUP[0x35],
            {
                'addr_mode': 'IMMEDIATE',
                'bytes': 2,
                'mnemonic': 'PULS',
                'read_from_memory': '8',
                'register': 'S',
            },
        )
        self.assertEqual(
            assembly2lines(0x35, 0x92),
            ['0000| 35 92      PULS A,X,PC'],
        )
