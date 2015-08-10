#!/usr/bin/env python
# coding: utf-8

"""
    borrowed from http://code.activestate.com/recipes/52215/

    usage:

    try:
        # ...do something...
    except:
        print_exc_plus()
"""

from __future__ import absolute_import, division, print_function

import sys
import traceback

import click

PY2 = sys.version_info[0] == 2
if PY2:
    range = xrange

MAX_CHARS = 256

def print_exc_plus():
    """
    Print the usual traceback information, followed by a listing of all the
    local variables in each frame.
    """
    sys.stderr.flush() # for eclipse
    sys.stdout.flush() # for eclipse

    tb = sys.exc_info()[2]
    while True:
        if not tb.tb_next:
            break
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back

    txt = traceback.format_exc()
    txt_lines = txt.splitlines()
    first_line = txt_lines.pop(0)
    last_line = txt_lines.pop(-1)
    click.secho(first_line, fg='red')

    for line in txt_lines:
        if line.strip().startswith("File"):
            print(line)
        else:
            click.secho(line, fg='white', bold=True)
            click.secho(line, fg="white", bold=True)
    click.secho(last_line, fg="red")

    print()
    click.secho(
        "Locals by frame, most recent call first:",
        fg="blue", bold=True
    )
    for frame in stack:
        click.secho('\n *** File "%s", line %i, in %s' % (
                frame.f_code.co_filename,
                frame.f_lineno,
                frame.f_code.co_name,
            ),
            fg="white",
            bold=True
        )

        for key, value in list(frame.f_locals.items()):
            print(click.style("%30s = " % key, bold=True), end=' ')
            # We have to be careful not to cause a new error in our error
            # printer! Calling str() on an unknown object could cause an
            # error we don't want.
            if isinstance(value, int):
                value = "$%x (decimal: %i)" % (value, value)
            else:
                value = repr(value)

            if len(value) > MAX_CHARS:
                value = "%s..." % value[:MAX_CHARS]

            try:
                print(value)
            except:
                print("<ERROR WHILE PRINTING VALUE>")

