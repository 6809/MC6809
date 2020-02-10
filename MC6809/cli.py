#!/usr/bin/env python3

"""
    MC6809 - CLI
    ~~~~~~~~~~~~

    :created: 2015 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2015-2020 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""
import cProfile
import pstats
import sys

import MC6809
from MC6809.core.bechmark import run_benchmark


try:
    import click
except ImportError as err:
    print(f"Import error: {err}")
    print()
    print("Please install 'click' !")
    print("more info: http://click.pocoo.org")
    sys.exit(-1)


@click.group()
@click.version_option(MC6809.__version__)
def cli():
    """
    MC6809 is a Open source (GPL v3 or later) emulator
    for the legendary 6809 CPU, used in 30 years old homecomputer
    Dragon 32 and Tandy TRS-80 Color Computer (CoCo)...

    Created by Jens Diemer

    Homepage: https://github.com/6809/MC6809
    """
    pass


DEFAULT_LOOPS = 5
DEFAULT_MULTIPLY = 15
@cli.command(help="Run a MC6809 emulation benchmark")
@click.option("--loops", default=DEFAULT_LOOPS,
              help=f"How many benchmark loops should be run? (default: {DEFAULT_LOOPS:d})")
@click.option("--multiply", default=DEFAULT_MULTIPLY,
              help=f"Test data multiplier (default: {DEFAULT_MULTIPLY:d})")
def benchmark(loops, multiply):
    run_benchmark(loops, multiply)


@cli.command(help="Profile the MC6809 emulation benchmark")
@click.option("--loops", default=DEFAULT_LOOPS,
              help=f"How many benchmark loops should be run? (default: {DEFAULT_LOOPS:d})")
@click.option("--multiply", default=DEFAULT_MULTIPLY,
              help=f"Test data multiplier (default: {DEFAULT_MULTIPLY:d})")
def profile(loops, multiply):
    pr = cProfile.Profile()
    pr.enable()

    run_benchmark(loops, multiply)

    pr.disable()

    pstats.Stats(pr).sort_stats('tottime', 'cumulative', 'calls').print_stats(20)


if __name__ == "__main__":
    cli()
