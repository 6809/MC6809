## MC6809 CPU emulator written in Python

MC6809 is a Open source (GPL v3 or later) emulator for the legendary **6809** CPU, used old homecomputer [Dragon 32/64](https://en.wikipedia.org/wiki/Dragon_32/64) and [Tandy TRS-80 Color Computer (CoCo)](https://en.wikipedia.org/wiki/TRS-80_Color_Computer) built in the 1980s...

Tested with Python 3.8, 3.9, 3.10 and PyPy3

[![tests](https://github.com/6809/MC6809/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/6809/MC6809/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/6809/MC6809/branch/main/graph/badge.svg)](https://app.codecov.io/github/6809/MC6809)
[![MC6809 @ PyPi](https://img.shields.io/pypi/v/MC6809?label=MC6809%20%40%20PyPi)](https://pypi.org/project/MC6809/)
[![Python Versions](https://img.shields.io/pypi/pyversions/MC6809)](https://github.com/6809/MC6809/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/MC6809)](https://github.com/6809/MC6809/blob/main/LICENSE)


A example usage can be find in: [MC6809/example6809.py](https://github.com/6809/MC6809/blob/main/MC6809/example6809.py)

Getting started:
```bash
~$ git clone https://github.com/6809/MC6809.git
~$ cd MC6809
~/MC6809 $ ./cli.py --help
```

The output of `./cli.py --help` looks like:

[comment]: <> (✂✂✂ auto generated main help start ✂✂✂)
```
Usage: ./cli.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ benchmark            Run a MC6809 emulation benchmark                                            │
│ profile              Profile the MC6809 emulation benchmark                                      │
│ version              Print version and exit                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated main help end ✂✂✂)


There is a simple benchmark. Run e.g.:
```bash
~/MC6809$ ./cli.py benchmark --help
```

The output of `./cli.py benchmark --help` looks like:

[comment]: <> (✂✂✂ auto generated benchmark help start ✂✂✂)
```
Usage: ./cli.py benchmark [OPTIONS]

 Run a MC6809 emulation benchmark

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --loops       INTEGER  How many benchmark loops should be run? [default: 6]                      │
│ --multiply    INTEGER  est data multiplier [default: 15]                                         │
│ --help                 Show this message and exit.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated benchmark help end ✂✂✂)


### profile

You can run the Python profiler against the benchmark, e.g.:

```bash
~/MC6809$ ./cli.py profile --help
```

The output of `./cli.py profile --help` looks like:

[comment]: <> (✂✂✂ auto generated profile help start ✂✂✂)
```
Usage: ./cli.py profile [OPTIONS]

 Profile the MC6809 emulation benchmark

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --loops       INTEGER  How many benchmark loops should be run? [default: 6]                      │
│ --multiply    INTEGER  est data multiplier [default: 15]                                         │
│ --help                 Show this message and exit.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated profile help end ✂✂✂)


### development

For development exists `dev-cli`, e.g.:

```bash
~/MC6809$ ./dev-cli.py --help
```

The output of `./dev-cli.py --help` looks like:

[comment]: <> (✂✂✂ auto generated dev help start ✂✂✂)
```
Usage: ./dev-cli.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ check-code-style            Check code style by calling darker + flake8                          │
│ coverage                    Run and show coverage.                                               │
│ fix-code-style              Fix code style of all MC6809 source code files via darker            │
│ install                     Run pip-sync and install 'MC6809' via pip as editable.               │
│ mypy                        Run Mypy (configured in pyproject.toml)                              │
│ publish                     Build and upload this project to PyPi                                │
│ safety                      Run safety check against current requirements files                  │
│ test                        Run unittests                                                        │
│ tox                         Run tox                                                              │
│ update                      Update "requirements*.txt" dependencies files                        │
│ update-test-snapshot-files  Update all test snapshot files (by remove and recreate all snapshot  │
│                             files)                                                               │
│ version                     Print version and exit                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated dev help end ✂✂✂)

Run tests, e.g.:

```bash
~/DragonPy$ ./dev-cli.py coverage
# or just:
~/DragonPy$ ./dev-cli.py test
# or with different Python versions:
~/DragonPy$ ./dev-cli.py tox
```

### TODO


* Update 'cpu6809_html_debug.py'
* Use bottle for http control server part
* unimplemented OPs:
  * RESET
  * SWI / SWI2 / SWI3
  * SYNC


## Make new release

We use [cli-base-utilities](https://github.com/jedie/cli-base-utilities#generate-project-history-base-on-git-commitstags) to generate the history in this README.


To make a new release, do this:

* Increase your project version number
* Run tests to update the README
* commit the changes
* Create release


## History

(Some of the points are related to [DragonPy Emulator](https://github.com/jedie/DragonPy))

[comment]: <> (✂✂✂ auto generated history start ✂✂✂)

* [v0.7.2](https://github.com/6809/MC6809/compare/v0.7.1...v0.7.2)
  * 2023-11-03 - Auto generate README history
  * 2023-11-03 - Fix code style
  * 2023-11-03 - Apply manageprojects updates + Update requirements
  * 2023-11-03 - Use verbose_check_call from cli_base
  * 2023-11-02 - Bump pip from 23.2.1 to 23.3
* [v0.7.1](https://github.com/6809/MC6809/compare/v0.7.0...v0.7.1)
  * 2023-08-05 - fix publish call
  * 2023-08-05 - Split CLI by apply manageprojects update
  * 2023-08-04 - Update requirements
* [v0.7.0](https://github.com/6809/MC6809/compare/v0.6.0...v0.7.0)
  * 2023-03-07 - Add "benchmark" and "profile" to CLI and remove dev-shell add DocTests
  * 2023-03-07 - Apply managedprojects update: Add DocTests via bx_py_utils helper
  * 2023-03-06 - Update README.md
  * 2023-03-06 - Migrate to https://github.com/jedie/cookiecutter_templates
  * 2022-09-04 - deactivate pypy3
  * 2022-09-04 - fix tests under windows
  * 2022-09-04 - fix code style
  * 2022-09-04 - replace Makefile with "dev-shell"
  * 2022-09-04 - update Makefile
  * 2022-09-04 - update README
  * 2022-09-04 - small code update
  * 2022-09-04 - remove travis config
  * 2022-09-04 - flynt updates
  * 2022-09-04 - fix flynt call
  * 2022-09-04 - replace Creole README with markdown
  * 2022-09-04 - fix pytest config
  * 2022-09-04 - update github CI
  * 2022-09-04 - add "make update"
  * 2022-09-04 - fix editorconfig
* [v0.6.0](https://github.com/6809/MC6809/compare/v0.5.0...v0.6.0)
  * 2020-02-10 - update CLI Tests
  * 2020-02-10 - git ignore: +/publish.log
  * 2020-02-10 - update CLI and README
  * 2020-02-10 - test release v0.6.0.dev0
  * 2020-02-10 - swap autopep8 and isort
  * 2020-02-10 - update Travis CI config
  * 2020-02-10 - fix code style
  * 2020-02-10 - update .join() statements
  * 2020-02-10 - setup poetry-publish
  * 2020-02-10 - apply pyupgrade
  * 2020-02-10 - apply code formatter
  * 2020-02-10 - f-strings convert
  * 2020-02-10 - WIP

<details><summary>Expand older history entries ...</summary>

* [v0.5.0](https://github.com/6809/MC6809/compare/v0.4.6...v0.5.0)
  * 2015-10-19 - update release info/Version
  * 2015-09-10 - try to install python on osx
  * 2015-09-03 - move Condition Code Register (CC) into CPU via mixin class
  * 2015-09-03 - rename mixin classes
  * 2015-09-03 - code cleanup
  * 2015-09-03 - rename base class
  * 2015-09-03 - Optimize: Don't return value. Because not needed in every case.
  * 2015-09-03 - do it directly
  * 2015-09-03 - remove .get() calls
  * 2015-09-03 - update README and version number
  * 2015-09-01 - OSX builds do not yet support Python :(
  * 2015-09-01 - refactor/move self._convert_differend_width()
  * 2015-09-01 - Bugfix _convert_differend_width()
  * 2015-08-31 - display report
  * 2015-08-31 - Append coverage data to .coverage
  * 2015-08-31 - WIP
  * 2015-08-31 - try to run DragonPy tests, too.
  * 2015-08-31 - obsolete since nose use
  * 2015-08-26 - WIP: speedlimit <-> normal
  * 2015-08-25 - Update README.creole
  * 2015-08-24 - WIP: Split CPU code
* [v0.4.6](https://github.com/6809/MC6809/compare/v0.4.5...v0.4.6)
  * 2015-08-24 - Update README. Release as v0.4.6
  * 2015-08-24 - change speed limit stuff.
* [v0.4.5](https://github.com/6809/MC6809/compare/v0.4.4...v0.4.5)
  * 2015-08-21 - release v0.4.5
  * 2015-08-21 - update history
  * 2015-08-21 - add cli information for run via subprocess in DragonPy
  * 2015-08-21 - use click CliRunner().invoke() for cli test
  * 2015-08-21 - add info text to cli
  * 2015-08-21 - deactivate 'cpu6809_html_debug.py' - TODO: update it!
  * 2015-08-21 - cleanup
  * 2015-08-21 - Update README.creole
  * 2015-08-20 - define the entrypoint name
  * 2015-08-10 - update PyPi/Hithub links
* [v0.4.4](https://github.com/6809/MC6809/compare/v0.4.3...v0.4.4)
  * 2015-08-10 - bugfix example to run with py2 and py3
  * 2015-08-10 - remove run tests from cli
  * 2015-08-10 - remove obsolete code (has run unittests two times)
  * 2015-08-10 - test the example, too
* [v0.4.3](https://github.com/6809/MC6809/compare/v0.4.2...v0.4.3)
  * 2015-08-10 - update from:
  * 2015-08-10 - just see that nose not fail: TODO update!
  * 2015-08-10 - bugfix ;)
  * 2015-08-10 - obsolete
  * 2015-08-10 - use click
  * 2015-08-10 - cleanup
  * 2015-08-10 - Exclude from nose
  * 2015-08-10 - start using nose
  * 2015-07-02 - add flattr link
* [v0.4.2](https://github.com/6809/MC6809/compare/v0.4.1...v0.4.2)
  * 2015-05-27 - relase as v0.4.2
  * 2015-05-27 - Add MC6809/example6809.py
  * 2015-05-27 - add CPU instance in CPU to memory
* [v0.4.1](https://github.com/6809/MC6809/compare/v0.4.0...v0.4.1)
  * 2015-05-26 - Tested with Python 2.7, 3.4 and PyPy
* [v0.4.0](https://github.com/6809/MC6809/compare/80f221b...v0.4.0)
  * 2015-05-26 - remove obsolete file
  * 2015-05-26 - cleanup
  * 2015-05-26 - +click +MC6809 cli entry point
  * 2015-05-26 - Add unittest for cli and add "--multiply" to benchmark
  * 2015-05-26 - fixup! add --source=MC6809
  * 2015-05-26 - add --source=MC6809
  * 2015-05-26 - remove dragonlib
  * 2015-05-26 - update coveralls token
  * 2015-05-26 - WIP: cleanup
  * 2015-05-26 - unittest run code
  * 2015-05-26 - add cli for benchmark
  * 2015-05-26 - add TODO
  * 2015-05-26 - bugfix imports
  * 2015-05-26 - remove obsolete files
  * 2015-05-26 - update setup.py
  * 2015-05-26 - fix links
  * 2015-05-26 - WIP: replace "DragonPy" -> "MC6809"
  * 2015-05-26 - rename
  * 2015-05-26 - cut README
  * 2015-05-20 - remove PyDev configs
  * 2015-05-20 - update README
  * 2015-05-20 - Update README.creole
  * 2015-05-20 - update travis-ci.org config
  * 2015-05-20 - move/rename cli code adn remove obsolete code
  * 2015-05-20 - Bugfix CLI and tests for it
  * 2015-01-28 - start to reimplement the CLI with "Click"
  * 2014-12-15 - use pygments syntax highlighter in BASIC editor
  * 2014-12-06 - Update .travis.yml
  * 2014-11-13 - 'dragonlib' as dependency
  * 2014-11-13 - outsource dragonlib:
  * 2014-11-13 - move LOG_LEVELS
  * 2014-10-08 - Bugfix for ReSt
  * 2014-10-08 - Add a setup.cfg
  * 2014-09-30 - add more info
  * 2014-09-30 - Bugfix
  * 2014-09-30 - WIP: BASIC editor: reformat code
  * 2014-09-30 - Bugfix renum tool + renum INVADER.bas
  * 2014-09-30 - PY3 bugfix
  * 2014-09-30 - Bugfix if line number > $ff
  * 2014-09-30 - Display also datum
  * 2014-09-29 - display more info on overflow error
  * 2014-09-29 - move BASIC programs
  * 2014-09-25 - Reimplement SBC09  ;)
  * 2014-09-25 - Split Op data - Squashed commit of the following:
  * 2014-09-24 - Disable some log output and update pypy win batches
  * 2014-09-24 - display_queue -> display_callback
  * 2014-09-22 - code cleanup and disable some log output
  * 2014-09-22 - move ROM load code
  * 2014-09-22 - code cleanup
  * 2014-09-22 - file rename and remove obsolete files
  * 2014-09-22 - move CPU utils
  * 2014-09-22 - move MC6809data
  * 2014-09-22 - ignore .idea/*
  * 2014-09-22 - update to new API
  * 2014-09-22 - Better default log formatter
  * 2014-09-18 - Bugfix unittest
  * 2014-09-18 - update test_run()
  * 2014-09-18 - display more info if e.g. the ROM loaded into a wrong area
  * 2014-09-18 - reimplement Multicomp 6809 !
  * 2014-09-18 - change logging setup
  * 2014-09-14 - Update README, see also:
  * 2014-09-14 - Release v0.2.0
  * 2014-09-14 - bugfix runtime
  * 2014-09-13 - display python version info in status line
  * 2014-09-13 - bugfix for Py2
  * 2014-09-13 - add python major version number to pickle files
  * 2014-09-13 - Update unittests in dragonlib, too.
  * 2014-09-13 - reimplement: Run CPU not faster than given speedlimit
  * 2014-09-13 - update unitests
  * 2014-09-13 - bugfix six.moves.xrange
  * 2014-09-13 - remove old multiprocessing files
  * 2014-09-13 - use xrange from six.py
  * 2014-09-12 - replace own lib2and3 with six
  * 2014-09-12 - WIP: refactor logging usage
  * 2014-09-12 - WIP: cpu run
  * 2014-09-11 - doesnt needed
  * 2014-09-11 - Start, refactoring memory:
  * 2014-09-09 - add more comments into PIA
  * 2014-09-08 - add "target CPU burst loops" to GUI config
  * 2014-09-07 - WIP: Implement IRQ
  * 2014-09-08 - merge code
  * 2014-09-08 - implement a callback mechanism which trigger the CPU cycles
  * 2014-09-11 - fix ReSt generation?
  * 2014-09-11 - use array.array("B", ...) for RAM/ROM memory
  * 2014-09-11 - Add callback/middleware tests to write byte, too.
  * 2014-09-11 - better tracebacks by using reraise
  * 2014-09-07 - A better speedlimit solution. TODO: Codecleanup
  * 2014-09-07 - WIP: Better speed limit
  * 2014-09-07 - add a not really good working speedlimit
  * 2014-09-05 - WIP: Release as v0.1.0
  * 2014-09-05 - include free v09.rom and vectrex ROM
  * 2014-09-05 - include scripts
  * 2014-09-05 - skip unittest if ROM files missing
  * 2014-09-05 - ignore /dist/
  * 2014-09-05 - include some more files
  * 2014-09-05 - Use python-creole to generate ReSt README on the fly, see:
  * 2014-09-05 - implemend "hard reset"
  * 2014-09-05 - Just add the alternative commented
  * 2014-09-05 - Simple loop optimizing
  * 2014-09-05 - little more information on error
  * 2014-09-04 - Work-a-round for https://bitbucket.org/pypy/pypy/issue/1858/pypy3-localeformat-d-val-1
  * 2014-09-04 - remove from __future__ import unicode_literals
  * 2014-09-04 - Adjust CPU burst count dynamically.
  * 2014-09-04 - update unittests
  * 2014-09-04 - remove threading stuff and use only tkinter after
  * 2014-09-04 - change grammar version in PyDev
  * 2014-09-04 - bugfix string.letters vs. string.ascii_letters
  * 2014-09-03 - bugfix cli unittest
  * 2014-09-03 - change print to log output
  * 2014-09-03 - explizit close
  * 2014-09-03 - log.warn() -> log.warning()
  * 2014-09-03 - Add a simple benchmark
  * 2014-09-03 - use '{:n}'.format(val) for formating cycles/sec
  * 2014-09-03 - add .pyo
  * 2014-09-03 - bugfix if run with -OO
  * 2014-09-03 - print all catched Ops vial decorator
  * 2014-09-03 - bugfix running CoCo from CLI
  * 2014-09-03 - use: python -m unittest discover
  * 2014-09-03 - updates: supported Python versions
  * 2014-09-03 - chnages to support python 2 and 3 with the same code
  * 2014-09-03 - changes to run with python2 and __future__ imports
  * 2014-09-03 - just run 2to3 script
  * 2014-08-31 - WIP: Just add dummy code for Vectrex
  * 2014-08-28 - Highlight line numbers and more the just one
  * 2014-08-28 - First, simple code highlighting
  * 2014-08-28 - Don't consume spaces between line number and code
  * 2014-08-28 - made BASIC Editor runable via CLI
  * 2014-08-27 - reimplement the CLI, today only for Dragon32/64 and CoCo
  * 2014-08-27 - WIP: move startup code
  * 2014-08-27 - move machine.py
  * 2014-08-27 - typo in README
  * 2014-08-27 - add history to README
  * 2014-08-27 - Bugfix: CoCo used the same default start address
  * 2014-08-26 - split ROM cfg, so that it can be loaded more than one ROM file:
  * 2014-08-26 - only code formatting
  * 2014-08-26 - raise error if perifery return None
  * 2014-08-20 - bugfix example prompt
  * 2014-08-20 - add CoCo info to README
  * 2014-08-20 - CoCo used a other default program start address than dragon
  * 2014-08-20 - WIP: Support CoCo in editor
  * 2014-08-20 - do the ' <-> :' and ELSE <-> :ELSE replacement internaly
  * 2014-08-20 - Use the new BASIC parser - TODO: Code cleanup!
  * 2014-08-20 - convert line number to int
  * 2014-08-20 - rename format functions
  * 2014-08-20 - add a BASIC parser with unittests
  * 2014-08-20 - code formating
  * 2014-08-18 - Add TODO unittests
  * 2014-08-18 - Better debug output
  * 2014-08-18 - better log output while load/inject BASIC program
  * 2014-08-18 - catch exception in unitest while running CPU
  * 2014-08-18 - Bugfix: support ON...GOTO and ON...GOSUB in renumbering
  * 2014-08-17 - add another renum unittest +code cleanup
  * 2014-08-17 - add "renumber listing" tool in editor
  * 2014-08-17 - TODO: Don't replace reversed words into tokens in comments and strings.
  * 2014-08-17 - bugfix: 'Cfg' object has no attribute 'memory_word_middlewares'
  * 2014-08-16 - Bugfix in inject BASIC program:
  * 2014-08-16 - WIP: move dump/load stuff into editor
  * 2014-08-15 - WIP: start splitting project: add "dragonlib"
  * 2014-08-14 - disable logging for run all unittests
  * 2014-08-14 - Add extract BASIC program unittest
  * 2014-08-14 - bugfix unittest init
  * 2014-08-14 - Bugfix: skip unittests if d32.rom not exists
  * 2014-08-14 - Start unittests with Dragon 32 ROM ;)
  * 2014-08-13 - transfert BASIC listing from editor into RAM worked!!!
  * 2014-08-13 - create a base test case only with some assertments
  * 2014-08-13 - move signed routines and...
  * 2014-08-12 - WIP: convert BASIC code to tokens
  * 2014-08-12 - bugfix display BASIC code:
  * 2014-08-11 - WIP: BASIC editor...
  * 2014-08-10 - WIP: GUI communication with CPU
  * 2014-08-08 - disable PUSH log in CPU
  * 2014-08-08 - add %(processName)s %(threadName)s to default log formatter
  * 2014-08-07 - calculate cycles/sec in GUI
  * 2014-08-07 - WIP: change queue stuff to work also with PyPy
  * 2014-08-07 - move some currently not useable files
  * 2014-08-07 - Bugfix: accessing cpu.cycles in CPUStatusThread
  * 2014-08-07 - add DragonPy schematic in README
  * 2014-08-07 - better Queue communication:
  * 2014-08-07 - cleanup machine start stuff
  * 2014-08-07 - move CPU into seperate thread
  * 2014-08-06 - Support CoCo keyboard input!
  * 2014-08-06 - bugfix in memory middleware
  * 2014-08-06 - read first the high-byte
  * 2014-08-06 - Update code around "reset vector":
  * 2014-08-06 - use memory.add_write_byte_middleware() and not a "own display RAM"
  * 2014-08-06 - move periphery memory hocks directly into memory
  * 2014-08-06 - rename memory callbacks to middlewares and now they can manipulate the byte
  * 2014-08-05 - WIP: Add CoCo
  * 2014-08-05 - Add info about broken CLI
  * 2014-08-04 - ./Dragon64_test.py worked!
  * 2014-08-04 - ignore *.rom files
  * 2014-08-03 - move display_cycle_interval() into CPU
  * 2014-08-03 - WIP: Split byte/word in periphery
  * 2014-08-02 - add info to Dragon Keyboard
  * 2014-08-01 - WIP: Keyboard input seems to work basicly!!!
  * 2014-07-31 - add /InputOutput/keyboard.bas
  * 2014-07-30 - WIP: Keyboard input to PIA
  * 2014-07-29 - use bit utils in CPU, too.
  * 2014-07-29 - add utilities around bit manipulations
  * 2014-07-28 - use central logger
  * 2014-07-27 - Quick work-a-round for travis
  * 2014-07-27 - WIP: Dragon Text mode with D64
  * 2014-07-25 - Add a Dragon32_test.py
  * 2014-07-24 - multiprocessing.JoinableQueue() -> multiprocessing.Queue()
  * 2014-07-24 - update console test
  * 2014-07-24 - reimplement "--display-cycle"
  * 2014-07-24 - work-a-round for double log output
  * 2014-07-24 - Change queue.get() stuff
  * 2014-07-24 - remove concept files
  * 2014-07-23 - remove obsolete text
  * 2014-07-23 - use global log
  * 2014-07-23 - use multiprocessing.JoinableQueue
  * 2014-07-23 - add names
  * 2014-07-23 - call cpu.quit()
  * 2014-07-23 - WIP: Merge Bus read & write Threads. Use thread.interrupt_main()
  * 2014-07-22 - WIP: KeyboardInterrupt
  * 2014-07-20 - WIP: sbc09 console
  * 2014-07-20 - Bugfix exit all threads/processes
  * 2014-07-20 - don't add more then one log handler
  * 2014-07-18 - unify "running" stuff
  * 2014-07-18 - rename multiprocess files
  * 2014-07-18 - code cleanup, use Simple6809Cfg as default, add '--dont_open_webbrowser'
  * 2014-07-18 - WIP: Simple6809 is running
  * 2014-07-17 - move CPU into components
  * 2014-07-17 - WIP: split concept code
  * 2014-07-17 - WIP: multiprocessing concept 2
  * 2014-07-17 - WIP: new multiprocessing concept
  * 2014-07-17 - just rename
  * 2014-07-17 - use multiprocessing under linux and subprocess unter windows
  * 2014-07-17 - WIP: Use multiprocessing to start CPU
  * 2014-07-17 - move CPU http server into a seperate thread.
  * 2014-07-17 - Bugfix CPU status
  * 2014-07-16 - remove loop stuff and use more threading
  * 2014-07-16 - Recalculate the op call burst_count
  * 2014-07-16 - That's fixed with pager ;)
  * 2014-07-16 - Use pager to get the user input.
  * 2014-07-16 - remove unused code
  * 2014-07-15 - add a console version of Simple6809 ROM without bus communication
  * 2014-07-15 - remove unused code & update README
  * 2014-07-15 - add complete DAA unittest
  * 2014-07-15 - display output is a good idea ;)
  * 2014-07-15 - Add unittest for DAA
  * 2014-07-15 - refactor DAA
  * 2014-07-15 - Bugfix DAA - TODO: Add unittests for it!
  * 2014-07-15 - moved
  * 2014-07-14 - Bugfix sbc09 unittest and add more sbc09 tests
  * 2014-07-14 - WIP: unittests with sbc09
  * 2014-07-14 - WIP: New call instruction implementation
  * 2014-07-14 - Bugfix: is needes, e.g.: in sbc09
  * 2014-07-14 - remove some test assert statements
  * 2014-07-14 - rename some pointer
  * 2014-07-14 - travis should only test master and stable
  * 2014-07-13 - remove speedup Simple6809 RAM test
  * 2014-07-13 - disable many logging lines
  * 2014-07-13 - set cc flags more than Xroar on startup
  * 2014-07-13 - merge some code in humanize.py
  * 2014-07-13 - move trace code:
  * 2014-07-13 - remove unused stuff
  * 2014-07-13 - remove "--compare_trace" adn update README
  * 2014-07-13 - Fix Travis
  * 2014-07-13 - boring in unittests ;)
  * 2014-07-13 - remo area debug and code cleanup
  * 2014-07-13 - test with pypy, too and diable coveralls
  * 2014-07-13 - Add some Dragon32 mem info
  * 2014-07-13 - Bugfix ASR/LSR: Bit seven is held constant. Catched with BASIC INT()
  * 2014-07-13 - Update unittest for TFR/EXG
  * 2014-07-13 - Bugfix: TFR and EXG
  * 2014-07-13 - add sixxie and tormod
  * 2014-07-13 - Bugfix INC
  * 2014-07-12 - add log to file
  * 2014-07-12 - add comments +typo
  * 2014-07-12 - better info on out of range writes
  * 2014-07-12 - add doctest
  * 2014-07-12 - Bugfix ADC... the last Bug???
  * 2014-07-11 - Add a working test for "FPA0_to_D"
  * 2014-07-11 - better debugging, add addr info after debug line
  * 2014-07-11 - Add some thanks...
  * 2014-07-11 - Just for devloper to play a little bit with the BASIC Interpreter.
  * 2014-07-11 - cleanup BASIC09 tests
  * 2014-07-09 - Add CLI to xroar filter script and add README
  * 2014-07-08 - update dev. tool
  * 2014-07-08 - merged "Programm Flow Instructions"
  * 2014-07-08 - add call number and datetime in HTML debug
  * 2014-07-07 - WIP: Test around BASIC floating point routines
  * 2014-07-07 - remove debug stuff and add a "debug.html" tracing generator
  * 2014-07-07 - update html opcode genrator script and add html file.
  * 2014-07-06 - WIP: 6809 data to html export
  * 2014-07-06 - disable open webbrower
  * 2014-07-06 - Add a memory callback functionality
  * 2014-07-04 - update division code
  * 2014-07-04 - add test for ROL,ROR in memory
  * 2014-07-04 - Bugfix CLI
  * 2014-07-03 - Bugfix ASR and add unittests for it.
  * 2014-07-03 - just move to group
  * 2014-07-03 - .gitignore
  * 2014-07-03 - add missing unittests after coverage run
  * 2014-07-03 - Test BASIC Interpreter works!
  * 2014-07-03 - WIP: Run tests with a alive BASIC Interpreter
  * 2014-07-03 - update cfg files
  * 2014-07-03 - add "create coverage report" in README
  * 2014-07-03 - remove syntax error in obsolete file
  * 2014-07-03 - bugfix coverage packagename
  * 2014-07-03 - change all package path, after file move
  * 2014-07-03 - moved all files into dragonpy package dir
  * 2014-07-03 - add packagename
  * 2014-07-03 - add coveralls in travis cfg.
  * 2014-07-03 - change TODO info in unittets
  * 2014-07-03 - add coveralls.io status image in README
  * 2014-07-03 - add coveralls cfg
  * 2014-07-03 - add unittest info in README
  * 2014-07-03 - add setup.py and travis cfg.
  * 2014-07-03 - better "first tim called" debug info.
  * 2014-07-03 - add unittest for SUBA indexed
  * 2014-07-03 - Update division test code
  * 2014-07-02 - WIP: ea indexed address modes
  * 2014-07-02 - Display CWAI not implemented error
  * 2014-07-02 - better error message
  * 2014-07-02 - refactor TFR, EXG stuff and add unittests
  * 2014-07-02 - add more Indexed tests
  * 2014-07-02 - typo
  * 2014-07-02 - add second division test code
  * 2014-07-02 - add seperate test for address modes
  * 2014-07-02 - group ST/LD and add unittests
  * 2014-07-02 - remove comment: it's correct
  * 2014-07-02 - move all not implemented ops
  * 2014-07-01 - bugfix EOR - TODO: Add a test for it.
  * 2014-07-01 - test with more interesting areas
  * 2014-07-01 - add test for ABX
  * 2014-07-01 - refactor ANDCC and ORCC
  * 2014-07-01 - add test for ORCC and ANDCC
  * 2014-07-01 - update example output
  * 2014-07-01 - reorder crc32 tests
  * 2014-07-01 - Bugfix for failed test.
  * 2014-07-01 - Update crc32 test. Works now!
  * 2014-07-01 - disable prints
  * 2014-07-01 - moved/grouped some ops
  * 2014-07-01 - Bugfix ROR and add unittest for it.
  * 2014-07-01 - WIP: add crc32 code
  * 2014-06-30 - Add division code test
  * 2014-06-30 - WIP: 6809 32/16 divison test
  * 2014-06-30 - nicer debug output
  * 2014-06-30 - add unittests for PSHU and PULU
  * 2014-06-30 - Start to add 6809 unittests with small assembler programs: crc16
  * 2014-06-30 - bugfix Push/Pull unittests
  * 2014-06-30 - add unittest for BLT and LBLT
  * 2014-06-30 - add unittest for SBCA
  * 2014-06-30 - move DEC test
  * 2014-06-29 - split/merge arithmetic shift tests
  * 2014-06-29 - unify: r & 0xff
  * 2014-06-29 - split arithmetic op tests
  * 2014-06-29 - comment debug output
  * 2014-06-29 - add unittest for ADDD and DECA
  * 2014-06-28 - Add test for ROL
  * 2014-06-28 - cleanup ADD and add unittest
  * 2014-06-28 - disallow out of range write into memory
  * 2014-06-28 - implement BRN, BVC and BVS
  * 2014-06-28 - Bugfix INC and add unittests
  * 2014-06-28 - add LSLA unittest
  * 2014-06-28 - split branch unittests
  * 2014-06-28 - code cleanup and add unittests for CMP
  * 2014-06-27 - Use only 1KB RAM for Simple6809, too.
  * 2014-06-27 - add hacked script for copy&paste .lst content from e.g.: http://www.asm80.com/
  * 2014-06-27 - WIP CPU control server
  * 2014-06-27 - add unittest for NEG memory
  * 2014-06-27 - Update NEG memory, TODO: add tests for it, too.
  * 2014-06-27 - Add complete range unittests for update_HNZVC_8
  * 2014-06-27 - bugfix unittest file
  * 2014-06-27 - Bugfix NEGA and NEGB and update unitests for them
  * 2014-06-27 - update unittest code
  * 2014-06-27 - update accu unittests
  * 2014-06-26 - add unittest for ORA and ORCC
  * 2014-06-26 - Add unittests for BPL and LBPL
  * 2014-06-26 - bugfix for /debug/
  * 2014-06-26 - Add unittests for LEAU and LDU
  * 2014-06-26 - Bugfix TST extended
  * 2014-06-26 - Bugfix in TST and add unittest for it
  * 2014-06-26 - Bugfix BGE
  * 2014-06-25 - add another simple test code
  * 2014-06-25 - add come cary flag tests
  * 2014-06-25 - Add Zero-Flag tests
  * 2014-06-25 - add a test code, use test config
  * 2014-06-24 - WIP: turn on DEBUG via POST request
  * 2014-06-24 - move tests TODO: Update all
  * 2014-06-24 - Better "called the first time:" info line.
  * 2014-06-24 - add info about ROMs
  * 2014-06-24 - README Update
  * 2014-06-23 - change reset debug output
  * 2013-10-31 - somthing wrong in dragon cycle/update calls ?!?
  * 2013-10-31 - commit current state:
  * 2013-10-31 - insert TODOs update README
  * 2013-10-31 - refactor:
  * 2013-10-30 - merge periphery code
  * 2013-10-30 - exit if Pygame is not installed
  * 2013-10-30 - implement MUL
  * 2013-10-30 - truncate long lines in traceback
  * 2013-10-29 - add a simple console, so it's runable without TKinter
  * 2013-10-29 - add cfg.BURST_COUNT
  * 2013-10-29 - display error info on exit
  * 2013-10-29 - update with removed logging output
  * 2013-10-29 - disable many logging output
  * 2013-10-28 - add a note about current performace
  * 2013-10-28 - pygame, numpy is not needed in every config
  * 2013-10-27 - convert chars to display, why?
  * 2013-10-27 - deactivate "sys exit" on trace difference
  * 2013-10-27 - implement SEX
  * 2013-10-27 - add update_HNZVC_16()
  * 2013-10-27 - update half-carry, though H is normaly "undefined"
  * 2013-10-27 - add hacked scb09 trace compare
  * 2013-10-27 - Bugfix CMP: update half-carry flag, too.
  * 2013-10-27 - add Lennart Benschop 6809 stuff (released under the GPL)
  * 2013-10-26 - Implement DAA, EXG and bugfix LSR
  * 2013-10-26 - bugfix activate logging later
  * 2013-10-26 - Bugfix in data: EXG need postbyte
  * 2013-10-26 - add current example
  * 2013-10-26 - display key events
  * 2013-10-25 - less debug output
  * 2013-10-25 - add LSL unittest
  * 2013-10-25 - add ANDA unittest
  * 2013-10-25 - add a unittest with a routine from origin ROM
  * 2013-10-24 - Update some CC handling.
  * 2013-10-24 - add CC unittest with DEC and update other tests
  * 2013-10-24 - Add CC unittest with INC
  * 2013-10-24 - Bugfix SUB and add a working unittest for SUB and CC flags
  * 2013-10-24 - first real working CC test with ADDA
  * 2013-10-23 - display first call
  * 2013-10-23 - Bugfix: set CC flags only if not set before
  * 2013-10-23 - don't raise if error was before and better debug messages
  * 2013-10-22 - nicer TK window
  * 2013-10-22 - some updates in unittest
  * 2013-10-22 - better trace compare
  * 2013-10-22 - use XRoar CC code
  * 2013-10-22 - Update exported 6809 data:
  * 2013-10-22 - nicer output + add screenshot
  * 2013-10-21 - wrap around value
  * 2013-10-21 - add CC tests.
  * 2013-10-21 - change debug output
  * 2013-10-21 - update unittest
  * 2013-10-21 - add --area_debug_cycles
  * 2013-10-21 - merge SUB8 and SUB16
  * 2013-10-21 - Implement BGE and BLT
  * 2013-10-21 - bugfix address modes
  * 2013-10-21 - use delimiter=';'
  * 2013-10-21 - use csv modul for export
  * 2013-10-21 - update state in README
  * 2013-10-21 - implement ANDCC
  * 2013-10-21 - bugfix get ea+m DIRECT
  * 2013-10-21 - TST need mem
  * 2013-10-21 - add new csv
  * 2013-10-21 - Add undocumented RESET opcode 0x3e
  * 2013-10-21 - data updates:
  * 2013-10-21 - remove stuff for stack pointer checks
  * 2013-10-21 - more debug info from get_ea_indexed()
  * 2013-10-21 - remove internal push/pull check:
  * 2013-10-21 - updates for new 6809 data
  * 2013-10-21 - bugfix TFR, JSR data
  * 2013-10-21 - ea is needed if write to memory
  * 2013-10-21 - * "needs_ea" is not the same for all ops
  * 2013-10-21 - needs_ea for all branch instructions
  * 2013-10-21 - add "needs_ea"
  * 2013-10-21 - rename "operand" to "register"
  * 2013-10-21 - remove "addr mode" register and stack
  * 2013-10-21 - manual changes for "reads from memory" info
  * 2013-10-21 - move HNZVC info from instruction to op code
  * 2013-10-21 - add a note about read_from_memory
  * 2013-10-20 - start to use the new data. Not ready, yet.
  * 2013-10-20 - change "-" to None
  * 2013-10-20 - generate a new op code info file
  * 2013-10-20 - merge with existing information
  * 2013-10-19 - pretty print the result, too.
  * 2013-10-19 - try to collect all data in a new way.
  * 2013-10-19 - add missing instructions
  * 2013-10-18 - add op info
  * 2013-10-17 - TODO: change 6809 data py
  * 2013-10-17 - long branches allways MEM_ACCESS_WORD
  * 2013-10-17 - more info on push/pull
  * 2013-10-17 - implement BGT
  * 2013-10-17 - stop on endless loops and merge code
  * 2013-10-17 - bugfix in get_indexed_ea()
  * 2013-10-17 - bugfix in stack count check
  * 2013-10-17 - info if mem info is not active
  * 2013-10-17 - * implement ABX, ASR, BLE, EOR, LSR, NOP, ROR, SBC, SUB16
  * 2013-10-16 - add not working CC half carry test
  * 2013-10-16 - display char in memory write
  * 2013-10-16 - bugfix missing attribute
  * 2013-10-16 - add check
  * 2013-10-16 - bugfix ORCC and ROL
  * 2013-10-16 - implement OR
  * 2013-10-16 - bugfix for EOF if XRoar log file
  * 2013-10-16 - implement ADDD
  * 2013-10-16 - add a internal stack push/pull counter with check
  * 2013-10-16 - update CC
  * 2013-10-16 - bugfix TST
  * 2013-10-16 - Merge code for BSR and JSR
  * 2013-10-16 - rename half carry method
  * 2013-10-16 - less debug if value out of range
  * 2013-10-16 - remove raise in ORCC
  * 2013-10-16 - bugfix push/pull
  * 2013-10-16 - bugfix test_TFR03()
  * 2013-10-16 - stop on wrong NEG (e.g.: jump to empty RAM area)
  * 2013-10-16 - better traceback
  * 2013-10-16 - clear hacked exception
  * 2013-10-16 - for eclipse :(
  * 2013-10-15 - Update/bugfixes because of mem_read information
  * 2013-10-15 - display cycles/sec
  * 2013-10-15 - better error info
  * 2013-10-15 - more debug info in memory access
  * 2013-10-15 - add "mem_read" and "mem_write" into MC6809 data
  * 2013-10-15 - send op address over bus, too.
  * 2013-10-14 - bugfix BLO / BHS
  * 2013-10-14 - implement AND
  * 2013-10-14 - add content in "read byte" debug info
  * 2013-10-14 - implement INC memory
  * 2013-10-14 - Bugfix: wrong mem access PSH, PUL
  * 2013-10-13 - conmpare first the registers than CC
  * 2013-10-13 - debug output for CPU cycles
  * 2013-10-13 - Display CC debug like '.F.IN..C' and compare it seperate
  * 2013-10-13 - bugfix get_direct_byte()
  * 2013-10-13 - implement PULS
  * 2013-10-13 - nicer debugger output
  * 2013-10-13 - Bugfix BSR
  * 2013-10-13 - implement ORCC
  * 2013-10-12 - bugfix in IllegalInstruction
  * 2013-10-12 - add a simple debugger
  * 2013-10-12 - implement BHI
  * 2013-10-12 - reimplement illegal ops
  * 2013-10-12 - bugfix: Hacked bugtracking only with Dragon 32
  * 2013-10-12 - add addr in error message
  * 2013-10-12 - log mem access as info
  * 2013-10-12 - hacked speedup Simple6809 RAM test
  * 2013-10-12 - Hacked bugtracking only with Dragon 32
  * 2013-10-12 - insert CC in XRoar trace line, too
  * 2013-10-12 - use sam attr than XRoar in PAGE1/2 ops
  * 2013-10-12 - use debug.error for TODOs in PIA/SAM
  * 2013-10-12 - special RAM init for Dragon.
  * 2013-10-12 - Bugfix pull_word() (e.g. RTS)
  * 2013-10-12 - Bugfix BLS
  * 2013-10-12 - bugfix LEA
  * 2013-10-11 - add two more CC test files
  * 2013-10-11 - better opcode .csc export output
  * 2013-10-11 - fix unittest
  * 2013-10-11 - add screenshots
  * 2013-10-11 - Add BASIC programm: Test CC Registers
  * 2013-10-10 - add a hacked bug tracking: xroar trace compare
  * 2013-10-10 - bugfix BEQ
  * 2013-10-10 - bugfix in indexed addressing mode
  * 2013-10-10 - bugfix init value in PIA
  * 2013-10-10 - add reset call to debug output
  * 2013-10-10 - merge read pc byte/word methods
  * 2013-10-10 - Bugfix in log output: Display PC and not ea ;)
  * 2013-10-10 - Bugfix STA/STB and CC update
  * 2013-10-10 - debug also CC registers
  * 2013-10-10 - tweak --verbosity=20 output simmilar to XRoar -trace
  * 2013-10-10 - implement "--max" cli argument
  * 2013-10-09 - add "--area_debug_active" in CLI
  * 2013-10-09 - implement ADC and BSR
  * 2013-10-09 - return 0x0, while read/write outside memory
  * 2013-10-09 - split mem info:
  * 2013-10-09 - Add unittest
  * 2013-10-09 - commit idea for CC
  * 2013-10-09 - update CPU for new MC6809_data_raw:
  * 2013-10-09 - nicer output
  * 2013-10-09 - update 6809 data:
  * 2013-10-09 - CC register updates
  * 2013-10-08 - add tests für CC.H and CC.C, but's seems to be wrong?!?
  * 2013-10-08 - Update unittest, so they are runable
  * 2013-10-07 - Bugfix COM
  * 2013-10-07 - add CLI examples into README
  * 2013-10-07 - bugfix: it's the right position
  * 2013-10-07 - commit current state: * bus I/O: split byte/word calls * bus I/O: use struct for Sending responses from periphery back to memory * split memory from cpu module * start with Simple6809Periphery
  * 2013-10-07 - * Add support for more than Dragon setups. * Start adding Simple6809 support
  * 2013-10-06 - use bus for the rest
  * 2013-10-06 - use reset() to ser CC F&I and init PC
  * 2013-10-06 - implement support for PAGE1/2 opcodes
  * 2013-10-06 - remove old code
  * 2013-10-06 - implement CMP8 and CMP16
  * 2013-10-06 - set inital PC to RESET_VECTOR == 0xb3b4
  * 2013-10-06 - implement LEAS,LEAU and LEAX, LEAY
  * 2013-10-06 - Set start stack pointer to 0xffff
  * 2013-10-06 - *wrap around 8/16-bit register values
  * 2013-10-06 - revert S to object: So it's the same API than other register objects
  * 2013-10-06 - add everywhere "m" argument
  * 2013-10-06 - * Implement LSL / ROL
  * 2013-10-06 - implement BMI, BPL
  * 2013-10-06 - update unittests (work in progress)
  * 2013-10-06 - * Implement JSR
  * 2013-10-06 - implement BLO/BCS/LBLO/LBCS and BHS/BCC/LBHS/LBCC branch
  * 2013-10-06 - bugfix direct byte - TODO: direct word
  * 2013-10-06 - Implement ST16 + Bugfix ST8
  * 2013-10-06 - reformat DocString
  * 2013-10-05 - implement BRA/LBRA
  * 2013-10-04 - stop before loop
  * 2013-10-04 - bugfix BNE and JMP
  * 2013-10-04 - start a simple memory hex viewer
  * 2013-10-03 - Add unittest for LDA, LDB, STA, STB and LDD in one test
  * 2013-10-03 - Bugfix m <-> ea missmatch in address methods
  * 2013-10-03 - * Implement ADD8
  * 2013-10-03 - add a low-level-register test
  * 2013-10-03 - remove some init debug messages
  * 2013-10-02 - start implementing SUB8
  * 2013-10-02 - * bugfix: differ between ea and memory content * Implement NEG memory
  * 2013-10-01 - starts implementing NEG, but seems to be buggy :(
  * 2013-10-01 - remove many startup debug output
  * 2013-10-01 - add name to ConditionCodeRegister for uniform API
  * 2013-10-01 - bugfix missing API update
  * 2013-10-01 - reimplement TFR
  * 2013-10-01 - implement TST
  * 2013-10-01 - * Implement BEQ * use same debug output in BNE
  * 2013-10-01 - Implement BIT
  * 2013-10-01 - implement BNE
  * 2013-10-01 - implement "relative" addressing mode
  * 2013-09-30 - add a test
  * 2013-09-30 - check mem values and make 'end' optional
  * 2013-09-30 - implement INC
  * 2013-09-30 - don't set overflow flag back to 0
  * 2013-09-24 - reimplement LD8
  * 2013-09-24 - implement DEC
  * 2013-09-24 - use new skeleton
  * 2013-09-24 - * don't split instrutions
  * 2013-09-24 - * split COM * implement COM
  * 2013-09-24 - * merge accu/CC code * all registers are objects with get()/set() method * leave unimplemented methods in skeleton class * reimplement JMP, LD16, ST8
  * 2013-09-24 - mark 8bit CC update methods
  * 2013-09-24 - rename CC calls
  * 2013-09-23 - start LD16: TODO: operand should be a object with get/set methods!
  * 2013-09-23 - implement JMP
  * 2013-09-23 - insert genereted code
  * 2013-09-23 - bigfix ;)
  * 2013-09-23 - change CSV data
  * 2013-09-23 - Use variables in "addr_mode"
  * 2013-09-23 - rename dir
  * 2013-09-23 - * insert 'cc update' calls for the most cases * better DocString * change function signature if nessesary *
  * 2013-09-23 - * split LEA * move cc bits info to INSTRUCTION_INFO
  * 2013-09-23 - add a simple CSV export
  * 2013-09-23 - Use also first and last part to link
  * 2013-09-23 - reimplement skeleton maker script
  * 2013-09-23 - * change cycles/bytes to integers * Merge PAGE and SWI
  * 2013-09-20 - merge informations, current result is MC6809_data_raw.py
  * 2013-09-20 - add hacked 6809 data scraping scripts.
  * 2013-09-19 - don't use property witch access methods...
  * 2013-09-19 - * Bugfix NEG * stop in soft witch
  * 2013-09-19 - * support JMP, NEG in all addressing modes * inc cycles in Memory class
  * 2013-09-19 - * change memory access methods to properties, so it's unify with register access * merge COM ops
  * 2013-09-19 - COM
  * 2013-09-19 - add to TODO ;)
  * 2013-09-19 - uniform debug output
  * 2013-09-18 - * move accumulator to seperate object
  * 2013-09-18 - remove register from 6309 and add some more links.
  * 2013-09-17 - * Add LD 8-bit load register from memory * move the CC frags into seperate module
  * 2013-09-17 - add "LD 16-bit load register from memory" and merge code with ST16
  * 2013-09-17 - check if ops only defined one time
  * 2013-09-17 - accumulator D, W and Q as property
  * 2013-09-17 - add ST 16-bit store register into memory
  * 2013-09-17 - add some 8-bit arithmetic operations
  * 2013-09-17 - debug write to text screen addresses
  * 2013-09-17 - add LSR
  * 2013-09-17 - add ORA
  * 2013-09-17 - bugfix indexed addressing modes
  * 2013-09-16 - add BNE
  * 2013-09-16 - make current opcode class wide. Handle list of opcodes
  * 2013-09-16 - FIXME: word and signed8 ???
  * 2013-09-16 - add copyright notes
  * 2013-09-16 - form if...elif to a dict access
  * 2013-09-16 - add LEAX indexed
  * 2013-09-16 - add Indexed addressing modes, but needs tests
  * 2013-09-16 - short debug output
  * 2013-09-16 - stop on illegal ops
  * 2013-09-15 - little-endian or big-endian ?!?!
  * 2013-09-12 - better unittest output in verbosity mode
  * 2013-09-11 - Display more mem info
  * 2013-09-11 - add ADDA extended, CMPX extended and JSR extended
  * 2013-09-11 - bugfix ROM/RAM size
  * 2013-09-11 - Change sizes, but: http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4363
  * 2013-09-11 - Add print_debug_info() to config class
  * 2013-09-11 - add op 0x00 NEG direct
  * 2013-09-11 - set cycles in ops
  * 2013-09-11 - add JMP
  * 2013-09-11 - rename CC flags
  * 2013-09-11 - setup logging
  * 2013-09-11 - move STACK_PAGE and RESET_VECTOR into cfg
  * 2013-09-11 - remove read_word_bug()
  * 2013-09-10 - cleanup and start to implement the 6809 CPU
  * 2013-08-29 - Update configs.py
  * 2013-08-27 - add some links
  * 2013-08-27 - fork and rename some files, change some settings... But will every be a Dragon 32 emulator?
  * 2013-08-20 - move files
  * 2013-08-20 - Initial commit
  * 2013-08-19 - Use MAX_HZ_VARIATION to seperate bit 1 or bit 0 display some statistics of bit detection
  * 2013-08-18 - add status while reading WAV file.
  * 2013-08-15 - add a script to convert dragon 32 Cassetts WAV files into plain text.
  * 2013-03-08 - added note about exact pip and brew commands I used
  * 2013-03-08 - improved hires colour, fixed non-ASCII key crash, fixed to work with later pygame/numpy
  * 2012-07-23 - added explicit mention of License in README
  * 2012-07-23 - added mention of numpy requirement
  * 2012-07-23 - added MIT license
  * 2012-07-23 - treat README as Markdown
  * 2012-04-18 - made applepy.py executable
  * 2011-10-01 - add --pc switch for starting run at specific program counter
  * 2011-10-01 - initialise display state variables in constructor
  * 2011-08-21 - add console control utility
  * 2011-08-21 - implement post to /memory in control requests
  * 2011-08-20 - control channel is now HTTP/REST/JSON
  * 2011-08-20 - add fileno() method to ControlHandler for better compatiblity with select()
  * 2011-08-20 - disassemble show instruction bytes
  * 2011-08-20 - reincarnate disassembler on control channel
  * 2011-08-20 - add dump memory command
  * 2011-08-20 - refactor control command processing
  * 2011-08-19 - start of cpu core control channel
  * 2011-08-19 - graceful shutdown if cpu core exits
  * 2011-08-19 - abandon startup if cpu module does not start
  * 2011-08-19 - rename --ui switch to --bus
  * 2011-08-18 - open memory files in binary mode
  * 2011-08-18 - update curses UI for socket comms
  * 2011-08-18 - use sockets for comms instead of stdio
  * 2011-08-19 - Edited README via GitHub
  * 2011-08-19 - Mention the minimal applepy_curses.py in README
  * 2011-08-16 - attempt to skip to data part of tape
  * 2011-08-16 - finish cassette support
  * 2011-08-16 - initial cassette input
  * 2011-08-14 - Separate CPU core and UI processes
  * 2011-08-15 - removed unused import
  * 2011-08-15 - adjusted speaker sample length to allow for leading edge
  * 2011-08-15 - made options...um...optional param to Memory so tests pass
  * 2011-08-15 - command line options: --rom, --ram, --quiet
  * 2011-08-15 - map left/right arrow keys to ^H/^U
  * 2011-08-15 - add flash attribute to text mode
  * 2011-08-15 - moved speaker buffer playing into the Speaker class
  * 2011-08-15 - implemented speaker; not a bad hack :-)
  * 2011-08-15 - pass in None for cycles so tests run
  * 2011-08-15 - refactored memory access so cycle can be passed in
  * 2011-08-14 - implemented cycle calculation (except for page boundary crossing)
  * 2011-08-14 - added notes on implementation that seems to give the right result
  * 2011-08-14 - more groking of why memory-based ASL, DEC, INC, LSR, ROL and ROR take what they take
  * 2011-08-14 - worked out why STA seemed an exception
  * 2011-08-14 - updated notes, fixing what seems to a mistake on the webpage I referenced
  * 2011-08-14 - typo and formatting fixes in cycle notes
  * 2011-08-14 - notes on cycle times
  * 2011-08-14 - added test_run to run CPU over a fragment of memory with no UI event handling (for automated testings)
  * 2011-08-14 - improved coloured for better whites
  * 2011-08-13 - fixed missing self
  * 2011-08-13 - refactored memory so RAM just subclasses ROM, adding write_byte
  * 2011-08-13 - whitespace nits
  * 2011-08-13 - added load_file to RAM
  * 2011-08-13 - updated README credits and status
  * 2011-08-13 - implemented HIRES colour
  * 2011-08-13 - use pregenerated character bitmaps for text mode
  * 2011-08-13 - added HIRES graphics support based on code from ghewgill: https://github.com/ghewgill/applepy/commit/5aa8ca2caa82cacdae08d0ffdbab2083b0f4c7a1
  * 2011-08-13 - always draw the spaces between scanlines
  * 2011-08-13 - in mixed mode, assume monitor is colour
  * 2011-08-13 - refactored update_text and update_lores into a single method
  * 2011-08-13 - display full width of characters
  * 2011-08-13 - character heights are really 8 not 9
  * 2011-08-13 - implemented LORES graphics
  * 2011-08-13 - make display optional (for testing)
  * 2011-08-13 - got tests working again after memory refactor
  * 2011-08-13 - ported to pygame and added bit-accurate characters
  * 2011-08-07 - if writing to text screen row group 3 just skip instead of throwing exception
  * 2011-08-07 - updated README to reflect status and give credit
  * 2011-08-07 - don't treat indices as signed in indexed addressing modes (ht: ghewgill)
  * 2011-08-07 - consistent whitespace
  * 2011-08-07 - split memory handling into separate classes for RAM, ROM and Soft Switches
  * 2011-08-07 - add disassembler, enable for dump mode
  * 2011-08-07 - don't allow writes to ROM area (this caused the ][+ ROM to hang on boot)
  * 2011-08-07 - fix typos for zero_page_y_mode in instruction dispatch table
  * 2011-08-07 - fix dump() function so it works (when uncommented)
  * 2011-08-07 - fix typo in instruction table
  * 2011-08-07 - simplify calculating signed values in adc and sbc
  * 2011-08-07 - only need to allocate 64k of memory
  * 2011-08-07 - if curses can't write a character to the screen, just skip it; fixes #1
  * 2011-08-07 - improved implementation of indirect bug across page boundaries including indexed indirects as well
  * 2011-08-07 - added unit tests
  * 2011-08-07 - fixed error in BVS
  * 2011-08-07 - whitespace nit
  * 2011-08-07 - properly use 0 and 1 not False and True for flags
  * 2011-08-07 - implemented non-accumulator version of ROR
  * 2011-08-06 - fixed inverse use of carry in SBC
  * 2011-08-06 - turns out PLA DOES affect NZ after all
  * 2011-08-06 - renamed load to load_file, added a load to load memory from byte list and refactored loading code
  * 2011-08-06 - emulate indirect mode bug in 6502
  * 2011-08-06 - reimplemented CMP, CPX and CPY based on 2006/2007 code
  * 2011-08-06 - reimplemented ADC and SBC based on 2006/2007 code
  * 2011-08-06 - apparently PLA does not affect NZ flags
  * 2011-08-06 - little BIT of simplication
  * 2011-08-06 - cleaned up ASL implementation
  * 2011-08-06 - TSX updated NZ flags
  * 2011-08-06 - fixed stray comment
  * 2011-08-06 - factored out stack pull/push
  * 2011-08-06 - refactored flags to status byte and back
  * 2011-08-06 - slight refactor of update_nz and update_nzc
  * 2011-08-06 - implemented BRK and RTI
  * 2011-08-06 - make further use of addressing mode refactor
  * 2011-08-06 - added zero_page_y_mode
  * 2011-08-06 - added wrap-around for zero_page_x_mode
  * 2011-08-06 - refactored addressing mode code
  * 2011-08-06 - added if __name__ == "__main__" test for mainline
  * 2011-08-06 - simplified screen address to col/row translation based on code from 2006
  * 2011-08-06 - initial update from 2001 code

</details>


[comment]: <> (✂✂✂ auto generated history end ✂✂✂)


## donation


* [Flattr This!](https://flattr.com/submit/auto?uid=jedie&url=https%3A%2F%2Fgithub.com%2F6809%2FMC6809%2F)
* Send [Bitcoins](http://www.bitcoin.org/) to [1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F](https://blockexplorer.com/address/1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F)
