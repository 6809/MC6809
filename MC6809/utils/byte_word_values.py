#!/usr/bin/env python

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================

    some code is borrowed from:
    XRoar emulator by Ciaran Anscomb (GPL license) more info, see README

    :copyleft: 2013-2014 by the DragonLib team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

import string
import sys

PY2 = sys.version_info[0] == 2
if PY2:
    range = xrange
    binary_type = str
else:
    binary_type = bytes


def signed5(x):
    """ convert to signed 5-bit """
    if x > 0xf: # 0xf == 2**4-1 == 15
        x = x - 0x20 # 0x20 == 2**5 == 32
    return x


def signed8(x):
    """ convert to signed 8-bit """
    if x > 0x7f: # 0x7f ==  2**7-1 == 127
        x = x - 0x100 # 0x100 == 2**8 == 256
    return x


def unsigned8(x):
    """ convert a signed 8-Bit value into a unsigned value """
    if x < 0:
        x = x + 0x0100 # 0x100 == 2**8 == 256
    return x


def signed16(x):
    """ convert to signed 16-bit """
    if x > 0x7fff: # 0x7fff ==  2**15-1 == 32767
        x = x - 0x10000 # 0x100 == 2**16 == 65536
    return x


def word2bytes(value):
    """
    >>> word2bytes(0xff09)
    (255, 9)

    >>> [hex(i) for i in word2bytes(0xffab)]
    ['0xff', '0xab']

    >>> word2bytes(0xffff +1)
    Traceback (most recent call last):
    ...
    AssertionError
    """
    assert 0 <= value <= 0xffff
    return (value >> 8, value & 0xff)


def bytes2word(byte_list):
    """
    >>> bytes2word([0xff,0xab])
    65451

    >>> hex(bytes2word([0xff,0xab]))
    '0xffab'
    """
    assert len(byte_list) == 2
    return (byte_list[0] << 8) + byte_list[1]


def bin2hexline(data, add_addr=True, width=16):
    """
    Format binary data to a Hex-Editor like format...

    e.g.:
    with open("C:\Python27\python.exe", "rb") as f:
        data = f.read(150)

    print("\n".join(bin2hexline(data, width=16)))

    0000 4d 5a 90 00 03 00 00 00 04 00 00 00 ff ff 00 00 MZ..............
    0016 b8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00 ........@.......
    0032 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................
    0048 00 00 00 00 00 00 00 00 00 00 00 00 e8 00 00 00 ................
    0064 0e 1f ba 0e 00 b4 09 cd 21 b8 01 4c cd 21 54 68 ........!..L.!Th
    0080 69 73 20 70 72 6f 67 72 61 6d 20 63 61 6e 6e 6f is.program.canno
    0096 74 20 62 65 20 72 75 6e 20 69 6e 20 44 4f 53 20 t.be.run.in.DOS.
    0112 6d 6f 64 65 2e 0d 0d 0a 24 00 00 00 00 00 00 00 mode....$.......
    0128 9d 68 ba 89 d9 09 d4 da d9 09 d4 da d9 09 d4 da .h..............
    0144 d0 71 41 da d8 09                               .qA...
    """
    assert isinstance(data, binary_type), (
        "is type: %s and not bytes/str: %s" % (type(data), repr(data))
    )

    addr = 0
    lines = []
    run = True
    line_width = 4 + (width * 3) + 1
    while run:
        if add_addr:
            line = ["%04i" % addr]
        else:
            line = []

        ascii_block = ""
        for i in range(width):
            b = data[addr]
            if PY2:
                b = ord(b)

            if chr(b) in string.printable:
                ascii_block += chr(b)
            else:
                ascii_block += "."

            line.append("%02x" % b)

            addr += 1
            if addr >= len(data):
                run = False
                break

        line = " ".join(line)
        line = line.ljust(line_width)
        line += ascii_block
        lines.append(line)
    return lines


def _bin2hexline_example():
    import sys

    with open(sys.executable, "rb") as f:
        data = f.read(500)

    print("\n".join(bin2hexline(data, width=16)))


if __name__ == "__main__":
    import doctest

    print(doctest.testmod(verbose=0))

    # _bin2hexline_example()
