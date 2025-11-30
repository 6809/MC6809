#!/usr/bin/env python

"""
    6809 instruction set data
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    merged data from:
        * http://www.maddes.net/m6809pm/sections.htm#sec4_4
        * http://www.burgins.com/m6809.html
        * http://www.maddes.net/m6809pm/appendix_a.htm#appA

    Note:
    * read_from_memory: it's "excluded" the address modes routines.
        So if the address mode will fetch the memory to get the
        effective address, but the content of the memory is not needed in
        the instruction them self, the read_from_memory must be set to False.

    Generated data is online here:
    https://docs.google.com/spreadsheet/ccc?key=0Alhtym6D6yKjdFBtNmF0UVR5OW05S3psaURnUTNtSFE

    :copyleft: 2013-2014 by Jens Diemer
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


BYTE = "8"
WORD = "16"


# Address modes:
DIRECT = "DIRECT"
DIRECT_WORD = "DIRECT_WORD"
EXTENDED = "EXTENDED"
EXTENDED_WORD = "EXTENDED_WORD"
IMMEDIATE = "IMMEDIATE"
IMMEDIATE_WORD = "IMMEDIATE_WORD"
INDEXED = "INDEXED"
INDEXED_WORD = "INDEXED_WORD"
INHERENT = "INHERENT"
RELATIVE = "RELATIVE"
RELATIVE_WORD = "RELATIVE_WORD"


# Registers:
REG_A = "A"
REG_B = "B"
REG_CC = "CC"
REG_D = "D"
REG_DP = "DP"
REG_PC = "PC"
REG_S = "S"
REG_U = "U"
REG_X = "X"
REG_Y = "Y"


BRANCH_MNEMONICS = frozenset(
    {
        'BRA',
        'BSR',
        'BEQ',
        'BNE',
        'BPL',
        'BMI',
        'BGE',
        'BLT',
        'BGT',
        'BLE',
        'BHI',
        'BLS',
        'BCC',
        'BVC',
        'BVS',
        'LBRA',
        'LBSR',
        'LBEQ',
        'LBNE',
        'LBPL',
        'LBMI',
        'LBGE',
        'LBLT',
        'LBGT',
        'LBLE',
        'LBHI',
        'LBLS',
        'LBCC',
        'LBCS',
        'LBVC',
        'LBVS',
        'JMP',
        'JSR',
    }
)


OP_DATA = {
    'ABX': {
        'mnemonic': {
            'ABX': {
                'needs_ea': False,
                'ops': {0x3A: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            }
        }
    },
    'ADC': {
        'mnemonic': {
            'ADCA': {
                'needs_ea': False,
                'ops': {
                    0x89: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0x99: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xA9: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xB9: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_A,
                'write_to_memory': None,
            },
            'ADCB': {
                'needs_ea': False,
                'ops': {
                    0xC9: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0xD9: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xE9: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xF9: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_B,
                'write_to_memory': None,
            },
        }
    },
    'ADD': {
        'mnemonic': {
            'ADDA': {
                'needs_ea': False,
                'ops': {
                    0x8B: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0x9B: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xAB: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xBB: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_A,
                'write_to_memory': None,
            },
            'ADDB': {
                'needs_ea': False,
                'ops': {
                    0xCB: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0xDB: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xEB: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xFB: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_B,
                'write_to_memory': None,
            },
            'ADDD': {
                'needs_ea': False,
                'ops': {
                    0xC3: {'addr_mode': IMMEDIATE_WORD, 'bytes': 3, 'cycles': 4},
                    0xD3: {'addr_mode': DIRECT_WORD, 'bytes': 2, 'cycles': 6},
                    0xE3: {'addr_mode': INDEXED_WORD, 'bytes': 2, 'cycles': 6},
                    0xF3: {'addr_mode': EXTENDED_WORD, 'bytes': 3, 'cycles': 7},
                },
                'read_from_memory': WORD,
                'register': REG_D,
                'write_to_memory': None,
            },
        }
    },
    'AND': {
        'mnemonic': {
            'ANDA': {
                'needs_ea': False,
                'ops': {
                    0x84: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0x94: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xA4: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xB4: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_A,
                'write_to_memory': None,
            },
            'ANDB': {
                'needs_ea': False,
                'ops': {
                    0xC4: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0xD4: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xE4: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xF4: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_B,
                'write_to_memory': None,
            },
            'ANDCC': {
                'needs_ea': False,
                'ops': {0x1C: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': BYTE,
                'register': REG_CC,
                'write_to_memory': None,
            },
        }
    },
    'ASR': {
        'mnemonic': {
            'ASR': {
                'needs_ea': True,
                'ops': {
                    0x07: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 6},
                    0x67: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 6},
                    0x77: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 7},
                },
                'read_from_memory': BYTE,
                'register': None,
                'write_to_memory': BYTE,
            },
            'ASRA': {
                'needs_ea': False,
                'ops': {0x47: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_A,
                'write_to_memory': None,
            },
            'ASRB': {
                'needs_ea': False,
                'ops': {0x57: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_B,
                'write_to_memory': None,
            },
        }
    },
    'BEQ': {
        'mnemonic': {
            'BEQ': {
                'needs_ea': True,
                'ops': {0x27: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBEQ': {
                'needs_ea': True,
                'ops': {0x1027: {'addr_mode': RELATIVE_WORD, 'bytes': 4, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BGE': {
        'mnemonic': {
            'BGE': {
                'needs_ea': True,
                'ops': {0x2C: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBGE': {
                'needs_ea': True,
                'ops': {0x102C: {'addr_mode': RELATIVE_WORD, 'bytes': 4, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BGT': {
        'mnemonic': {
            'BGT': {
                'needs_ea': True,
                'ops': {0x2E: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBGT': {
                'needs_ea': True,
                'ops': {0x102E: {'addr_mode': RELATIVE_WORD, 'bytes': 4, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BHI': {
        'mnemonic': {
            'BHI': {
                'needs_ea': True,
                'ops': {0x22: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBHI': {
                'needs_ea': True,
                'ops': {0x1022: {'addr_mode': RELATIVE_WORD, 'bytes': 4, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BHS': {
        'mnemonic': {
            'BCC': {
                'needs_ea': True,
                'ops': {0x24: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBCC': {
                'needs_ea': True,
                'ops': {0x1024: {'addr_mode': RELATIVE_WORD, 'bytes': 4, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BIT': {
        'mnemonic': {
            'BITA': {
                'needs_ea': False,
                'ops': {
                    0x85: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0x95: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xA5: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xB5: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_A,
                'write_to_memory': None,
            },
            'BITB': {
                'needs_ea': False,
                'ops': {
                    0xC5: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0xD5: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xE5: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xF5: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_B,
                'write_to_memory': None,
            },
        }
    },
    'BLE': {
        'mnemonic': {
            'BLE': {
                'needs_ea': True,
                'ops': {0x2F: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBLE': {
                'needs_ea': True,
                'ops': {0x102F: {'addr_mode': RELATIVE_WORD, 'bytes': 4, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BLO': {
        'mnemonic': {
            'BLO': {
                'needs_ea': True,
                'ops': {0x25: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBCS': {
                'needs_ea': True,
                'ops': {0x1025: {'addr_mode': RELATIVE_WORD, 'bytes': 4, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BLS': {
        'mnemonic': {
            'BLS': {
                'needs_ea': True,
                'ops': {0x23: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBLS': {
                'needs_ea': True,
                'ops': {0x1023: {'addr_mode': RELATIVE_WORD, 'bytes': 4, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BLT': {
        'mnemonic': {
            'BLT': {
                'needs_ea': True,
                'ops': {0x2D: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBLT': {
                'needs_ea': True,
                'ops': {0x102D: {'addr_mode': RELATIVE_WORD, 'bytes': 4, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BMI': {
        'mnemonic': {
            'BMI': {
                'needs_ea': True,
                'ops': {0x2B: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBMI': {
                'needs_ea': True,
                'ops': {0x102B: {'addr_mode': RELATIVE_WORD, 'bytes': 4, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BNE': {
        'mnemonic': {
            'BNE': {
                'needs_ea': True,
                'ops': {0x26: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBNE': {
                'needs_ea': True,
                'ops': {0x1026: {'addr_mode': RELATIVE_WORD, 'bytes': 4, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BPL': {
        'mnemonic': {
            'BPL': {
                'needs_ea': True,
                'ops': {0x2A: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBPL': {
                'needs_ea': True,
                'ops': {0x102A: {'addr_mode': RELATIVE_WORD, 'bytes': 4, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BRA': {
        'mnemonic': {
            'BRA': {
                'needs_ea': True,
                'ops': {0x20: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBRA': {
                'needs_ea': True,
                'ops': {0x16: {'addr_mode': RELATIVE_WORD, 'bytes': 3, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BRN': {
        'mnemonic': {
            'BRN': {
                'needs_ea': True,
                'ops': {0x21: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBRN': {
                'needs_ea': True,
                'ops': {0x1021: {'addr_mode': RELATIVE_WORD, 'bytes': 4, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BSR': {
        'mnemonic': {
            'BSR': {
                'needs_ea': True,
                'ops': {0x8D: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 7}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBSR': {
                'needs_ea': True,
                'ops': {0x17: {'addr_mode': RELATIVE_WORD, 'bytes': 3, 'cycles': 9}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BVC': {
        'mnemonic': {
            'BVC': {
                'needs_ea': True,
                'ops': {0x28: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBVC': {
                'needs_ea': True,
                'ops': {0x1028: {'addr_mode': RELATIVE_WORD, 'bytes': 4, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'BVS': {
        'mnemonic': {
            'BVS': {
                'needs_ea': True,
                'ops': {0x29: {'addr_mode': RELATIVE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'LBVS': {
                'needs_ea': True,
                'ops': {0x1029: {'addr_mode': RELATIVE_WORD, 'bytes': 4, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'CLR': {
        'mnemonic': {
            'CLR': {
                'needs_ea': True,
                'ops': {
                    0x0F: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 6},
                    0x6F: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 6},
                    0x7F: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 7},
                },
                'read_from_memory': None,
                'register': None,
                'write_to_memory': BYTE,
            },
            'CLRA': {
                'needs_ea': False,
                'ops': {0x4F: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_A,
                'write_to_memory': None,
            },
            'CLRB': {
                'needs_ea': False,
                'ops': {0x5F: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_B,
                'write_to_memory': None,
            },
        }
    },
    'CMP': {
        'mnemonic': {
            'CMPA': {
                'needs_ea': False,
                'ops': {
                    0x81: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0x91: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xA1: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xB1: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_A,
                'write_to_memory': None,
            },
            'CMPB': {
                'needs_ea': False,
                'ops': {
                    0xC1: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0xD1: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xE1: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xF1: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_B,
                'write_to_memory': None,
            },
            'CMPD': {
                'needs_ea': False,
                'ops': {
                    0x1083: {'addr_mode': IMMEDIATE_WORD, 'bytes': 4, 'cycles': 5},
                    0x1093: {'addr_mode': DIRECT_WORD, 'bytes': 3, 'cycles': 7},
                    0x10A3: {'addr_mode': INDEXED_WORD, 'bytes': 3, 'cycles': 7},
                    0x10B3: {'addr_mode': EXTENDED_WORD, 'bytes': 4, 'cycles': 8},
                },
                'read_from_memory': WORD,
                'register': REG_D,
                'write_to_memory': None,
            },
            'CMPS': {
                'needs_ea': False,
                'ops': {
                    0x118C: {'addr_mode': IMMEDIATE_WORD, 'bytes': 4, 'cycles': 5},
                    0x119C: {'addr_mode': DIRECT_WORD, 'bytes': 3, 'cycles': 7},
                    0x11AC: {'addr_mode': INDEXED_WORD, 'bytes': 3, 'cycles': 7},
                    0x11BC: {'addr_mode': EXTENDED_WORD, 'bytes': 4, 'cycles': 8},
                },
                'read_from_memory': WORD,
                'register': REG_S,
                'write_to_memory': None,
            },
            'CMPU': {
                'needs_ea': False,
                'ops': {
                    0x1183: {'addr_mode': IMMEDIATE_WORD, 'bytes': 4, 'cycles': 5},
                    0x1193: {'addr_mode': DIRECT_WORD, 'bytes': 3, 'cycles': 7},
                    0x11A3: {'addr_mode': INDEXED_WORD, 'bytes': 3, 'cycles': 7},
                    0x11B3: {'addr_mode': EXTENDED_WORD, 'bytes': 4, 'cycles': 8},
                },
                'read_from_memory': WORD,
                'register': REG_U,
                'write_to_memory': None,
            },
            'CMPX': {
                'needs_ea': False,
                'ops': {
                    0x8C: {'addr_mode': IMMEDIATE_WORD, 'bytes': 3, 'cycles': 4},
                    0x9C: {'addr_mode': DIRECT_WORD, 'bytes': 2, 'cycles': 6},
                    0xAC: {'addr_mode': INDEXED_WORD, 'bytes': 2, 'cycles': 6},
                    0xBC: {'addr_mode': EXTENDED_WORD, 'bytes': 3, 'cycles': 7},
                },
                'read_from_memory': WORD,
                'register': REG_X,
                'write_to_memory': None,
            },
            'CMPY': {
                'needs_ea': False,
                'ops': {
                    0x108C: {'addr_mode': IMMEDIATE_WORD, 'bytes': 4, 'cycles': 5},
                    0x109C: {'addr_mode': DIRECT_WORD, 'bytes': 3, 'cycles': 7},
                    0x10AC: {'addr_mode': INDEXED_WORD, 'bytes': 3, 'cycles': 7},
                    0x10BC: {'addr_mode': EXTENDED_WORD, 'bytes': 4, 'cycles': 8},
                },
                'read_from_memory': WORD,
                'register': REG_Y,
                'write_to_memory': None,
            },
        }
    },
    'COM': {
        'mnemonic': {
            'COM': {
                'needs_ea': True,
                'ops': {
                    0x03: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 6},
                    0x63: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 6},
                    0x73: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 7},
                },
                'read_from_memory': BYTE,
                'register': None,
                'write_to_memory': BYTE,
            },
            'COMA': {
                'needs_ea': False,
                'ops': {0x43: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_A,
                'write_to_memory': None,
            },
            'COMB': {
                'needs_ea': False,
                'ops': {0x53: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_B,
                'write_to_memory': None,
            },
        }
    },
    'CWAI': {
        'mnemonic': {
            'CWAI': {
                'needs_ea': False,
                'ops': {0x3C: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 21}},
                'read_from_memory': BYTE,
                'register': None,
                'write_to_memory': None,
            }
        }
    },
    'DAA': {
        'mnemonic': {
            'DAA': {
                'needs_ea': False,
                'ops': {0x19: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            }
        }
    },
    'DEC': {
        'mnemonic': {
            'DEC': {
                'needs_ea': True,
                'ops': {
                    0x0A: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 6},
                    0x6A: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 6},
                    0x7A: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 7},
                },
                'read_from_memory': BYTE,
                'register': None,
                'write_to_memory': BYTE,
            },
            'DECA': {
                'needs_ea': False,
                'ops': {0x4A: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_A,
                'write_to_memory': None,
            },
            'DECB': {
                'needs_ea': False,
                'ops': {0x5A: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_B,
                'write_to_memory': None,
            },
        }
    },
    'EOR': {
        'mnemonic': {
            'EORA': {
                'needs_ea': False,
                'ops': {
                    0x88: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0x98: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xA8: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xB8: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_A,
                'write_to_memory': None,
            },
            'EORB': {
                'needs_ea': False,
                'ops': {
                    0xC8: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0xD8: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xE8: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xF8: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_B,
                'write_to_memory': None,
            },
        }
    },
    'EXG': {
        'mnemonic': {
            'EXG': {
                'needs_ea': False,
                'ops': {0x1E: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 8}},
                'read_from_memory': BYTE,
                'register': None,
                'write_to_memory': None,
            }
        }
    },
    'INC': {
        'mnemonic': {
            'INC': {
                'needs_ea': True,
                'ops': {
                    0x0C: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 6},
                    0x6C: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 6},
                    0x7C: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 7},
                },
                'read_from_memory': BYTE,
                'register': None,
                'write_to_memory': BYTE,
            },
            'INCA': {
                'needs_ea': False,
                'ops': {0x4C: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_A,
                'write_to_memory': None,
            },
            'INCB': {
                'needs_ea': False,
                'ops': {0x5C: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_B,
                'write_to_memory': None,
            },
        }
    },
    'JMP': {
        'mnemonic': {
            'JMP': {
                'needs_ea': True,
                'ops': {
                    0x0E: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 3},
                    0x6E: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 3},
                    0x7E: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 3},
                },
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            }
        }
    },
    'JSR': {
        'mnemonic': {
            'JSR': {
                'needs_ea': True,
                'ops': {
                    0x9D: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 7},
                    0xAD: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 7},
                    0xBD: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 8},
                },
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            }
        }
    },
    'LD': {
        'mnemonic': {
            'LDA': {
                'needs_ea': False,
                'ops': {
                    0x86: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0x96: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xA6: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xB6: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_A,
                'write_to_memory': None,
            },
            'LDB': {
                'needs_ea': False,
                'ops': {
                    0xC6: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0xD6: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xE6: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xF6: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_B,
                'write_to_memory': None,
            },
            'LDD': {
                'needs_ea': False,
                'ops': {
                    0xCC: {'addr_mode': IMMEDIATE_WORD, 'bytes': 3, 'cycles': 3},
                    0xDC: {'addr_mode': DIRECT_WORD, 'bytes': 2, 'cycles': 5},
                    0xEC: {'addr_mode': INDEXED_WORD, 'bytes': 2, 'cycles': 5},
                    0xFC: {'addr_mode': EXTENDED_WORD, 'bytes': 3, 'cycles': 6},
                },
                'read_from_memory': WORD,
                'register': REG_D,
                'write_to_memory': None,
            },
            'LDS': {
                'needs_ea': False,
                'ops': {
                    0x10CE: {'addr_mode': IMMEDIATE_WORD, 'bytes': 4, 'cycles': 4},
                    0x10DE: {'addr_mode': DIRECT_WORD, 'bytes': 3, 'cycles': 6},
                    0x10EE: {'addr_mode': INDEXED_WORD, 'bytes': 3, 'cycles': 6},
                    0x10FE: {'addr_mode': EXTENDED_WORD, 'bytes': 4, 'cycles': 7},
                },
                'read_from_memory': WORD,
                'register': REG_S,
                'write_to_memory': None,
            },
            'LDU': {
                'needs_ea': False,
                'ops': {
                    0xCE: {'addr_mode': IMMEDIATE_WORD, 'bytes': 3, 'cycles': 3},
                    0xDE: {'addr_mode': DIRECT_WORD, 'bytes': 2, 'cycles': 5},
                    0xEE: {'addr_mode': INDEXED_WORD, 'bytes': 2, 'cycles': 5},
                    0xFE: {'addr_mode': EXTENDED_WORD, 'bytes': 3, 'cycles': 6},
                },
                'read_from_memory': WORD,
                'register': REG_U,
                'write_to_memory': None,
            },
            'LDX': {
                'needs_ea': False,
                'ops': {
                    0x8E: {'addr_mode': IMMEDIATE_WORD, 'bytes': 3, 'cycles': 3},
                    0x9E: {'addr_mode': DIRECT_WORD, 'bytes': 2, 'cycles': 5},
                    0xAE: {'addr_mode': INDEXED_WORD, 'bytes': 2, 'cycles': 5},
                    0xBE: {'addr_mode': EXTENDED_WORD, 'bytes': 3, 'cycles': 6},
                },
                'read_from_memory': WORD,
                'register': REG_X,
                'write_to_memory': None,
            },
            'LDY': {
                'needs_ea': False,
                'ops': {
                    0x108E: {'addr_mode': IMMEDIATE_WORD, 'bytes': 4, 'cycles': 4},
                    0x109E: {'addr_mode': DIRECT_WORD, 'bytes': 3, 'cycles': 6},
                    0x10AE: {'addr_mode': INDEXED_WORD, 'bytes': 3, 'cycles': 6},
                    0x10BE: {'addr_mode': EXTENDED_WORD, 'bytes': 4, 'cycles': 7},
                },
                'read_from_memory': WORD,
                'register': REG_Y,
                'write_to_memory': None,
            },
        }
    },
    'LEA': {
        'mnemonic': {
            'LEAS': {
                'needs_ea': True,
                'ops': {0x32: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4}},
                'read_from_memory': None,
                'register': REG_S,
                'write_to_memory': None,
            },
            'LEAU': {
                'needs_ea': True,
                'ops': {0x33: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4}},
                'read_from_memory': None,
                'register': REG_U,
                'write_to_memory': None,
            },
            'LEAX': {
                'needs_ea': True,
                'ops': {0x30: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4}},
                'read_from_memory': None,
                'register': REG_X,
                'write_to_memory': None,
            },
            'LEAY': {
                'needs_ea': True,
                'ops': {0x31: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4}},
                'read_from_memory': None,
                'register': REG_Y,
                'write_to_memory': None,
            },
        }
    },
    'LSL': {
        'mnemonic': {
            'LSL': {
                'needs_ea': True,
                'ops': {
                    0x08: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 6},
                    0x68: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 6},
                    0x78: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 7},
                },
                'read_from_memory': BYTE,
                'register': None,
                'write_to_memory': BYTE,
            },
            'LSLA': {
                'needs_ea': False,
                'ops': {0x48: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_A,
                'write_to_memory': None,
            },
            'LSLB': {
                'needs_ea': False,
                'ops': {0x58: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_B,
                'write_to_memory': None,
            },
        }
    },
    'LSR': {
        'mnemonic': {
            'LSR': {
                'needs_ea': True,
                'ops': {
                    0x04: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 6},
                    0x64: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 6},
                    0x74: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 7},
                },
                'read_from_memory': BYTE,
                'register': None,
                'write_to_memory': BYTE,
            },
            'LSRA': {
                'needs_ea': False,
                'ops': {0x44: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_A,
                'write_to_memory': None,
            },
            'LSRB': {
                'needs_ea': False,
                'ops': {0x54: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_B,
                'write_to_memory': None,
            },
        }
    },
    'MUL': {
        'mnemonic': {
            'MUL': {
                'needs_ea': False,
                'ops': {0x3D: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 11}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            }
        }
    },
    'NEG': {
        'mnemonic': {
            'NEG': {
                'needs_ea': True,
                'ops': {
                    0x00: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 6},
                    0x60: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 6},
                    0x70: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 7},
                },
                'read_from_memory': BYTE,
                'register': None,
                'write_to_memory': BYTE,
            },
            'NEGA': {
                'needs_ea': False,
                'ops': {0x40: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_A,
                'write_to_memory': None,
            },
            'NEGB': {
                'needs_ea': False,
                'ops': {0x50: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_B,
                'write_to_memory': None,
            },
        }
    },
    'NOP': {
        'mnemonic': {
            'NOP': {
                'needs_ea': False,
                'ops': {0x12: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            }
        }
    },
    'OR': {
        'mnemonic': {
            'ORA': {
                'needs_ea': False,
                'ops': {
                    0x8A: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0x9A: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xAA: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xBA: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_A,
                'write_to_memory': None,
            },
            'ORB': {
                'needs_ea': False,
                'ops': {
                    0xCA: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0xDA: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xEA: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xFA: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_B,
                'write_to_memory': None,
            },
            'ORCC': {
                'needs_ea': False,
                'ops': {0x1A: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 3}},
                'read_from_memory': BYTE,
                'register': REG_CC,
                'write_to_memory': None,
            },
        }
    },
    'PAGE': {
        'mnemonic': {
            'PAGE 1': {
                'needs_ea': False,
                'ops': {0x10: {'addr_mode': None, 'bytes': 1, 'cycles': 1}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'PAGE 2': {
                'needs_ea': False,
                'ops': {0x11: {'addr_mode': None, 'bytes': 1, 'cycles': 1}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'PSH': {
        'mnemonic': {
            'PSHS': {
                'needs_ea': False,
                'ops': {0x34: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 5}},
                'read_from_memory': BYTE,
                'register': REG_S,
                'write_to_memory': None,
            },
            'PSHU': {
                'needs_ea': False,
                'ops': {0x36: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 5}},
                'read_from_memory': BYTE,
                'register': REG_U,
                'write_to_memory': None,
            },
        }
    },
    'PUL': {
        'mnemonic': {
            'PULS': {
                'needs_ea': False,
                'ops': {0x35: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 5}},
                'read_from_memory': BYTE,
                'register': REG_S,
                'write_to_memory': None,
            },
            'PULU': {
                'needs_ea': False,
                'ops': {0x37: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 5}},
                'read_from_memory': BYTE,
                'register': REG_U,
                'write_to_memory': None,
            },
        }
    },
    'RESET': {
        'mnemonic': {
            'RESET': {
                'needs_ea': False,
                'ops': {0x3E: {'addr_mode': None, 'bytes': 1, 'cycles': -1}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            }
        }
    },
    'ROL': {
        'mnemonic': {
            'ROL': {
                'needs_ea': True,
                'ops': {
                    0x09: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 6},
                    0x69: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 6},
                    0x79: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 7},
                },
                'read_from_memory': BYTE,
                'register': None,
                'write_to_memory': BYTE,
            },
            'ROLA': {
                'needs_ea': False,
                'ops': {0x49: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_A,
                'write_to_memory': None,
            },
            'ROLB': {
                'needs_ea': False,
                'ops': {0x59: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_B,
                'write_to_memory': None,
            },
        }
    },
    'ROR': {
        'mnemonic': {
            'ROR': {
                'needs_ea': True,
                'ops': {
                    0x06: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 6},
                    0x66: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 6},
                    0x76: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 7},
                },
                'read_from_memory': BYTE,
                'register': None,
                'write_to_memory': BYTE,
            },
            'RORA': {
                'needs_ea': False,
                'ops': {0x46: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_A,
                'write_to_memory': None,
            },
            'RORB': {
                'needs_ea': False,
                'ops': {0x56: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_B,
                'write_to_memory': None,
            },
        }
    },
    'RTI': {
        'mnemonic': {
            'RTI': {
                'needs_ea': False,
                'ops': {0x3B: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 6}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            }
        }
    },
    'RTS': {
        'mnemonic': {
            'RTS': {
                'needs_ea': False,
                'ops': {0x39: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 5}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            }
        }
    },
    'SBC': {
        'mnemonic': {
            'SBCA': {
                'needs_ea': False,
                'ops': {
                    0x82: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0x92: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xA2: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xB2: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_A,
                'write_to_memory': None,
            },
            'SBCB': {
                'needs_ea': False,
                'ops': {
                    0xC2: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0xD2: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xE2: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xF2: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_B,
                'write_to_memory': None,
            },
        }
    },
    'SEX': {
        'mnemonic': {
            'SEX': {
                'needs_ea': False,
                'ops': {0x1D: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            }
        }
    },
    'ST': {
        'mnemonic': {
            'STA': {
                'needs_ea': True,
                'ops': {
                    0x97: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xA7: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xB7: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': None,
                'register': REG_A,
                'write_to_memory': BYTE,
            },
            'STB': {
                'needs_ea': True,
                'ops': {
                    0xD7: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xE7: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xF7: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': None,
                'register': REG_B,
                'write_to_memory': BYTE,
            },
            'STD': {
                'needs_ea': True,
                'ops': {
                    0xDD: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 5},
                    0xED: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 5},
                    0xFD: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 6},
                },
                'read_from_memory': None,
                'register': REG_D,
                'write_to_memory': WORD,
            },
            'STS': {
                'needs_ea': True,
                'ops': {
                    0x10DF: {'addr_mode': DIRECT, 'bytes': 3, 'cycles': 6},
                    0x10EF: {'addr_mode': INDEXED, 'bytes': 3, 'cycles': 6},
                    0x10FF: {'addr_mode': EXTENDED, 'bytes': 4, 'cycles': 7},
                },
                'read_from_memory': None,
                'register': REG_S,
                'write_to_memory': WORD,
            },
            'STU': {
                'needs_ea': True,
                'ops': {
                    0xDF: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 5},
                    0xEF: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 5},
                    0xFF: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 6},
                },
                'read_from_memory': None,
                'register': REG_U,
                'write_to_memory': WORD,
            },
            'STX': {
                'needs_ea': True,
                'ops': {
                    0x9F: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 5},
                    0xAF: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 5},
                    0xBF: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 6},
                },
                'read_from_memory': None,
                'register': REG_X,
                'write_to_memory': WORD,
            },
            'STY': {
                'needs_ea': True,
                'ops': {
                    0x109F: {'addr_mode': DIRECT, 'bytes': 3, 'cycles': 6},
                    0x10AF: {'addr_mode': INDEXED, 'bytes': 3, 'cycles': 6},
                    0x10BF: {'addr_mode': EXTENDED, 'bytes': 4, 'cycles': 7},
                },
                'read_from_memory': None,
                'register': REG_Y,
                'write_to_memory': WORD,
            },
        }
    },
    'SUB': {
        'mnemonic': {
            'SUBA': {
                'needs_ea': False,
                'ops': {
                    0x80: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0x90: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xA0: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xB0: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_A,
                'write_to_memory': None,
            },
            'SUBB': {
                'needs_ea': False,
                'ops': {
                    0xC0: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 2},
                    0xD0: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 4},
                    0xE0: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 4},
                    0xF0: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 5},
                },
                'read_from_memory': BYTE,
                'register': REG_B,
                'write_to_memory': None,
            },
            'SUBD': {
                'needs_ea': False,
                'ops': {
                    0x83: {'addr_mode': IMMEDIATE_WORD, 'bytes': 3, 'cycles': 4},
                    0x93: {'addr_mode': DIRECT_WORD, 'bytes': 2, 'cycles': 6},
                    0xA3: {'addr_mode': INDEXED_WORD, 'bytes': 2, 'cycles': 6},
                    0xB3: {'addr_mode': EXTENDED_WORD, 'bytes': 3, 'cycles': 7},
                },
                'read_from_memory': WORD,
                'register': REG_D,
                'write_to_memory': None,
            },
        }
    },
    'SWI': {
        'mnemonic': {
            'SWI': {
                'needs_ea': False,
                'ops': {0x3F: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 19}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'SWI2': {
                'needs_ea': False,
                'ops': {0x103F: {'addr_mode': INHERENT, 'bytes': 2, 'cycles': 20}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
            'SWI3': {
                'needs_ea': False,
                'ops': {0x113F: {'addr_mode': INHERENT, 'bytes': 2, 'cycles': 20}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            },
        }
    },
    'SYNC': {
        'mnemonic': {
            'SYNC': {
                'needs_ea': False,
                'ops': {0x13: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': None,
                'write_to_memory': None,
            }
        }
    },
    'TFR': {
        'mnemonic': {
            'TFR': {
                'needs_ea': False,
                'ops': {0x1F: {'addr_mode': IMMEDIATE, 'bytes': 2, 'cycles': 7}},
                'read_from_memory': BYTE,
                'register': None,
                'write_to_memory': None,
            }
        }
    },
    'TST': {
        'mnemonic': {
            'TST': {
                'needs_ea': False,
                'ops': {
                    0x0D: {'addr_mode': DIRECT, 'bytes': 2, 'cycles': 6},
                    0x6D: {'addr_mode': INDEXED, 'bytes': 2, 'cycles': 6},
                    0x7D: {'addr_mode': EXTENDED, 'bytes': 3, 'cycles': 7},
                },
                'read_from_memory': BYTE,
                'register': None,
                'write_to_memory': None,
            },
            'TSTA': {
                'needs_ea': False,
                'ops': {0x4D: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_A,
                'write_to_memory': None,
            },
            'TSTB': {
                'needs_ea': False,
                'ops': {0x5D: {'addr_mode': INHERENT, 'bytes': 1, 'cycles': 2}},
                'read_from_memory': None,
                'register': REG_B,
                'write_to_memory': None,
            },
        }
    },
}
