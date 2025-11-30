from unittest import TestCase

from MC6809.components.MC6809data.MC6809_op_data import ALL_MNEMONIC, BRANCH_MNEMONICS


class OpDataTestCase(TestCase):
    def test_validate_branch_mnemonics(self):
        unknown = BRANCH_MNEMONICS - ALL_MNEMONIC
        self.assertFalse(unknown, f'Unknown branch mnemonics: {unknown}')
