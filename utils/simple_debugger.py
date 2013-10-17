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

import sys, traceback

def print_exc_plus():
    """
    Print the usual traceback information, followed by a listing of all the
    local variables in each frame.
    """
    sys.stderr.flush() # for eclipse
    sys.stdout.flush() # for eclipse

    tb = sys.exc_info()[2]
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
#     stack.reverse()
    traceback.print_exc()
    print "Locals by frame, most recent call first:"
    for frame in stack:
        print '\n *** File "%s", line %i, in %s' % (
            frame.f_code.co_filename, frame.f_lineno, frame.f_code.co_name
        )
        for key, value in frame.f_locals.items():
            print "\t%10s = " % key,
            # We have to be careful not to cause a new error in our error
            # printer! Calling str() on an unknown object could cause an
            # error we don't want.
            if isinstance(value, basestring):
                value = repr(value)
            elif isinstance(value, int):
                value = "$%x (decimal: %i)" % (value, value)

            try:
                print value
            except:
                print "<ERROR WHILE PRINTING VALUE>"