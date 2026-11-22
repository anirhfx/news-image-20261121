#!/usr/bin/env python3
"""The World in One Page -- make.fun bounty news-image-20261121.

Sums up world news of Saturday 21 November 2026 in a single 1024x1024
PNG, drawn as a newspaper front page. Pure Python 3 standard library:
the page rasterizer, the 5x7 bitmap font and the PNG encoder are all
written in this one file, so the program needs no network, no system
fonts and no third-party packages at run time.

Deterministic: fixed layout, fixed palette, fixed zlib level, no clock,
no randomness, no hash-order dependence. Two runs write identical bytes.

Usage: python3 main.py
Writes: $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png)
"""
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 228)   # newsprint cream
INK = (22, 22, 22)        # near-black ink
RED = (176, 30, 30)       # headline red
DARKRED = (138, 18, 18)
BLUE = (28, 74, 138)      # deep blue
NAVY = (14, 30, 60)       # night panel
SKY = (186, 216, 238)     # pale sky
GOLD = (198, 158, 40)     # gold accent
GREEN = (42, 122, 52)     # green accent
WHITE = (255, 255, 255)
GREY = (96, 94, 86)       # muted grey
LIGHT = (233, 228, 214)   # light panel
ORANGE = (230, 118, 28)
TEAL = (18, 110, 110)

# ---------------------------------------------------------------- 5x7 font
# Glyphs are 7 rows of 5 bits; '#' is ink. Uppercase, digits, punctuation.
# Written for this entry; text is set in capitals throughout.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "01100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '-': ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '*': ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
}


