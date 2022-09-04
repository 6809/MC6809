import argparse
import cProfile
import pstats
from pathlib import Path

import cmd2
from cmd2 import Cmd2ArgumentParser, with_argparser
from dev_shell.base_cmd2_app import DevShellBaseApp, run_cmd2_app
from dev_shell.command_sets import DevShellBaseCommandSet
from dev_shell.command_sets.dev_shell_commands import DevShellCommandSet as OriginDevShellCommandSet
from dev_shell.config import DevShellConfig
from dev_shell.utils.colorful import bright_yellow
from dev_shell.utils.subprocess_utils import verbose_check_call
from poetry_publish.publish import poetry_publish

import MC6809
from MC6809.core.bechmark import run_benchmark


PACKAGE_ROOT = Path(MC6809.__file__).parent.parent.parent


@cmd2.with_default_category('MC6809 commands')
class MC6809CommandSet(DevShellBaseCommandSet):
    benchmark_argparser = Cmd2ArgumentParser()
    benchmark_argparser.add_argument(
        '--loops',
        type=int,
        default=6,
        help='How many benchmark loops should be run? (default: %(default)s)',
    )
    benchmark_argparser.add_argument(
        '--multiply',
        type=int,
        default=15,
        help='Test data multiplier (default: %(default)s)',
    )

    @with_argparser(benchmark_argparser)
    def do_benchmark(self, args: argparse.Namespace):
        """
        Run a MC6809 emulation benchmark
        """
        run_benchmark(loops=args.loops, multiply=args.multiply)

    @with_argparser(benchmark_argparser)
    def do_profile(self, args: argparse.Namespace):
        """
        Profile the MC6809 emulation benchmark
        """
        with cProfile.Profile() as pr:
            run_benchmark(loops=args.loops, multiply=args.multiply)
        pstats.Stats(pr).sort_stats('tottime', 'cumulative', 'calls').print_stats(20)


class DevShellCommandSet(OriginDevShellCommandSet):
    def do_publish(self, statement: cmd2.Statement):
        """
        Publish "dev-shell" to PyPi
        """
        # don't publish if code style wrong:
        verbose_check_call('darker', '--check')

        # don't publish if test fails:
        verbose_check_call('pytest', '-x')

        poetry_publish(
            package_root=PACKAGE_ROOT,
            version=MC6809.__version__,
            creole_readme=False,
        )


class DevShellApp(DevShellBaseApp):
    # Remove some commands:
    delattr(cmd2.Cmd, 'do_edit')
    delattr(cmd2.Cmd, 'do_shell')
    delattr(cmd2.Cmd, 'do_run_script')
    delattr(cmd2.Cmd, 'do_run_pyscript')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.intro = f'Developer shell - {bright_yellow("MC6809")} - v{MC6809.__version__}\n'


def get_devshell_app_kwargs():
    """
    Generate the kwargs for the cmd2 App.
    (Separated because we needs the same kwargs in tests)
    """
    config = DevShellConfig(package_module=MC6809)

    # initialize all CommandSet() with context:
    kwargs = dict(config=config)

    app_kwargs = dict(
        config=config,
        command_sets=[
            MC6809CommandSet(**kwargs),
            DevShellCommandSet(**kwargs),
        ],
    )
    return app_kwargs


def devshell_cmdloop():
    """
    Entry point to start the "dev-shell" cmd2 app.
    Used in: [tool.poetry.scripts]
    """
    app = DevShellApp(**get_devshell_app_kwargs())
    run_cmd2_app(app)  # Run a cmd2 App as CLI or shell
