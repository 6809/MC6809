#!/usr/bin/env python
# encoding:utf8

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================


    Based on:
        ApplePy - an Apple ][ emulator in Python:
        James Tauber / http://jtauber.com/ / https://github.com/jtauber/applepy
        originally written 2001, updated 2011
        origin source code licensed under MIT License
"""


import time
try:
    import pygame
except ImportError:
    # Maybe Dragon would not be emulated ;)
    pygame = None


class Display(object):

    characters = [
        [0b00000, 0b01110, 0b10001, 0b10101, 0b10111, 0b10110, 0b10000, 0b01111],
        [0b00000, 0b00100, 0b01010, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001],
        [0b00000, 0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110],
        [0b00000, 0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110],
        [0b00000, 0b11110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11110],
        [0b00000, 0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111],
        [0b00000, 0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000],
        [0b00000, 0b01111, 0b10000, 0b10000, 0b10000, 0b10011, 0b10001, 0b01111],
        [0b00000, 0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
        [0b00000, 0b01110, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
        [0b00000, 0b00001, 0b00001, 0b00001, 0b00001, 0b00001, 0b10001, 0b01110],
        [0b00000, 0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001],
        [0b00000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111],
        [0b00000, 0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001],
        [0b00000, 0b10001, 0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001],
        [0b00000, 0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
        [0b00000, 0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000],
        [0b00000, 0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101],
        [0b00000, 0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001],
        [0b00000, 0b01110, 0b10001, 0b10000, 0b01110, 0b00001, 0b10001, 0b01110],
        [0b00000, 0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
        [0b00000, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
        [0b00000, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100],
        [0b00000, 0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b11011, 0b10001],
        [0b00000, 0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001],
        [0b00000, 0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00100],
        [0b00000, 0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111],
        [0b00000, 0b11111, 0b11000, 0b11000, 0b11000, 0b11000, 0b11000, 0b11111],
        [0b00000, 0b00000, 0b10000, 0b01000, 0b00100, 0b00010, 0b00001, 0b00000],
        [0b00000, 0b11111, 0b00011, 0b00011, 0b00011, 0b00011, 0b00011, 0b11111],
        [0b00000, 0b00000, 0b00000, 0b00100, 0b01010, 0b10001, 0b00000, 0b00000],
        [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b11111],
        [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000],
        [0b00000, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00000, 0b00100],
        [0b00000, 0b01010, 0b01010, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000],
        [0b00000, 0b01010, 0b01010, 0b11111, 0b01010, 0b11111, 0b01010, 0b01010],
        [0b00000, 0b00100, 0b01111, 0b10100, 0b01110, 0b00101, 0b11110, 0b00100],
        [0b00000, 0b11000, 0b11001, 0b00010, 0b00100, 0b01000, 0b10011, 0b00011],
        [0b00000, 0b01000, 0b10100, 0b10100, 0b01000, 0b10101, 0b10010, 0b01101],
        [0b00000, 0b00100, 0b00100, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000],
        [0b00000, 0b00100, 0b01000, 0b10000, 0b10000, 0b10000, 0b01000, 0b00100],
        [0b00000, 0b00100, 0b00010, 0b00001, 0b00001, 0b00001, 0b00010, 0b00100],
        [0b00000, 0b00100, 0b10101, 0b01110, 0b00100, 0b01110, 0b10101, 0b00100],
        [0b00000, 0b00000, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0b00000],
        [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00100, 0b00100, 0b01000],
        [0b00000, 0b00000, 0b00000, 0b00000, 0b11111, 0b00000, 0b00000, 0b00000],
        [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00100],
        [0b00000, 0b00000, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b00000],
        [0b00000, 0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110],
        [0b00000, 0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
        [0b00000, 0b01110, 0b10001, 0b00001, 0b00110, 0b01000, 0b10000, 0b11111],
        [0b00000, 0b11111, 0b00001, 0b00010, 0b00110, 0b00001, 0b10001, 0b01110],
        [0b00000, 0b00010, 0b00110, 0b01010, 0b10010, 0b11111, 0b00010, 0b00010],
        [0b00000, 0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b10001, 0b01110],
        [0b00000, 0b00111, 0b01000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110],
        [0b00000, 0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b01000, 0b01000],
        [0b00000, 0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110],
        [0b00000, 0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00010, 0b11100],
        [0b00000, 0b00000, 0b00000, 0b00100, 0b00000, 0b00100, 0b00000, 0b00000],
        [0b00000, 0b00000, 0b00000, 0b00100, 0b00000, 0b00100, 0b00100, 0b01000],
        [0b00000, 0b00010, 0b00100, 0b01000, 0b10000, 0b01000, 0b00100, 0b00010],
        [0b00000, 0b00000, 0b00000, 0b11111, 0b00000, 0b11111, 0b00000, 0b00000],
        [0b00000, 0b01000, 0b00100, 0b00010, 0b00001, 0b00010, 0b00100, 0b01000],
        [0b00000, 0b01110, 0b10001, 0b00010, 0b00100, 0b00100, 0b00000, 0b00100]
    ]

    lores_colours = [
        (0, 0, 0), # black
        (208, 0, 48), # magenta / dark red
        (0, 0, 128), # dark blue
        (255, 0, 255), # purple / violet
        (0, 128, 0), # dark green
        (128, 128, 128), # gray 1
        (0, 0, 255), # medium blue / blue
        (96, 160, 255), # light blue
        (128, 80, 0), # brown / dark orange
        (255, 128 , 0), # orange
        (192, 192, 192), # gray 2
        (255, 144, 128), # pink / light red
        (0, 255, 0), # light green / green
        (255, 255, 0), # yellow / light orange
        (64, 255, 144), # aquamarine / light green
        (255, 255, 255), # white
    ]

    def __init__(self):
        self.screen = pygame.display.set_mode((560, 384))
        pygame.display.set_caption("DragonPy")
        self.mix = False
        self.flash_time = time.time()
        self.flash_on = False
        self.flash_chars = [[0] * 0x400] * 2

        self.page = 1
        self.text = True
        self.colour = False

        self.chargen = []
        for c in self.characters:
            chars = [[pygame.Surface((14, 16)), pygame.Surface((14, 16))],
                     [pygame.Surface((14, 16)), pygame.Surface((14, 16))]]
            for colour in (0, 1):
                hue = (255, 255, 255) if colour else (0, 200, 0)
                for inv in (0, 1):
                    pixels = pygame.PixelArray(chars[colour][inv])
                    off = hue if inv else (0, 0, 0)
                    on = (0, 0, 0) if inv else hue
                    for row in range(8):
                        b = c[row] << 1
                        for col in range(7):
                            bit = (b >> (6 - col)) & 1
                            pixels[2 * col][2 * row] = on if bit else off
                            pixels[2 * col + 1][2 * row] = on if bit else off
                    del pixels
            self.chargen.append(chars)

    def txtclr(self):
        self.text = False

    def txtset(self):
        self.text = True
        self.colour = False

    def mixclr(self):
        self.mix = False

    def mixset(self):
        self.mix = True
        self.colour = True

    def lowscr(self):
        self.page = 1

    def hiscr(self):
        self.page = 2

    def lores(self):
        self.high_res = False

    def hires(self):
        self.high_res = True

    def update(self, address, value):
        if self.page == 1:
            start_text = 0x400
            start_hires = 0x2000
        elif self.page == 2:
            start_text = 0x800
            start_hires = 0x4000
        else:
            return

        if start_text <= address <= start_text + 0x3FF:
            base = address - start_text
            self.flash_chars[self.page - 1][base] = value
            hi, lo = divmod(base, 0x80)
            row_group, column = divmod(lo, 0x28)
            row = hi + 8 * row_group

            if row_group == 3:
                return

            if self.text or not self.mix or not row < 20:
                mode, ch = divmod(value, 0x40)

                if mode == 0:
                    inv = True
                elif mode == 1:
                    inv = self.flash_on
                else:
                    inv = False

                self.screen.blit(self.chargen[ch][self.colour][inv], (2 * (column * 7), 2 * (row * 8)))
            else:
                pixels = pygame.PixelArray(self.screen)
                if not self.high_res:
                    lower, upper = divmod(value, 0x10)

                    for dx in range(14):
                        for dy in range(8):
                            x = column * 14 + dx
                            y = row * 16 + dy
                            pixels[x][y] = self.lores_colours[upper]
                        for dy in range(8, 16):
                            x = column * 14 + dx
                            y = row * 16 + dy
                            pixels[x][y] = self.lores_colours[lower]
                del pixels

        elif start_hires <= address <= start_hires + 0x1FFF:
            if self.high_res:
                base = address - start_hires
                row8, b = divmod(base, 0x400)
                hi, lo = divmod(b, 0x80)
                row_group, column = divmod(lo, 0x28)
                row = 8 * (hi + 8 * row_group) + row8

                if self.mix and row >= 160:
                    return

                if row < 192 and column < 40:

                    pixels = pygame.PixelArray(self.screen)
                    msb = value // 0x80

                    for b in range(7):
                        c = value & (1 << b)
                        xx = (column * 7 + b)
                        x = 2 * xx
                        y = 2 * row

                        if msb:
                            if xx % 2:
                                pixels[x][y] = (0, 0, 0)
                                # orange
                                pixels[x][y] = (255, 192, 0) if c else (0, 0, 0) # @@@
                                pixels[x + 1][y] = (255, 192, 0) if c else (0, 0, 0)
                            else:
                                # blue
                                pixels[x][y] = (0, 192, 255) if c else (0, 0, 0)
                                pixels[x + 1][y] = (0, 0, 0)
                                pixels[x + 1][y] = (0, 192, 255) if c else (0, 0, 0) # @@@
                        else:
                            if xx % 2:
                                pixels[x][y] = (0, 0, 0)
                                # green
                                pixels[x][y] = (0, 255, 0) if c else (0, 0, 0) # @@@
                                pixels[x + 1][y] = (0, 255, 0) if c else (0, 0, 0)
                            else:
                                # violet
                                pixels[x][y] = (255, 0, 255) if c else (0, 0, 0)
                                pixels[x + 1][y] = (0, 0, 0)
                                pixels[x + 1][y] = (255, 0, 255) if c else (0, 0, 0) # @@@

                        pixels[x][y + 1] = (0, 0, 0)
                        pixels[x + 1][y + 1] = (0, 0, 0)

                    del pixels

    def flash(self):
        if time.time() - self.flash_time >= 0.5:
            self.flash_on = not self.flash_on
            for offset, char in enumerate(self.flash_chars[self.page - 1]):
                if (char & 0xC0) == 0x40:
                    self.update(0x400 + offset, char)
            self.flash_time = time.time()
