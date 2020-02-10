#!/usr/bin/env python

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================

    :copyleft: 2013-2015 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import unittest

from click.testing import CliRunner

import MC6809
from MC6809.cli import cli


class CLITestCase(unittest.TestCase):
    """
    TODO: Do more than this simple tests
    """

    def _invoke(self, *args):
        runner = CliRunner()
        result = runner.invoke(cli, args)

        if result.exit_code != 0:
            msg = (
                "cli return code: %r\n"
                " *** output: ***\n"
                "%s\n"
                " *** exception: ***\n"
                "%s\n"
                "****************\n"
            ) % (result.exit_code, result.output, result.exception)
            self.assertEqual(result.exit_code, 0, msg=msg)

        return result

    def assert_contains_members(self, members, container):
        for member in members:
            msg = f"{member!r} not found in:\n{container}"
            # self.assertIn(member, container, msg) # Bad error message :(
            if member not in container:
                self.fail(msg)

    def assert_not_contains_members(self, members, container):
        for member in members:
            if member in container:
                self.fail(f"{member!r} found in:\n{container}")

    def test_main_help(self):
        result = self._invoke("--help")
        self.assert_contains_members([
            "cli [OPTIONS] COMMAND [ARGS]...",
            "Commands:",
            "benchmark ", " Run a MC6809 emulation benchmark",
            "profile ", " Profile the MC6809 emulation benchmark",
        ], result.output)

        errors = ["Error", "Traceback"]
        self.assert_not_contains_members(errors, result.output)

    def test_version(self):
        result = self._invoke("--version")
        self.assertIn(MC6809.__version__, result.output)

    def test_benchmark_help(self):
        result = self._invoke("benchmark", "--help")
        #        print(result.output)
        #        print(cli_err)
        self.assert_contains_members([
            "Usage: cli benchmark [OPTIONS]",
            "Run a MC6809 emulation benchmark",
        ], result.output)

        errors = ["Error", "Traceback"]
        self.assert_not_contains_members(errors, result.output)

    def test_run_benchmark(self):
        result = self._invoke("benchmark", "--loops", "1", "--multiply", "1")
        self.assert_contains_members([
            "CRC16 benchmark",
            "Start 1 CRC16 loops",
            "CRC32 benchmark",
            "Start 1 CRC32 loops",
        ], result.output)

        errors = ["Error", "Traceback"]
        self.assert_not_contains_members(errors, result.output)

    def test_run_profile(self):
        result = self._invoke("profile", "--loops", "1", "--multiply", "1")
        self.assert_contains_members([
            "CRC16 benchmark",
            "Start 1 CRC16 loops",
            "CRC32 benchmark",
            "Start 1 CRC32 loops",

            "function calls",
            "MC6809/components/mc6809_base.py",
            "MC6809/components/memory.py",
        ], result.output)

        errors = ["Error", "Traceback"]
        self.assert_not_contains_members(errors, result.output)
