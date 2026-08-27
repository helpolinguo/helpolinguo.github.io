#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds the home page's fixed images, from the same measurements as
`emblem.py`:

  emblem.svg           the emblem alone, square — favicon
  apple-touch-icon.png the same, 180 x 180, on an azure ground
  icon-192.png         }  the manifest's icons, azure ground
  icon-512.png         }
  icon-1536.png        the same drawing again, for the lock screen — see below
  og-image.png         1200 x 630, the mark and the motto — for sharing

In the PNGs the motto is converted to OUTLINES: the rasteriser does not
resolve fonts by name, and a sharing image must depend on nothing.
"""
import math

import pymupdf
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

FONTS = '/home/user/dicionario/pocket/fonts/'
AZURE, PAPER, INK = '#007FFF', '#fbfaf7', '#1a1a1a'
CAP, KERN = 700.0, 12.19
DIAM = 1.0651 * CAP
s3 = math.sqrt(3)

bold = TTFont(FONTS + 'Jost-Bold.ttf')
medium = TTFont(FONTS + 'Jost-Medium.ttf')


def outlines(font, text, tracking=0.0):
    """The text as outlines, in the font's coordinate system (y upwards)."""
    glyphs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font['hmtx']
    x, out = 0.0, []
    for ch in text:
        name = cmap[ord(ch)]
        pen = SVGPathPen(glyphs, ntos=lambda v: f'{v:.1f}')
        glyphs[name].draw(pen)
        d = pen.getCommands()
        if d:
            out.append(f'<path transform="translate({x:.1f},0)" d="{d}"/>')
        x += hmtx[name][0] + tracking
    return '\n'.join(out), x - tracking


# --- The emblem -------------------------------------------------------
POINTS = [(0, 1), (-s3/12, .25), (-s3/4, .25), (-s3/6, 0), (-s3/2, -.5),
          (-s3/12, -.25), (0, -.5), (s3/12, -.25), (s3/2, -.5), (s3/6, 0),
          (s3/4, .25), (s3/12, .25)]


def star(cx, cy, R, colour):
    p = ' '.join(f'{cx+px*R:.2f},{cy-py*R:.2f}' for px, py in POINTS)
    return f'<polygon points="{p}" fill="{colour}"/>'


# emblem.svg — the emblem alone, the disc touching the edges
emblem = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
          f'<circle cx="16" cy="16" r="16" fill="{AZURE}"/>'
          f'{star(16, 16, 16, "#ffffff")}</svg>')
open('emblem.svg', 'w').write(emblem)

# apple-touch-icon: the same, with a margin — iOS rounds the corner
touch = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180">'
         f'<rect width="180" height="180" fill="{AZURE}"/>'
         f'<circle cx="90" cy="90" r="62" fill="#ffffff"/>'
         f'{star(90, 90, 62, AZURE)}</svg>')
# The SVG's box is in points; at 72 dpi a point is a pixel.
pymupdf.open(stream=touch.encode(), filetype='svg')[0]\
    .get_pixmap(dpi=72).save('apple-touch-icon.png')

# The manifest's icons — 192 and 512, on an azure ground like the iOS one —
# and 1536, WHICH IS NOT ONE OF THEM.
#
# 1536 IS FOR THE LOCK SCREEN. When the song behind the seven clicks plays,
# iOS puts it in its Now Playing panel and looks for an artwork; without one
# named it takes the largest icon the manifest offers, which was 512.
# MEASURED, from a screenshot of an iPhone 16 Pro at 1206 x 2622: the panel
# draws that artwork 1111 px wide. 512 was being blown up 2.17 times, and it
# showed — the star's edges came out stepped. 1024 would still be an
# upscale; 1536 is three times 512, covers 1111 with a third to spare, and
# costs what a flat two-colour PNG costs.
#
# It is deliberately NOT in the manifest. Nothing installs from it: a
# launcher offered a 1536 icon may fetch it in place of the 512 it wants,
# and this file is meant to be fetched by the readers who find the egg, at
# the moment they find it, and by nobody else.
for size in (192, 512, 1536):
    r = size * 62 / 180
    icon = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">'
            f'<rect width="{size}" height="{size}" fill="{AZURE}"/>'
            f'<circle cx="{size/2}" cy="{size/2}" r="{r}" fill="#ffffff"/>'
            f'{star(size/2, size/2, r, AZURE)}</svg>')
    pymupdf.open(stream=icon.encode(), filetype='svg')[0]\
        .get_pixmap(dpi=72).save(f'icon-{size}.png')

# --- The sharing image ------------------------------------------------
letters, width_ID = outlines(bold, 'ID')
cx, cy, R = width_ID + KERN + DIAM/2, CAP/2, DIAM/2
WIDTH = cx + R - 74                       # from the ink of the I to the edge of the disc
HEIGHT = DIAM                             # the disc overshoots the capitals

# The motto keeps the page's proportions: a type size of 132 for a logotype
# width of 1736.76, and a tracking of 0.102 em — the two values which,
# together, give it exactly that width.
SIZE_REL, TRACK_REL = 132/WIDTH, 0.102
LOGO_W = 620.0                            # width of the mark within the image
OUT = (1200, 630)
k = LOGO_W / WIDTH

motto_size = SIZE_REL * LOGO_W            # type size of the motto, in pixels
tracking = TRACK_REL * 1000               # tracking, in font units
motto, natural = outlines(medium, 'helpolinguo internaciona', tracking=tracking)
scale = LOGO_W / (natural - 69 - 57)      # extreme side bearings taken off

# Vertical placement: the block — mark, white space, motto — centred on the
# image.
LOGO_H = HEIGHT * k
GAP = 0.155 * LOGO_H
MOTTO_CAP = CAP * scale
MOTTO_DESC = 215 * scale
BLOCK = LOGO_H + GAP + MOTTO_CAP + MOTTO_DESC
y0 = (OUT[1] - BLOCK) / 2
x0 = (OUT[0] - LOGO_W) / 2
baseline = y0 + LOGO_H + GAP + MOTTO_CAP  # baseline of the motto

og = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {OUT[0]} {OUT[1]}">
<rect width="{OUT[0]}" height="{OUT[1]}" fill="{PAPER}"/>
<g transform="translate({x0:.2f},{y0:.2f}) scale({k:.5f}) translate(-74,22.79)">
  <g transform="translate(0,{CAP:.0f}) scale(1,-1)" fill="{AZURE}">{letters}</g>
  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}" fill="{AZURE}"/>
  {star(cx, cy, R, PAPER)}
</g>
<g transform="translate({x0:.2f},{baseline:.2f}) scale({scale:.6f},{-scale:.6f}) translate(-69,0)"
   fill="{INK}" fill-opacity=".82">{motto}</g>
</svg>'''
open('/tmp/og.svg', 'w').write(og)
pymupdf.open(stream=og.encode(), filetype='svg')[0]\
    .get_pixmap(dpi=72).save('og-image.png')
print('emblem.svg, apple-touch-icon.png, icon-192.png, icon-512.png,\n'
      'icon-1536.png, og-image.png')
