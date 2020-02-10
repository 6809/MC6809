-------------------------------------
MC6809 CPU emulator written in Python
-------------------------------------

MC6809 is a Open source (GPL v3 or later) emulator for the legendary **6809** CPU, used old homecomputer `Dragon 32/64 <https://en.wikipedia.org/wiki/Dragon_32/64>`_ and `Tandy TRS-80 Color Computer (CoCo) <https://en.wikipedia.org/wiki/TRS-80_Color_Computer>`_ built in the 1980s...

Tested with Python 3.6, 3.7, 3.8 and PyPy3

+-----------------------------------+-------------------------------+
| |Build Status on travis-ci.org|   | `travis-ci.org/6809/MC6809`_  |
+-----------------------------------+-------------------------------+
| |Coverage Status on coveralls.io| | `coveralls.io/r/6809/MC6809`_ |
+-----------------------------------+-------------------------------+

.. |Build Status on travis-ci.org| image:: https://travis-ci.org/6809/MC6809.svg?branch=master
.. _travis-ci.org/6809/MC6809: https://travis-ci.org/6809/MC6809/
.. |Coverage Status on coveralls.io| image:: https://coveralls.io/repos/6809/MC6809/badge.svg
.. _coveralls.io/r/6809/MC6809: https://coveralls.io/r/6809/MC6809

A example usage can be find in: `MC6809/example6809.py <https://github.com/6809/MC6809/blob/master/MC6809/example6809.py>`_

usage:

::

    ~$ python3 -m venv MC6809
    ~$ cd MC6809
    ~/MC6809 $ source bin/activate
    (MC6809) ~/MC6809 $ pip3 install MC6809
    (MC6809) ~/MC6809$ MC6809 --help
    Usage: MC6809 [OPTIONS] COMMAND [ARGS]...
    
      MC6809 is a Open source (GPL v3 or later) emulator for the legendary 6809
      CPU, used in 30 years old homecomputer Dragon 32 and Tandy TRS-80 Color
      Computer (CoCo)...
    
      Created by Jens Diemer
    
      Homepage: https://github.com/6809/MC6809
    
    Options:
      --version  Show the version and exit.
      --help     Show this message and exit.
    
    Commands:
      benchmark  Run a 6809 Emulation benchmark

There is a simple benchmark. Run e.g.:

::

    (MC6809) ~/MC6809$ MC6809 benchmark --help

tests
=====

::

    ~$ cd MC6809-clone
    ~/MC6809-clone $ make pytest
    or
    ~/MC6809-clone $ poetry run pytest

profile
=======

To profile, e.g.:
$ cd MC6809-clone
/MC6809-clone $ make profile
or
/MC6809-clone $ poetry run MC6809 profile
}}}

TODO
====

#. Update 'cpu6809_html_debug.py'

#. Use bottle for http control server part

unimplemented OPs:

* RESET

* SWI / SWI2 / SWI3

* SYNC

-------
History
-------

(Some of the points are related to `DragonPy Emulator <https://github.com/jedie/DragonPy>`_)

* 10.02.2020 - `v0.6.0 <https://github.com/6809/MC6809/compare/v0.5.0...v0.6.0>`_ 

    * modernize project and sources

    * skip support for Python 2

    * minimal Python v3.6

* 19.10.2015 - `v0.5.0 <https://github.com/6809/MC6809/compare/v0.4.6...v0.5.0>`_ 

    * Split CPU with mixin inheritance

    * Optimizing:

        * remove ``.get()`` function calls from registers

        * move Condition Code Register (CC) into CPU via mixin class

    * Bugfix TFR and EXG by *convert_differend_width()*

    * Run DragonPy unittests on travis CI, too.

* 24.08.2015 - `v0.4.6 <https://github.com/6809/MC6809/compare/v0.4.5...v0.4.6>`_ 

    * Add a "max_delay", to fix the "freeze" after a speed limit change

    * rename some of the "speed limit" variables

* 21.08.2015 - `v0.4.5 <https://github.com/6809/MC6809/compare/v0.4.4...v0.4.5>`_ 

    * deactivate 'cpu6809_html_debug.py' - TODO: update it!

    * update cli unittests

    * update README and code cleanup

* 10.08.2015 - `v0.4.4 <https://github.com/6809/MC6809/compare/v0.4.3...v0.4.4>`_ - bugfix and cleanup the tests

* 10.08.2015 - `v0.4.3 <https://github.com/6809/MC6809/compare/v0.4.2...v0.4.3>`_ - run unittests with nose

