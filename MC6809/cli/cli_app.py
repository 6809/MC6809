"""
    CLI for usage
"""
import cProfile
import logging
import pstats
import sys
from pathlib import Path

import rich_click as click
from bx_py_utils.path import assert_is_file
from rich import print  # noqa
from rich_click import RichGroup

import MC6809
from MC6809 import __version__, constants
from MC6809.core.bechmark import run_benchmark


logger = logging.getLogger(__name__)


PACKAGE_ROOT = Path(MC6809.__file__).parent.parent
assert_is_file(PACKAGE_ROOT / 'pyproject.toml')

OPTION_ARGS_DEFAULT_TRUE = dict(is_flag=True, show_default=True, default=True)
OPTION_ARGS_DEFAULT_FALSE = dict(is_flag=True, show_default=True, default=False)
ARGUMENT_EXISTING_DIR = dict(
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True, path_type=Path)
)
ARGUMENT_NOT_EXISTING_DIR = dict(
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        readable=False,
        writable=True,
        path_type=Path,
    )
)
ARGUMENT_EXISTING_FILE = dict(
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, path_type=Path)
)


class ClickGroup(RichGroup):  # FIXME: How to set the "info_name" easier?
    def make_context(self, info_name, *args, **kwargs):
        info_name = './cli.py'
        return super().make_context(info_name, *args, **kwargs)


@click.group(
    cls=ClickGroup,
    epilog=constants.CLI_EPILOG,
)
def cli():
    pass


@click.command()
def version():
    """Print version and exit"""
    # Pseudo command, because the version always printed on every CLI call ;)
    sys.exit(0)


cli.add_command(version)


@click.command()
@click.option('--loops', type=int, default=6, show_default=True, help='How many benchmark loops should be run?')
@click.option('--multiply', type=int, default=15, show_default=True, help='est data multiplier')
def benchmark(loops, multiply):
    """
    Run a MC6809 emulation benchmark
    """
    run_benchmark(loops=loops, multiply=multiply)


cli.add_command(benchmark)


@click.command()
@click.option('--loops', type=int, default=6, show_default=True, help='How many benchmark loops should be run?')
@click.option('--multiply', type=int, default=15, show_default=True, help='est data multiplier')
def profile(loops, multiply):
    """
    Profile the MC6809 emulation benchmark
    """
    with cProfile.Profile() as pr:
        run_benchmark(loops=loops, multiply=multiply)
    pstats.Stats(pr).sort_stats('tottime', 'cumulative', 'calls').print_stats(20)


cli.add_command(profile)


def main():
    print(f'[bold][green]MC6809[/green] v[cyan]{__version__}')

    # Execute Click CLI:
    cli.name = './cli.py'
    cli()
