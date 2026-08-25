#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reconstruction of the azure IDO logotype from the Dicionario's title page.

Everything below is MEASURED from `dicionario/pocket/cover.tex` and checked
against page 3 of `dicionario.pdf` (recto, the title page):

  * the letters ID are set in Jost* Bold, at 115.083 pt;
  * the disc follows the D at 0.0045 x page-width, that is 12.19/1000 em;
  * its diameter is 1.0651 times the cap height (700/1000 em);
  * it is centred on the cap height;
  * the star is regular, built to the four rules of cover.tex, its three
    long points on the circle and its three short ones at half-radius.

The output coordinate system has its origin at the typographic origin of
the I, y downwards, the unit one thousandth of an em: the baseline is
therefore at y = 700 and the top of the capitals at y = 0.
"""
import math
import sys

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

JOST = '/home/user/dicionario/pocket/fonts/Jost-Bold.ttf'
CAP = 700.0             # cap height, in units of 1000
KERN = 12.19            # 0.0045 x 311.811 pt, referred to 115.083 pt
DIAM = 1.0651 * CAP     # diameter of the disc

font = TTFont(JOST)
glyphs = font.getGlyphSet()
upm = font['head'].unitsPerEm
assert upm == 1000, upm

# --- The two letters --------------------------------------------------
x, letters = 0.0, []
for name in ('I', 'D'):
    pen = SVGPathPen(glyphs, ntos=lambda v: f'{v:.1f}')
    glyphs[name].draw(pen)
    letters.append((x, pen.getCommands()))
    x += font['hmtx'][name][0]
width_ID = x

# --- The disc ---------------------------------------------------------
cx = width_ID + KERN + DIAM / 2
cy = CAP / 2
R = DIAM / 2

# --- The star ---------------------------------------------------------
s3 = math.sqrt(3)
POINTS = [(0, 1), (-s3/12, .25), (-s3/4, .25), (-s3/6, 0), (-s3/2, -.5),
          (-s3/12, -.25), (0, -.5), (s3/12, -.25), (s3/2, -.5), (s3/6, 0),
          (s3/4, .25), (s3/12, .25)]
star = ' '.join(f'{cx + px*R:.1f},{cy - py*R:.1f}' for px, py in POINTS)

WIDTH = cx + R          # total width of the logotype

# The letters are drawn in the font's coordinate system (y upwards, origin
# on the baseline): a single transform brings them into the page's.
body = [f'<g transform="translate(0,{CAP:.0f}) scale(1,-1)" fill="currentColor">']
for dx, d in letters:
    body.append(f'<path transform="translate({dx:.0f},0)" d="{d}"/>')
body.append('</g>')
body.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}" fill="currentColor"/>')
body.append(f'<polygon class="star" points="{star}" fill="var(--star,#fbfaf7)"/>')

print(f'width={WIDTH:.1f}  ID={width_ID:.0f}  disc=({cx:.1f},{cy:.1f}) r={R:.1f}',
      file=sys.stderr)
open('/tmp/logo-body.svg', 'w').write('\n'.join(body))
open('/tmp/logo-width.txt', 'w').write(f'{WIDTH:.1f}')
