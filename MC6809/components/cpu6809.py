#!/usr/bin/env python
# coding: utf-8

"""
    MC6809 - 6809 CPU emulator in Python
    =======================================

    6809 is Big-Endian

    Links:
        http://dragondata.worldofdragon.org/Publications/inside-dragon.htm
        http://www.burgins.com/m6809.html
        http://koti.mbnet.fi/~atjs/mc6809/

    :copyleft: 2013-2014 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.

    Based on:
        * ApplyPy by James Tauber (MIT license)
        * XRoar emulator by Ciaran Anscomb (GPL license)
    more info, see README
"""

from __future__ import absolute_import, division, print_function

import sys

if sys.version_info[0] == 3:
    # Python 3
    pass
else:
    # Python 2
    range = xrange

import logging

from MC6809.components.mc6809_interrupt import MC6809Interrupt
from MC6809.components.mc6809_addressing import MC6809Addressing
from MC6809.components.mc6809_stack import MC6809Stack
from MC6809.components.mc6809_ops_load_store import MC6809OpsLoadStore
from MC6809.components.mc6809_ops_branches import MC6809OpsBranches
from MC6809.components.mc6809_ops_logic import MC6809OpsLogical
from MC6809.components.mc6809_ops_test import MC6809OpsTest
from MC6809.components.mc6809_base import CPUBase
from MC6809.components.mc6809_tools import CPUThreadedStatus

log = logging.getLogger("MC6809")


# HTML_TRACE = True
HTML_TRACE = False


class CPU(CPUBase, MC6809Addressing, MC6809Stack, MC6809Interrupt, MC6809OpsLoadStore, MC6809OpsBranches,
    MC6809OpsTest, MC6809OpsLogical, CPUThreadedStatus):# , CPUTypeAssert):
    pass
