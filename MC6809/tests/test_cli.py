#!/usr/bin/env python

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================

    :copyleft: 2013-2015 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

import os
import subprocess
import sys
import unittest

CLI = os.path.normpath(
    os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "cli.py"
    )
)


class CLITestCase(unittest.TestCase):
    """
    TODO: Do more than this simple tests
    """

    def _get(self, *args):
        self.assertTrue(os.path.isfile(CLI), "Not a file: %r" % CLI)
        cmd_args = [
            sys.executable,
            CLI
        ]
        cmd_args += args
        # print("\nStartup CLI with: %s" % " ".join(cmd_args[1:]))

        p = subprocess.Popen(
            cmd_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        retcode = p.wait()

        cli_out = p.stdout.read()
        p.stdout.close()
        cli_err = p.stderr.read()
        p.stderr.close()

        if retcode != 0:
            msg = (
                "subprocess returned %s.\n"
                " *** stdout: ***\n"
                "%s\n"
                " *** stderr: ***\n"
                "%s\n"
                "****************\n"
            ) % (retcode, cli_out, cli_err)
            self.assertEqual(retcode, 0, msg=msg)

        return cli_out, cli_err

    def assertInMultiline(self, members, container):
        for member in members:
            msg = "%r not found in:\n%s" % (member, container)
            # self.assertIn(member, container, msg) # Bad error message :(
            if not member in container:
                self.fail(msg)

    def assertNotInMultiline(self, members, container):
        for member in members:
            if member in container:
                self.fail("%r found in:\n%s" % (member, container))

    def test_main_help(self):
        cli_out, cli_err = self._get("--help")
        self.assertInMultiline([
            "cli.py [OPTIONS] COMMAND [ARGS]...",
            "Commands:",
            "benchmark  Run a 6809 Emulation benchmark",
            "tests      Run unittests",
        ], cli_out)

        errors = ["Error", "Traceback"]
        self.assertNotInMultiline(errors, cli_out)
        self.assertNotInMultiline(errors, cli_err)

    def test_benchmark_help(self):
        cli_out, cli_err = self._get("benchmark", "--help")
        #        print(cli_out)
        #        print(cli_err)
        self.assertInMultiline([
            "Usage: cli.py benchmark [OPTIONS]",
            "Run a 6809 Emulation benchmark",
        ], cli_out)

        errors = ["Error", "Traceback"]
        self.assertNotInMultiline(errors, cli_out)
        self.assertNotInMultiline(errors, cli_err)

    def test_run_benchmark(self):
        cli_out, cli_err = self._get("benchmark", "--loops", "1", "--multiply", "1")
        self.assertInMultiline([
            "CRC16 benchmark",
            "Start 1 CRC16 loops",
            "CRC32 benchmark",
            "Start 1 CRC32 loops",
        ], cli_out)

        errors = ["Error", "Traceback"]
        self.assertNotInMultiline(errors, cli_out)
        self.assertNotInMultiline(errors, cli_err)


if __name__ == '__main__':
    unittest.main(verbosity=2)
