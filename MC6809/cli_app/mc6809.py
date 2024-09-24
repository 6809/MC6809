import cProfile
import logging
import pstats

import rich_click as click

from MC6809.cli_app import cli
from MC6809.core.bechmark import run_benchmark


logger = logging.getLogger(__name__)


@cli.command()
@click.option('--loops', type=int, default=6, show_default=True, help='How many benchmark loops should be run?')
@click.option('--multiply', type=int, default=15, show_default=True, help='est data multiplier')
def benchmark(loops, multiply):
    """
    Run a MC6809 emulation benchmark
    """
    run_benchmark(loops=loops, multiply=multiply)


@cli.command()
@click.option('--loops', type=int, default=6, show_default=True, help='How many benchmark loops should be run?')
@click.option('--multiply', type=int, default=15, show_default=True, help='est data multiplier')
def profile(loops, multiply):
    """
    Profile the MC6809 emulation benchmark
    """
    with cProfile.Profile() as pr:
        run_benchmark(loops=loops, multiply=multiply)
    pstats.Stats(pr).sort_stats('tottime', 'cumulative', 'calls').print_stats(20)