# ---------------------------------------------------------------- canvas
class Canvas:
    """A plain RGB framebuffer with small drawing primitives."""

    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.buf = bytearray(bytes(bg) * (w * h))

    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i:i + 3] = bytes(c)

    def fill(self, x, y, w, h, c):
        x0 = max(x, 0)
        y0 = max(y, 0)
        x1 = min(x + w, self.w)
        y1 = min(y + h, self.h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(c) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.buf[i:i + len(row)] = row

    def outline(self, x, y, w, h, c, t=1):
        self.fill(x, y, w, t, c)
        self.fill(x, y + h - t, w, t, c)
        self.fill(x, y, t, h, c)
        self.fill(x + w - t, y, t, h, c)

    def hline(self, x, y, w, c, t=1):
        self.fill(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.fill(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        """Bresenham line, t pixels thick (square brush)."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.fill(x0 - t // 2, y0 - t // 2, t, t, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            dx = int((r * r - (yy - cy) ** 2) ** 0.5)
            self.fill(cx - dx, yy, 2 * dx + 1, 1, c)

    def ring(self, cx, cy, r, c, t=2):
        for yy in range(cy - r - t, cy + r + t + 1):
            for xx in range(cx - r - t, cx + r + t + 1):
                d = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5
                if r - t / 2 <= d <= r + t / 2:
                    self.put(xx, yy, c)

    def star(self, cx, cy, r, c, spikes=8):
        """Explosion starburst: straight spokes from the centre."""
        import math
        for k in range(spikes):
            a = math.pi * 2 * k / spikes
            self.line(cx, cy, int(cx + r * math.cos(a)),
                      int(cy + r * math.sin(a)), c, 3)
        self.disc(cx, cy, max(3, r // 4), c)

    # -- text -------------------------------------------------------------
    def twidth(self, s, scale):
        return len(s) * 6 * scale - scale

    def text(self, x, y, s, scale, c):
        s = s.upper()
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT[' '])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == '1':
                        self.fill(cx + col * scale, y + row * scale,
                                  scale, scale, c)
            cx += 6 * scale
        return cx

    def text_c(self, y, s, scale, c):
        """Centred text on the full page width."""
        self.text((self.w - self.twidth(s, scale)) // 2, y, s, scale, c)

    def wrap(self, s, width, scale):
        """Greedy word wrap; returns a list of lines fitting width px."""
        limit = max(1, width // (6 * scale))
        lines = []
        for chunk in s.split('\n'):
            words = chunk.split(' ')
            cur = ''
            for word in words:
                trial = word if not cur else cur + ' ' + word
                if len(trial) <= limit:
                    cur = trial
                else:
                    if cur:
                        lines.append(cur)
                    while len(word) > limit:
                        lines.append(word[:limit])
                        word = word[limit:]
                    cur = word
            if cur or not lines:
                lines.append(cur)
        return lines

    def para(self, x, y, s, width, scale, c, leading=None):
        """Draw a wrapped paragraph; returns the y just below it."""
        lh = leading if leading is not None else 7 * scale + 4
        for line in self.wrap(s, width, scale):
            self.text(x, y, line, scale, c)
            y += lh
        return y


# ---------------------------------------------------------------- PNG encoder
def _chunk(kind, data):
    out = struct.pack('>I', len(data)) + kind + data
    out += struct.pack('>I', zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(cv):
    """Encode the canvas as a deterministic RGB PNG (filter 0 rows)."""
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.buf[y * stride:(y + 1) * stride]
    ihdr = struct.pack('>IIBBBBB', cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n'
    png += _chunk(b'IHDR', ihdr)
    png += _chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += _chunk(b'IEND', b'')
    return png


# ---------------------------------------------------------------- illustrations
def draw_flag_us(cv, x, y, w, h):
    """Stars and stripes, simplified: 7 stripes, blue canton, dot stars."""
    stripe = max(1, h // 7)
    for i in range(7):
        cv.fill(x, y + i * stripe, w, stripe, RED if i % 2 == 0 else WHITE)
    cw, ch = w * 2 // 5, stripe * 4
    cv.fill(x, y, cw, ch, BLUE)
    for r in range(3):
        for c in range(4):
            cv.disc(x + 6 + c * 9, y + 5 + r * 8, 1, WHITE)


def draw_flag_cn(cv, x, y, w, h):
    """China: red field, one large and four small yellow stars."""
    cv.fill(x, y, w, h, RED)
    cv.star(x + w // 4, y + h // 3, 9, GOLD, 5)
    for dx, dy in ((18, -8), (24, -2), (24, 6), (18, 12)):
        cv.disc(x + w // 4 + dx, y + h // 3 + dy, 2, GOLD)


def draw_flag_ru(cv, x, y, w, h):
    """Russia: white, blue, red horizontal tricolour."""
    third = h // 3
    cv.fill(x, y, w, third, WHITE)
    cv.fill(x, y + third, w, third, BLUE)
    cv.fill(x, y + 2 * third, w, h - 2 * third, RED)


def draw_clock(cv, cx, cy, r, hour, minute):
    """A clock face with hands at hour:minute."""
    import math
    cv.disc(cx, cy, r, WHITE)
    cv.ring(cx, cy, r, INK, 3)
    cv.ring(cx, cy, r - 6, RED, 1)
    for k in range(12):
        a = math.pi * 2 * k / 12
        x1 = int(cx + (r - 8) * math.sin(a))
        y1 = int(cy - (r - 8) * math.cos(a))
        cv.disc(x1, y1, 2, INK)
    ha = math.pi * 2 * (hour % 12 + minute / 60.0) / 12
    ma = math.pi * 2 * minute / 60.0
    cv.line(cx, cy, int(cx + (r * 0.5) * math.sin(ha)),
            int(cy - (r * 0.5) * math.cos(ha)), INK, 4)
    cv.line(cx, cy, int(cx + (r * 0.75) * math.sin(ma)),
            int(cy - (r * 0.75) * math.cos(ma)), INK, 3)
    cv.disc(cx, cy, 4, RED)


def draw_chart(cv, x, y, w, h, points, c):
    """A falling line chart with axes and end dot."""
    cv.outline(x, y, w, h, GREY, 1)
    n = len(points)
    xs = [x + 8 + i * (w - 16) // (n - 1) for i in range(n)]
    lo = min(points)
    hi = max(points)
    span = max(1, hi - lo)
    ys = [y + h - 8 - (p - lo) * (h - 16) // span for p in points]
    for i in range(n - 1):
        cv.line(xs[i], ys[i], xs[i + 1], ys[i + 1], c, 4)
    for px, py in zip(xs, ys):
        cv.disc(px, py, 4, c)
    cv.disc(xs[-1], ys[-1], 6, DARKRED)


def draw_missile(cv, x, y, x2, y2):
    """A missile streaking to (x2, y2) with a smoke trail."""
    cv.line(x, y, x2, y2, WHITE, 4)
    cv.line(x, y, x2, y2, ORANGE, 2)
    cv.disc(x2, y2, 5, GOLD)
    for k in range(1, 5):
        t = k / 5.0
        mx = int(x + (x2 - x) * t)
        my = int(y + (y2 - y) * t)
        cv.disc(mx, my, 5 - k, WHITE)


def draw_tanker(cv, x, y, w, h):
    """A crude-oil tanker silhouette on the sea."""
    cv.fill(x, y + h // 2, w, h // 2, INK)          # hull
    cv.fill(x + w // 8, y, w // 6, h // 2, INK)     # bow castle
    cv.fill(x + w * 5 // 8, y + h // 6, w // 6, h // 3, INK)  # bridge
    cv.fill(x + w * 5 // 8, y, w // 8, h // 6, RED)  # funnel
    cv.fill(x, y + h - 4, w, 4, RED)                # waterline


def draw_mine(cv, cx, cy, r):
    """A naval mine: spiked ball."""
    import math
    cv.disc(cx, cy, r, INK)
    for k in range(8):
        a = math.pi * 2 * k / 8
        cv.line(cx, cy, int(cx + (r + 7) * math.cos(a)),
                int(cy + (r + 7) * math.sin(a)), INK, 3)
    cv.disc(cx, cy, r // 2, GREY)


# ---------------------------------------------------------------- page furniture
def kicker(cv, x, y, label, accent=RED):
    cv.fill(x, y - 2, 26, 4, accent)
    cv.text(x + 34, y - 4, label, 2, accent)


def rule(cv, y, x0=24, x1=1000, c=INK, t=2):
    cv.hline(x0, y, x1 - x0, c, t)


def masthead(cv):
    cv.text_c(24, "THE WORLD IN ONE PAGE", 5, INK)
    cv.text_c(72, "SATURDAY 21 NOVEMBER 2026", 3, RED)
    cv.text(24, 100, "ONE DAY IN ONE PICTURE", 1, GREY)
    right = "VOL. 1 - NO. 325"
    cv.text(1000 - cv.twidth(right, 1), 100, right, 1, GREY)
    rule(cv, 116, 24, 1000, INK, 3)
    rule(cv, 122, 24, 1000, INK, 1)


def lead_story(cv):
    """Top story: Trump tells Europe to stop funding Ukraine."""
    y = 140
    kicker(cv, 24, y + 4, "THE SUMMIT AFTERMATH")
    cv.para(24, y + 26, "TRUMP TELLS EUROPE:", 540, 4, INK, 34)
    cv.para(24, y + 60, "STOP FUNDING UKRAINE", 540, 4, RED, 34)
    cv.para(24, y + 108,
            "After his summit with Putin, the US president tells "
            "European leaders to withhold money from Kyiv. Xi, who "
            "put China at the centre of the talks, backs a "
            "ceasefire pact and new nuclear-safety negotiations.",
            536, 2, INK, 19)
    cv.para(24, y + 208,
            "Europe calls for a winter ceasefire and reaffirms "
            "plans for postwar troops, despite Putin's threats.",
            536, 2, GREY, 19)
    # illustration: three flags over a slashed aid coin
    px, py, pw, ph = 584, 132, 416, 268
    cv.fill(px, py, pw, ph, NAVY)
    cv.outline(px, py, pw, ph, INK, 2)
    cv.text(px + 16, py + 12, "SHENZHEN - THE DAY AFTER", 1, WHITE)
    flags = ((px + 30, draw_flag_us), (px + 163, draw_flag_cn),
             (px + 296, draw_flag_ru))
    names = ("USA", "CHINA", "RUSSIA")
    for (fx, fn), name in zip(flags, names):
        cv.vline(fx + 4, py + 48, 96, WHITE, 3)
        fn(cv, fx + 8, py + 48, 88, 56)
        cv.text(fx + 8, py + 112, name, 1, WHITE)
    cv.disc(px + pw // 2, py + 208, 40, GOLD)
    cv.ring(px + pw // 2, py + 208, 40, WHITE, 2)
    cv.text(px + pw // 2 - 21, py + 196, "AID", 3, NAVY)
    cv.line(px + pw // 2 - 34, py + 176, px + pw // 2 + 34, py + 240, RED, 7)
    rule(cv, 416, 24, 1000, INK, 2)


def cop31_panel(cv):
    """Climate talks in Antalya run into Saturday overtime."""
    x, y, w, h = 24, 432, 476, 224
    cv.fill(x, y, w, h, LIGHT)
    cv.outline(x, y, w, h, INK, 2)
    kicker(cv, x + 16, y + 20, "CLIMATE - ANTALYA", TEAL)
    cv.para(x + 16, y + 44, "COP31: NO DEAL", 300, 3, INK, 26)
    cv.para(x + 16, y + 70, "OR A GOOD DEAL", 300, 3, TEAL, 26)
    cv.para(x + 16, y + 106,
            "Talks run into Saturday overtime as the EU refuses a "
            "weak text.",
            290, 2, INK, 17)
    cv.text(x + 16, y + 170, "DRAFT DROPS FOSSIL-FUEL WORDING,", 1, INK)
    cv.text(x + 16, y + 182, "$120BN TARGET ALSO CUT", 1, INK)
    draw_clock(cv, x + 396, y + 78, 52, 9, 0)
    cv.text(x + 348, y + 140, "OVERTIME", 2, RED)
    cv.text(x + 332, y + 162, "21+ HOURS OVER", 1, GREY)
    cv.text(x + 16, y + 196, "NEARLY 200 COUNTRIES, NO AGREEMENT YET",
            1, GREY)


def markets_panel(cv):
    """The AI sell-off: worst week for Wall Street since 2020."""
    x, y, w, h = 524, 432, 476, 224
    cv.fill(x, y, w, h, WHITE)
    cv.outline(x, y, w, h, INK, 2)
    kicker(cv, x + 16, y + 20, "MARKETS", RED)
    cv.para(x + 16, y + 44, "WORST WEEK SINCE 2020", 444, 3, RED, 26)
    cv.para(x + 16, y + 74,
            "The AI sell-off spreads worldwide. Nvidia falls 14% "
            "as the SEC examines its books. Anthropic gives back "
            "8.5% a day after its record debut.",
            444, 2, INK, 19)
    draw_chart(cv, x + 16, y + 154, 444, 48, (100, 92, 84, 70, 52, 30), RED)
    cv.text(x + 16, y + 208, "S&P 500 -3.7%   NIKKEI -5.1%   NASDAQ -5.3%",
            1, INK)


def war_panel(cv):
    """Russia's strikes on Ukraine and the Polish airspace breach."""
    x, y, w, h = 24, 672, 476, 212
    cv.fill(x, y, w, h, NAVY)
    cv.outline(x, y, w, h, INK, 2)
    kicker(cv, x + 16, y + 20, "UKRAINE - POLAND", ORANGE)
    cv.para(x + 16, y + 44, "MISSILES HIT KYIV", 340, 3, WHITE, 26)
    cv.para(x + 16, y + 70, "AND KRYVYI RIH", 340, 3, WHITE, 26)
    cv.para(x + 16, y + 106,
            "Two killed, 60 hurt in Zelensky's home city. Russian "
            "missiles and a drone cross into Polish airspace.",
            290, 2, WHITE, 19)
    draw_missile(cv, x + 330, y + 60, x + 420, y + 130)
    cv.star(x + 420, y + 130, 34, ORANGE, 10)
    cv.star(x + 420, y + 130, 20, GOLD, 8)
    cv.text(x + 330, y + 178, "WARSAW CALLS IT A", 1, WHITE)
    cv.text(x + 330, y + 192, "PROVOCATION", 1, WHITE)


def gulf_panel(cv):
    """Trump weighs new strikes on Iran; tankers hit mines at Hormuz."""
    x, y, w, h = 524, 672, 476, 212
    cv.fill(x, y, w, h, SKY)
    cv.outline(x, y, w, h, INK, 2)
    kicker(cv, x + 16, y + 20, "THE GULF", BLUE)
    cv.para(x + 16, y + 44, "TRUMP WEIGHS NEW", 300, 3, INK, 26)
    cv.para(x + 16, y + 70, "IRAN STRIKES", 300, 3, INK, 26)
    cv.para(x + 16, y + 106,
            "Tehran says it fired on a US F-16 in the Gulf. Two "
            "oil tankers hit mines near the Strait of Hormuz.",
            290, 2, INK, 19)
    cv.fill(x + 316, y + 150, 144, 46, BLUE)
    draw_tanker(cv, x + 322, y + 128, 132, 44)
    draw_mine(cv, x + 330, y + 182, 8)
    cv.text(x + 316, y + 78, "STRAIT OF HORMUZ", 1, BLUE)


def footer(cv):
    """Also today: six more stories from Saturday 21 November."""
    y = 900
    rule(cv, y, 24, 1000, INK, 2)
    cv.text(24, y + 12, "ALSO TODAY", 2, RED)
    items = [
        ("MEXICO", "Violence flares in Sinaloa after the capture of "
         "cartel boss 'El Chapo Isidro'."),
        ("SCIENCE", "Mosquitoes carrying a bacterium cut dengue "
         "cases by 69% in a Brazil trial."),
        ("SPACE", "BepiColombo reaches Mercury orbit after an "
         "eight-year journey."),
        ("EU - UK", "London and Brussels sign a landmark deal to "
         "rebuild ties after Brexit."),
        ("GENEVA", "UN talks agree to keep working on rules to "
         "limit AI weapons - no binding deal yet."),
        ("AND MORE", "Somalia expels the UAE envoy; France passes "
         "its police-shootings law."),
    ]
    col_w = 488
    for i, (tag, body) in enumerate(items):
        cx = 24 + (i % 2) * (col_w + 24)
        cy = y + 36 + (i // 2) * 26
        cv.text(cx, cy, tag + ":", 1, RED)
        cv.para(cx + cv.twidth(tag + ": ", 1), cy, body, 400, 1, INK, 10)
    rule(cv, 1014, 24, 1000, INK, 1)


# ---------------------------------------------------------------- main
def main():
    cv = Canvas(W, H, PAPER)
    masthead(cv)
    lead_story(cv)
    cop31_panel(cv)
    markets_panel(cv)
    war_panel(cv)
    gulf_panel(cv)
    footer(cv)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(encode_png(cv))
    print("wrote", path)


if __name__ == "__main__":
    main()
