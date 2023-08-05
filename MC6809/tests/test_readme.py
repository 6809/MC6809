from bx_py_utils.auto_doc import assert_readme_block
from bx_py_utils.path import assert_is_file
from manageprojects.test_utils.click_cli_utils import invoke_click
from manageprojects.tests.base import BaseTestCase

from MC6809 import constants
from MC6809.cli.cli_app import PACKAGE_ROOT, cli
from MC6809.cli.dev import cli as dev_cli


def assert_cli_help_in_readme(text_block: str, marker: str):
    README_PATH = PACKAGE_ROOT / 'README.md'
    assert_is_file(README_PATH)

    text_block = text_block.replace(constants.CLI_EPILOG, '')
    text_block = f'```\n{text_block.strip()}\n```'
    assert_readme_block(
        readme_path=README_PATH,
        text_block=text_block,
        start_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} start ✂✂✂)',
        end_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} end ✂✂✂)',
    )


class ReadmeTestCase(BaseTestCase):
    def test_main_help(self):
        stdout = invoke_click(cli, '--help')
        self.assert_in_content(
            got=stdout,
            parts=(
                'Usage: ./cli.py [OPTIONS] COMMAND [ARGS]...',
                ' benchmark ',
                ' profile ',
                constants.CLI_EPILOG,
            ),
        )
        assert_cli_help_in_readme(text_block=stdout, marker='main help')

    def test_dev_cli_main_help(self):
        stdout = invoke_click(dev_cli, '--help')
        self.assert_in_content(
            got=stdout,
            parts=(
                'Usage: ./dev-cli.py [OPTIONS] COMMAND [ARGS]...',
                ' check-code-style ',
                ' coverage ',
                constants.CLI_EPILOG,
            ),
        )
        assert_cli_help_in_readme(text_block=stdout, marker='dev help')

    def test_benchmark_help(self):
        stdout = invoke_click(cli, 'benchmark', '--help')
        self.assert_in_content(
            got=stdout,
            parts=(
                'Usage: ./cli.py benchmark [OPTIONS]',
                ' --loops ',
                ' --multiply ',
            ),
        )
        assert_cli_help_in_readme(text_block=stdout, marker='benchmark help')

    def test_profile_help(self):
        stdout = invoke_click(cli, 'profile', '--help')
        self.assert_in_content(
            got=stdout,
            parts=(
                'Usage: ./cli.py profile [OPTIONS]',
                ' --loops ',
                ' --multiply ',
            ),
        )
        assert_cli_help_in_readme(text_block=stdout, marker='profile help')
