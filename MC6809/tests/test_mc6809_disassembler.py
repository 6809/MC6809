import unittest

from MC6809.components.mc6809_disassembler import (
    OPCODE_LOOKUP,
    Disassembly,
    LineInfo,
    disassemble,
    iter_disassembly_lines,
)


def assembly2lines(*assembly, start_address=0x0, with_header=True) -> list[str]:
    disassembly: Disassembly = disassemble(assembly, start_address=start_address)
    return list(iter_disassembly_lines(disassembly, with_header=with_header))


class TestDisassemble(unittest.TestCase):
    maxDiff = None

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
        self.assertEqual(
            disassemble(assembly=[0x44]),
            Disassembly(
                branch_labels={},
                lines=[
                    LineInfo(
                        pc=0,
                        effective_address=0,
                        addr_label=None,
                        op_code=68,
                        op_args=(),
                        op_args_label=None,
                        op_info={'addr_mode': 'INHERENT', 'bytes': 1, 'mnemonic': 'LSRA', 'register': 'A'},
                    )
                ],
            ),
        )
        self.assertEqual(
            assembly2lines(
                0x44,  # 0120|           LSRA             ; shift CRC right, beginning with high word
                0x56,  # 0121|           RORB
                0x1E,
                0x01,  # 0122|           EXG   d,x
                0x46,  # 0124|           RORA             ; low word
                0x56,  # 0125|           RORB
                0x24,
                0x12,  # 0126|           BCC   cl
            ),
            [
                ';',
                '; Disassembly',
                '; ====================',
                '; (no branch labels)',
                '; ====================',
                ';',
                '0000|                 44               LSRA',
                '0001|                 56               RORB',
                '0002|                 1E 01            EXG $01',
                '0004|                 46               RORA',
                '0005|                 56               RORB',
                '0006|                 24 12            BCC $12',
            ],
        )

    def test_branches1(self):
        """
        org $1000

        loop:
            jsr sub1
            jsr sub2
            jsr loop

        sub1:
            lda #0
            rts

        sub2:
            CMPY #$1234
            rts


        1000:	BD 10 09       	JSR SUB1
        1003:	BD 10 0C       	JSR $100
        1006:	BD 10 00       	JSR LOOP
        1009:	86 00          	LDA #$0
        100B:	39             	RTS
        100C:	10 8C 12 34    	CMPY #$1234
        1010:	39             	RTS
        """
        self.assertEqual(
            assembly2lines(
                0xBD,
                0x10,
                0x09,
                0xBD,
                0x10,
                0x0C,
                0xBD,
                0x10,
                0x00,
                0x86,
                0x00,
                0x39,
                0x10,
                0x8C,
                0x12,
                0x34,
                0x39,
                start_address=0x1000,
            ),
            [
                ';',
                '; Disassembly',
                '; ====================',
                '; LABEL000 = $1000',
                '; LABEL001 = $1009',
                '; LABEL002 = $100C',
                '; ====================',
                ';',
                '1000| LABEL000        BD 10 09         JSR LABEL001',
                '1003|                 BD 10 0C         JSR LABEL002',
                '1006|                 BD 10 00         JSR LABEL000',
                '1009| LABEL001        86 00            LDA $00',
                '100B|                 39               RTS',
                '100C| LABEL002        108C 12 34       CMPY $1234',
                '1010|                 39               RTS',
            ],
        )

    def test_two_bytes_op_codes(self):
        self.assertEqual(
            assembly2lines(0x10, 0x8C, 0x12, 0x34, 0x39, with_header=False),
            [
                '0000|                 108C 12 34       CMPY $1234',
                '0004|                 39               RTS',
            ],
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
            assembly2lines(0x35, 0x92, with_header=False),
            ['0000|                 35 92            PULS A,X,PC']
        )
