import tempfile
import unittest

from bx_py_utils.test_utils.redirect import RedirectOut
from bx_py_utils.test_utils.snapshot import assert_text_snapshot
from cli_base.cli_tools.test_utils.assertion import assert_in
from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRich

from MC6809 import cli_app


def skip_lines_before(text: str, line_prefix: str = ';') -> str | None:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(line_prefix):
            return '\n'.join(lines[idx:])
    return None


class DisassembleCliTestCase(unittest.TestCase):
    maxDiff = None

    def test_happy_path(self):
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(bytes([
                0x8E, 0x00, 0x01,
                0xBD, 0x40, 0x06,
                0x8E, 0x00, 0x00,
                0x39,
            ]))
            temp_file.flush()

            with NoColorEnvRich(), RedirectOut() as buffer:
                cli_app.main(args=('disassemble', temp_file.name, '--start-address', str(0x1000)))

        self.assertEqual(buffer.stderr, '')

        cleaned_output = skip_lines_before(buffer.stdout, line_prefix=';')
        assert_in(
            cleaned_output,
            parts=(
                '; Disassembly',
                '; LABEL000 = $4006',
                '1003| ',
                ' BD 40 06 ',
                ' JSR LABEL000',
            ),
        )
        assert_text_snapshot(got=cleaned_output, extension='.lst')
