#!/usr/bin/env python

"""
    MC6809 - CLI
    ~~~~~~~~~~~~

    :created: 2015 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2015 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function


import sys
import unittest

try:
    import click
except ImportError as err:
    print("Import error: %s" % err)
    print()
    print("Please install 'click' !")
    print("more info: http://click.pocoo.org")
    sys.exit(-1)

from MC6809.tests import run_tests
from MC6809.core.bechmark import run_benchmark


@click.group()
def cli():
    pass


DEFAULT_LOOPS = 5
@cli.command(help="Run a 6809 Emulation benchmark")
@click.option("--loops", default=DEFAULT_LOOPS,
    help="How many benchmark loops should be run? (default: %i)" % DEFAULT_LOOPS)
def benchmark(loops):
    run_benchmark(loops)


@cli.command(help="Run unittests")
@click.option('--verbosity', default=2, help='Number for verbosity settings')
@click.option('--failfast', default=False, help='Number for verbosity settings', is_flag=True)
def tests(verbosity, failfast):
    run_tests(verbosity, failfast)


if __name__ == "__main__":
    cli()