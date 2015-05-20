#!/usr/bin/env python2
# coding: utf-8

"""
    DragonPy - CLI
    ~~~~~~~~~~~~~~

    :created: 2013 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2013-2015 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function


import atexit
import locale
import logging


# https://pypi.python.org/pypi/click/
import click

from dragonlib.utils.logging_utils import setup_logging, LOG_LEVELS

from basic_editor.editor import run_basic_editor

import dragonpy
from dragonpy.CoCo.config import CoCo2bCfg
from dragonpy.CoCo.machine import run_CoCo2b
from dragonpy.Dragon32.config import Dragon32Cfg
from dragonpy.Dragon32.machine import run_Dragon32
from dragonpy.Dragon64.config import Dragon64Cfg
from dragonpy.Dragon64.machine import run_Dragon64
from dragonpy.Multicomp6809.config import Multicomp6809Cfg
from dragonpy.Multicomp6809.machine import run_Multicomp6809
from dragonpy.core import configs
from dragonpy.core.bechmark import run_benchmark
from dragonpy.core.configs import machine_dict
from dragonpy.sbc09.config import SBC09Cfg
from dragonpy.sbc09.machine import run_sbc09
from dragonpy.vectrex.config import VectrexCfg
from dragonpy.vectrex.machine import run_Vectrex


log = logging.getLogger(__name__)


# DEFAULT_LOG_FORMATTER = "%(message)s"
# DEFAULT_LOG_FORMATTER = "%(processName)s/%(threadName)s %(message)s"
# DEFAULT_LOG_FORMATTER = "[%(processName)s %(threadName)s] %(message)s"
# DEFAULT_LOG_FORMATTER = "[%(levelname)s %(asctime)s %(module)s] %(message)s"
# DEFAULT_LOG_FORMATTER = "%(levelname)8s %(created)f %(module)-12s %(message)s"
DEFAULT_LOG_FORMATTER = "%(relativeCreated)-5d %(levelname)8s %(module)13s %(lineno)d %(message)s"


machine_dict.register(configs.DRAGON32, (run_Dragon32, Dragon32Cfg), default=True)
machine_dict.register(configs.DRAGON64, (run_Dragon64, Dragon64Cfg))
machine_dict.register(configs.COCO2B, (run_CoCo2b, CoCo2bCfg))
machine_dict.register(configs.SBC09, (run_sbc09,SBC09Cfg))
# machine_dict.register(configs.SIMPLE6809, Simple6809Cfg)
machine_dict.register(configs.MULTICOMP6809, (run_Multicomp6809, Multicomp6809Cfg))
machine_dict.register(configs.VECTREX, (run_Vectrex, VectrexCfg))


# use user's preferred locale
# e.g.: for formating cycles/sec number
locale.setlocale(locale.LC_ALL, '')


@atexit.register
def goodbye():
    print("\n --- END --- \n")



class CliConfig(object):
    def __init__(self, machine, log, verbosity, log_formatter):
        self.machine = machine
        self.log = log
        self.verbosity=int(verbosity)
        self.log_formatter=log_formatter

        self.setup_logging()

        self.cfg_dict = {
            "verbosity":self.verbosity,
            "trace":None,
        }
        machine_name = self.machine
        self.machine_run_func, self.machine_cfg = machine_dict[machine]

    def setup_logging(self):
        handler = logging.StreamHandler()

        # Setup root logger
        setup_logging(
            level=self.verbosity,
            logger_name=None, # Use root logger
            handler=handler,
            log_formatter=self.log_formatter
        )

        if self.log is None:
            return

        # Setup given loggers
        for logger_cfg in self.log:
            logger_name, level = logger_cfg.rsplit(",", 1)
            level = int(level)

            setup_logging(
                level=level,
                logger_name=logger_name,
                handler=handler,
                log_formatter=self.log_formatter
            )

cli_config = click.make_pass_decorator(CliConfig)


@click.group()
@click.version_option(dragonpy.__version__)
@click.option("--machine",
    type=click.Choice(sorted(machine_dict.keys())),
    default=machine_dict.DEFAULT,
    help="Used machine configuration (Default: %s)" % machine_dict.DEFAULT)
@click.option("--log", default=False, multiple=True,
    help="Setup loggers, e.g.: --log DragonPy.cpu6809,50 --log dragonpy.Dragon32.MC6821_PIA,10")
@click.option("--verbosity",
    type=click.Choice(["%i" % level for level in LOG_LEVELS]),
    default="%i" % logging.CRITICAL,
    help="verbosity level to stdout (lower == more output! default: %s)" % logging.INFO)
@click.option("--log_formatter", default=DEFAULT_LOG_FORMATTER,
    help="see: http://docs.python.org/2/library/logging.html#logrecord-attributes")
@click.pass_context
def cli(ctx, **kwargs):
    log.critical("cli kwargs: %s", repr(kwargs))
    ctx.obj = CliConfig(**kwargs)


@cli.command(help="Run only the BASIC editor")
@cli_config
def editor(cli_config):
    log.critical("Use machine cfg: %s", cli_config.machine_cfg.__name__)
    cfg = cli_config.machine_cfg(cli_config.cfg_dict)
    run_basic_editor(cfg)


@cli.command(help="Run a machine emulation")
@click.option("--trace", default=False,
    help="Create trace lines."
)
@click.option("--ram", default=None, help="RAM file to load (default none)")
@click.option("--rom", default=None, help="ROM file to use (default set by machine configuration)")
@click.option("--max_ops", default=None, type=int,
    help="If given: Stop CPU after given cycles else: run forever")
@cli_config
def run(cli_config, **kwargs):
    log.critical("Use machine func: %s", cli_config.machine_run_func.__name__)
    log.critical("cli run kwargs: %s", repr(kwargs))
    cli_config.cfg_dict.update(kwargs)
    cli_config.machine_run_func(cli_config.cfg_dict)


DEFAULT_LOOPS = 5
@cli.command(help="Run a 6809 Emulation benchmark")
@click.option("--loops", default=DEFAULT_LOOPS,
    help="How many benchmark loops should be run? (default: %i)" % DEFAULT_LOOPS)
def benchmark(loops):
    log.critical("Run a benchmark only...")
    run_benchmark(loops)


@cli.command(help="List all exiting loggers and exit.")
def log_list():
    print("A list of all loggers:")
    for log_name in sorted(logging.Logger.manager.loggerDict):
        print("\t%s" % log_name)


if __name__ == "__main__":
    cli()