* 27.05.2015 - `v0.4.2 <https://github.com/6809/MC6809/compare/v0.4.1...v0.4.2>`_ - Add MC6809/example6809.py

* 26.05.2015 - `v0.4.0, 0.4.1 <https://github.com/6809/MC6809/compare/1a40593...v0.4.1>`_ - Split MC6809 from `DragonPy <https://github.com/jedie/DragonPy>`_

* 22.09.2014 - Remove hacked CPU skeleton generator scripts with `commit ac903a8f <https://github.com/6809/MC6809/commit/ac903a8fb9f02e1db23172cb367af2581d4b29a1>`_

* 14.09.2014 - Release v0.2.0 - Add a speedlimit, config dialog and IRQ: `Forum post 11780 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&p=11780#p11780>`_

* 05.09.2014 - Release v0.1.0 - Implement pause/resume, hard-/soft-reset 6809 in GUI and improve a little the GUI/Editor stuff: `v0.1.0 <https://github.com/jedie/DragonPy/releases/tag/v0.1.0>`_ see also: `Forum post 11719 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&p=11719#p11719>`_.

* 27.08.2014 - Run CoCo with Extended Color Basic v1.1, bugfix transfer BASIC Listing with `8fe24e5...697d39e <https://github.com/jedie/DragonPy/compare/8fe24e5...697d39e>`_ see: `Forum post 11696 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=90#p11696>`_.

* 20.08.2014 - rudimenary BASIC IDE works with `7e0f16630...ce12148 <https://github.com/jedie/DragonPy/compare/7e0f16630...ce12148>`_, see also: `Forum post 11645 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=8&t=4439#p11645>`_.

* 05.08.2014 - Start to support CoCo, too with `0df724b <https://github.com/jedie/DragonPy/commit/0df724b3ee9d87088b524c3623040a41e9772eb4>`_, see also: `Forum post 11573 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=80#p11573>`_.

* 04.08.2014 - Use the origin Pixel-Font with Tkinter GUI, see: `Forum post 4909 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4909>`_ and `Forum post 11570 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=80#p11570>`_.

* 27.07.2014 - Copyrigth info from Dragon 64 ROM is alive with `543275b <https://github.com/jedie/DragonPy/commit/543275b1b90824b64b67dcd003cc5ab54296fc15>`_, see: `Forum post 11524 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=80#p11524>`_.

* 29.06.2014 - First "HELLO WORLD" works, see: `Forum post 11283 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=70#p11283>`_.

* 27.10.2013 - "sbc09" ROM works wuite well almist, see: `Forum post 9752 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=60#p9752>`_.

* 16.10.2013 - See copyright info from "Simple6809" ROM with `25a97b6 <https://github.com/jedie/DragonPy/tree/25a97b66d8567ba7c3a5b646e4a807b816a0e376>`_ see also: `Forum post 9654 <http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4308&start=50#p9654>`_.

* 10.09.2013 - Start to implement the 6809 CPU with `591d2ed <https://github.com/jedie/DragonPy/commit/591d2ed2b6f1a5f913c14e56e1e37f5870510b0d>`_

* 28.08.2013 - Fork "Apple ][ Emulator" written in Python: `https://github.com/jtauber/applepy <https://github.com/jtauber/applepy>`_ to `https://github.com/jedie/DragonPy <https://github.com/jedie/DragonPy>`_

------
Links:
------

+--------+----------------------------------------+
| Forum  | `http://forum.pylucid.org/`_           |
+--------+----------------------------------------+
| IRC    | `#pylucid on freenode.net`_            |
+--------+----------------------------------------+
| Jabber | pylucid@conference.jabber.org          |
+--------+----------------------------------------+
| PyPi   | `https://pypi.python.org/pypi/MC6809`_ |
+--------+----------------------------------------+
| Github | `https://github.com/6809/MC6809`_      |
+--------+----------------------------------------+

.. _http://forum.pylucid.org/: http://forum.pylucid.org/
.. _#pylucid on freenode.net: http://www.pylucid.org/permalink/304/irc-channel
.. _https://pypi.python.org/pypi/MC6809: https://pypi.python.org/pypi/MC6809
.. _https://github.com/6809/MC6809: https://github.com/6809/MC6809

--------
donation
--------

* `Flattr This! <https://flattr.com/submit/auto?uid=jedie&url=https%3A%2F%2Fgithub.com%2F6809%2FMC6809%2F>`_

* Send `Bitcoins <http://www.bitcoin.org/>`_ to `1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F <https://blockexplorer.com/address/1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F>`_

------------

``Note: this file is generated from README.creole 2020-02-10 21:04:15 with "python-creole"``