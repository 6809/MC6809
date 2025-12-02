import logging
from pathlib import Path
from typing import Annotated

import tyro
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.tyro_commands import TyroVerbosityArgType
from rich import print  # noqa

from MC6809.cli_app import app
from MC6809.components.mc6809_disassembler import Disassembly, iter_disassembly_lines


logger = logging.getLogger(__name__)


@app.command
def disassemble(
    file: Annotated[Path, tyro.conf.arg(help='Input file to disassemble')],
    /,
    start_address: Annotated[int, tyro.conf.arg(help='Optinal start address')] = 0x0,
    header: Annotated[bool, tyro.conf.arg(help='Include disassembly header')] = True,
    verbosity: TyroVerbosityArgType = 1,
):
    """
    Run a MC6809 emulation benchmark
    """
    setup_logging(verbosity=verbosity)
    print(f'Disassembling file: {file}')

    with file.open('rb') as f:
        assembly = f.read()

    from MC6809.components.mc6809_disassembler import disassemble

    disassembly: Disassembly = disassemble(assembly, start_address=start_address)
    for line in iter_disassembly_lines(disassembly, with_header=header):
        print(line)
