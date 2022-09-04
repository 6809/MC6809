from cmd2 import CommandResult
from cmd2_ext_test import ExternalTestMixin
from dev_shell.tests.fixtures import CmdAppBaseTestCase

from MC6809.dev_shell import DevShellApp, get_devshell_app_kwargs


class DevShellAppTester(ExternalTestMixin, DevShellApp):
    pass


class DevShellAppBaseTestCase(CmdAppBaseTestCase):
    """
    Base class for dev-shell tests
    """

    def get_app_instance(self):
        # Init the test app with the same kwargs as the real app
        # see: dev_shell.cmd2app.devshell_cmdloop()
        app = DevShellAppTester(**get_devshell_app_kwargs())
        return app


class DragonPyDevShellTestCase(DevShellAppBaseTestCase):
    def test_help_raw(self):
        out = self.app.app_cmd('help')

        assert isinstance(out, CommandResult)
        stdout = out.stdout
        assert 'MC6809 commands' in stdout
        assert 'benchmark' in stdout
        assert 'profile' in stdout

    def test_help_via_execute(self):
        stdout, stderr = self.execute('help')
        assert stderr == ''
        assert 'MC6809 commands' in stdout
        assert 'benchmark' in stdout
        assert 'profile' in stdout

    def test_help_run(self):
        stdout, stderr = self.execute('help benchmark')
        assert stderr == ''
        assert 'Run a MC6809 emulation benchmark' in stdout
        assert ' --loops ' in stdout
        assert ' --multiply ' in stdout

    def test_benchmark(self):
        stdout, stderr = self.execute('benchmark --loops 1 --multiply 1')
        print(stdout)
        print(stderr)
        assert stderr == ''
        assert 'CRC16 benchmark' in stdout
        assert 'Start 1 CRC16 loops' in stdout
        assert 'CRC32 benchmark' in stdout
        assert 'Start 1 CRC32 loops' in stdout

    def test_profile(self):
        stdout, stderr = self.execute('profile --loops 1 --multiply 1')
        print(stdout)
        print(stderr)
        assert stderr == ''
        assert 'CRC16 benchmark' in stdout
        assert 'Start 1 CRC16 loops' in stdout
        assert 'CRC32 benchmark' in stdout
        assert 'Start 1 CRC32 loops' in stdout

        assert 'function calls' in stdout
        assert 'mc6809_base.py' in stdout
        assert 'memory.py' in stdout
