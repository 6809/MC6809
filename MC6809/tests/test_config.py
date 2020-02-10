"""
    MC6809 - 6809 CPU emulator in Python
    =======================================

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the MC6809 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


from MC6809.core.configs import BaseConfig


class TestCfg(BaseConfig):
    """
    Default test config
    """
    RAM_START = 0x0000
    RAM_END = 0x7FFF

    ROM_START = 0x8000
    ROM_END = 0xFFFF

    RESET_VECTOR = 0xFFFE

    BUS_ADDR_AREAS = (
        (0xFFF2, 0xFFFE, "Interrupt vectors"),
    )

    DEFAULT_ROMS = None

    def __init__(self, cfg_dict):

        super().__init__(cfg_dict)
