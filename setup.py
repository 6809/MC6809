#!/usr/bin/env python
# coding: utf-8

"""
    distutils setup
    ~~~~~~~~~~~~~~~

    :copyleft: 2014-2015 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

from setuptools import setup, find_packages
import os
import sys

import MC6809


PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))


if "publish" in sys.argv:
    import subprocess
    args = [sys.executable or "python", "setup.py", "sdist", "bdist_wheel", "upload"]
    print("\nCall: %r\n" %  " ".join(args))
    subprocess.call(args)

    print("\nDon't forget to tag this version, e.g.:")
    print("\tgit tag v%s" % MC6809.__version__)
    print("\tgit push --tags")
    sys.exit()


# convert creole to ReSt on-the-fly, see also:
# https://code.google.com/p/python-creole/wiki/UseInSetup
try:
    from creole.setup_utils import get_long_description
except ImportError as err:
    if "check" in sys.argv or "register" in sys.argv or "sdist" in sys.argv or "--long-description" in sys.argv:
        raise ImportError("%s - Please install python-creole >= v0.8 -  e.g.: pip install python-creole" % err)
    long_description = None
else:
    long_description = get_long_description(PACKAGE_ROOT)


if "test" in sys.argv or "nosetests" in sys.argv:
    """
    nose is a optional dependency, so test import.
    Otherwise the user get only the error:
        error: invalid command 'nosetests'
    """
    try:
        import nose
    except ImportError as err:
        print("\nError: Can't import 'nose': %s" % err)
        print("\nMaybe 'nose' is not installed or virtualenv not activated?!?")
        print("e.g.:")
        print("    ~/your/env/$ source bin/activate")
        print("    ~/your/env/$ pip install nose")
        print("    ~/your/env/$ ./setup.py nosetests\n")
        sys.exit(-1)
    else:
        if "test" in sys.argv:
            print("\nPlease use 'nosetests' instead of 'test' to cover all tests!\n")
            print("e.g.:")
            print("     $ ./setup.py nosetests\n")
            sys.exit(-1)


setup(
    name="MC6809",
    version=MC6809.__version__,
    py_modules=["MC6809"],
    provides=["MC6809"],
    install_requires=[
        "click",
    ],
    tests_require=[
        "nose", # https://pypi.python.org/pypi/nose
    ],
    entry_points='''
        [console_scripts]
        MC6809=MC6809.cli:cli
    ''',
    author="Jens Diemer",
    author_email="MC6809@jensdiemer.de",
    description="MC6809 CPU emulator written in Python",
    keywords="Emulator 6809",
    long_description=long_description,
    url="https://github.com/6809/MC6809",
    license="GPL v3+",
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: System :: Emulators",
        "Topic :: Software Development :: Assemblers",
        "Topic :: Software Development :: Testing",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
