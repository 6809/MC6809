import cProfile
import logging
import pstats
from typing import Annotated

import tyro
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.tyro_commands import TyroVerbosityArgType
from rich import print  # noqa

from MC6809.cli_app import app
from MC6809.core.benchmark import run_benchmark
from MC6809.example6809 import run_example


logger = logging.getLogger(__name__)


@app.command
def benchmark(
    loops: Annotated[int, tyro.conf.arg(help='How many benchmark loops should be run?')] = 6,
    multiply: Annotated[int, tyro.conf.arg(help='Process data multiplier')] = 15,
    verbosity: TyroVerbosityArgType = 1,
):
    """
    Run a MC6809 emulation benchmark
    """
    setup_logging(verbosity=verbosity)
    run_benchmark(loops=loops, multiply=multiply)


@app.command
def profile(
    loops: Annotated[int, tyro.conf.arg(help='How many benchmark loops should be run?')] = 6,
    multiply: Annotated[int, tyro.conf.arg(help='Process data multiplier')] = 15,
    verbosity: TyroVerbosityArgType = 1,
):
    """
    Profile the MC6809 emulation benchmark
    """
    setup_logging(verbosity=verbosity)
    with cProfile.Profile() as pr:
        run_benchmark(loops=loops, multiply=multiply)
    pstats.Stats(pr).sort_stats('tottime', 'cumulative', 'calls').print_stats(20)


@app.command
def example():
    """
    Just run the MC6809/example6809.py example (CRC32 calculation)
    """
    run_example()
