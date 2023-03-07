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

```bash
~$ git clone https://github.com/jedie/DragonPy.git
~$ cd DragonPy/
~/DragonPy$ ./cli.py --help
```

The output of `./cli.py --help` looks like:

[comment]: <> (✂✂✂ auto generated main help start ✂✂✂)
```
Usage: ./cli.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ benchmark                   Run a MC6809 emulation benchmark                                     │
│ check-code-style            Check code style by calling darker + flake8                          │
│ coverage                    Run and show coverage.                                               │
│ fix-code-style              Fix code style of all MC6809 source code files via darker            │
│ install                     Run pip-sync and install 'MC6809' via pip as editable.               │
│ mypy                        Run Mypy (configured in pyproject.toml)                              │
│ profile                     Profile the MC6809 emulation benchmark                               │
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
[comment]: <> (✂✂✂ auto generated main help end ✂✂✂)




You can use the devshell as a CLI, too, e.g.:
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



### tests

```bash
~/DragonPy$ ./cli.py coverage
# or just:
~/DragonPy$ ./cli.py test
# or with different Python versions:
~/DragonPy$ ./cli.py tox
```

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


### TODO


* Update 'cpu6809_html_debug.py'
* Use bottle for http control server part
* unimplemented OPs:
  * RESET
  * SWI / SWI2 / SWI3
  * SYNC


## History

(Some of the points are related to [DragonPy Emulator](https://github.com/jedie/DragonPy))


* [*dev*](https://github.com/6809/MC6809/compare/v0.7.0...main)
  * TBC
* 07.03.2023 - [v0.7.0](https://github.com/6809/MC6809/compare/v0.6.0...v0.7.0)
  * Replace the `Makefile` with a click CLI
  * Use pip-tools and https://github.com/jedie/manageprojects
  * Rename git `master` to `main` branch
  * Run CI tests against Python 3.9, 3.10 and 3.11
  * Replace Creole README with markdown
* 10.02.2020 - [v0.6.0](https://github.com/6809/MC6809/compare/v0.5.0...v0.6.0)
  * modernize project and sources
  * skip support for Python 2
  * minimal Python v3.6
* 19.10.2015 - [v0.5.0](https://github.com/6809/MC6809/compare/v0.4.6...v0.5.0)
  * Split CPU with mixin inheritance
  * Optimizing:
    * remove `.get()` function calls from registers
    * move Condition Code Register (CC) into CPU via mixin class
  * Bugfix TFR and EXG by _convert_differend_width()_
  * Run DragonPy unittests on travis CI, too.
* 24.08.2015 - [v0.4.6](https://github.com/6809/MC6809/compare/v0.4.5...v0.4.6)
  * Add a "max_delay", to fix the "freeze" after a speed limit change
  * rename some of the "speed limit" variables
* 21.08.2015 - [v0.4.5](https://github.com/6809/MC6809/compare/v0.4.4...v0.4.5)
  * deactivate 'cpu6809_html_debug.py' - TODO: update it!
  * update cli unittests
  * update README and code cleanup
* 10.08.2015 - [v0.4.4](https://github.com/6809/MC6809/compare/v0.4.3...v0.4.4) - bugfix and cleanup the tests
* 10.08.2015 - [v0.4.3](https://github.com/6809/MC6809/compare/v0.4.2...v0.4.3) - run unittests with nose
* 27.05.2015 - [v0.4.2](https://github.com/6809/MC6809/compare/v0.4.1...v0.4.2) - Add MC6809/example6809.py
* 26.05.2015 - [v0.4.0, 0.4.1](https://github.com/6809/MC6809/compare/1a40593...v0.4.1) - Split MC6809 from [DragonPy](https://github.com/jedie/DragonPy)
* 22.09.2014 - Remove hacked CPU skeleton generator scripts with [commit ac903a8f](https://github.com/6809/MC6809/commit/ac903a8fb9f02e1db23172cb367af2581d4b29a1)
* 14.09.2014 - Release v0.2.0 - Add a speedlimit, config dialog and IRQ: [Forum post 11780](http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&p=11780#p11780)
* 05.09.2014 - Release v0.1.0 - Implement pause/resume, hard-/soft-reset 6809 in GUI and improve a little the GUI/Editor stuff: [v0.1.0](https://github.com/jedie/DragonPy/releases/tag/v0.1.0) see also: [Forum post 11719](http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&p=11719#p11719).
* 27.08.2014 - Run CoCo with Extended Color Basic v1.1, bugfix transfer BASIC Listing with [8fe24e5...697d39e](https://github.com/jedie/DragonPy/compare/8fe24e5...697d39e) see: [Forum post 11696](http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=90#p11696).
* 20.08.2014 - rudimenary BASIC IDE works with [7e0f16630...ce12148](https://github.com/jedie/DragonPy/compare/7e0f16630...ce12148), see also: [Forum post 11645](http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=8&t=4439#p11645).
* 05.08.2014 - Start to support CoCo, too with [0df724b](https://github.com/jedie/DragonPy/commit/0df724b3ee9d87088b524c3623040a41e9772eb4), see also: [Forum post 11573](http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=80#p11573).
* 04.08.2014 - Use the origin Pixel-Font with Tkinter GUI, see: [Forum post 4909](http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4909) and [Forum post 11570](http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=80#p11570).
* 27.07.2014 - Copyrigth info from Dragon 64 ROM is alive with [543275b](https://github.com/jedie/DragonPy/commit/543275b1b90824b64b67dcd003cc5ab54296fc15), see: [Forum post 11524](http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=80#p11524).
* 29.06.2014 - First "HELLO WORLD" works, see: [Forum post 11283](http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=70#p11283).
* 27.10.2013 - "sbc09" ROM works wuite well almist, see: [Forum post 9752](http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=60#p9752).
* 16.10.2013 - See copyright info from "Simple6809" ROM with [25a97b6](https://github.com/jedie/DragonPy/tree/25a97b66d8567ba7c3a5b646e4a807b816a0e376) see also: [Forum post 9654](http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=50#p9654).
* 10.09.2013 - Start to implement the 6809 CPU with [591d2ed](https://github.com/jedie/DragonPy/commit/591d2ed2b6f1a5f913c14e56e1e37f5870510b0d)
* 28.08.2013 - Fork "Apple ][ Emulator" written in Python: [https://github.com/jtauber/applepy](https://github.com/jtauber/applepy) to [https://github.com/jedie/DragonPy](https://github.com/jedie/DragonPy)


## donation


* [Flattr This!](https://flattr.com/submit/auto?uid=jedie&url=https%3A%2F%2Fgithub.com%2F6809%2FMC6809%2F)
* Send [Bitcoins](http://www.bitcoin.org/) to [1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F](https://blockexplorer.com/address/1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F)
