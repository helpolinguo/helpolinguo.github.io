#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fabrique les images fixes de la page d'accueil, a partir du meme releve
que `emblemo.py` :

  emblemo.svg          l'embleme seul, carre — favicon
  apple-touch-icon.png le meme, 180 x 180, sur fond azur
  og-imajo.png         1200 x 630, la marque et la devise — partage

Dans les PNG, la devise est convertie en COURBES : le rasteriseur ne
resout pas les polices par leur nom, et une image de partage ne doit
dependre de rien.
"""
import math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import pymupdf

POL = '/home/user/dicionario/posho/polices/'
AZUR, PAPER, ENK = '#007FFF', '#fbfaf7', '#1a1a1a'
CAP, KERN = 700.0, 12.19
DIAM = 1.0651 * CAP
s3 = math.sqrt(3)

bold = TTFont(POL + 'Jost-Bold.ttf')
med = TTFont(POL + 'Jost-Medium.ttf')


def kurbi(font, txt, tracking=0.0):
    """Le texte en courbes, dans le repere de la fonte (y vers le haut)."""
    gs, cmap, hm = font.getGlyphSet(), font.getBestCmap(), font['hmtx']
    x, out = 0.0, []
    for c in txt:
        g = cmap[ord(c)]
        pen = SVGPathPen(gs, ntos=lambda v: f'{v:.1f}')
        gs[g].draw(pen)
        d = pen.getCommands()
        if d:
            out.append(f'<path transform="translate({x:.1f},0)" d="{d}"/>')
        x += hm[g][0] + tracking
    return '\n'.join(out), x - tracking


# --- L'embleme --------------------------------------------------------
POINTI = [(0, 1), (-s3/12, .25), (-s3/4, .25), (-s3/6, 0), (-s3/2, -.5),
          (-s3/12, -.25), (0, -.5), (s3/12, -.25), (s3/2, -.5), (s3/6, 0),
          (s3/4, .25), (s3/12, .25)]


def stelo(cx, cy, R, koloro):
    p = ' '.join(f'{cx+px*R:.2f},{cy-py*R:.2f}' for px, py in POINTI)
    return f'<polygon points="{p}" fill="{koloro}"/>'


# emblemo.svg — l'embleme seul, le disque touchant les bords
emb = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
       f'<circle cx="16" cy="16" r="16" fill="{AZUR}"/>'
       f'{stelo(16, 16, 16, "#ffffff")}</svg>')
open('emblemo.svg', 'w').write(emb)

# apple-touch-icon : le meme, avec une marge — iOS arrondit l'angle
ati = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180">'
       f'<rect width="180" height="180" fill="{AZUR}"/>'
       f'<circle cx="90" cy="90" r="62" fill="#ffffff"/>'
       f'{stelo(90, 90, 62, AZUR)}</svg>')
# La boite du SVG est en points ; a 72 ppp, un point vaut un pixel.
pymupdf.open(stream=ati.encode(), filetype='svg')[0]\
    .get_pixmap(dpi=72).save('apple-touch-icon.png')

# --- L'image de partage ----------------------------------------------
letroj, largo_ID = kurbi(bold, 'ID')
cx, cy, R = largo_ID + KERN + DIAM/2, CAP/2, DIAM/2
LARGO = cx + R - 74                       # de l'encre du I au bord du disque
ALTO = DIAM                               # le disque deborde la capitale

# La devise reprend les proportions de la page : corps de 132 pour une
# largeur de logotype de 1736,76, et une approche de 0,102 cadratin —
# les deux valeurs qui, ensemble, lui font exactement cette largeur.
KORPO_REL, APROX_REL = 132/LARGO, 0.102
LOGO_L = 620.0                            # largeur de la marque dans l'image
O = (1200, 630)
k = LOGO_L / LARGO

korpo_dev = KORPO_REL * LOGO_L            # corps de la devise, en pixels
trakt = APROX_REL * 1000                  # approche, en unites de fonte
deviz, natur = kurbi(med, 'helpolinguo internaciona', tracking=trakt)
esk = LOGO_L / (natur - 69 - 57)          # approches extremes retranchees

# Pose verticale : le bloc — marque, blanc, devise — centre sur l'image.
ALTO_LOGO = ALTO * k
BLANKO = 0.155 * ALTO_LOGO
CAP_DEV = CAP * esk
DESC_DEV = 215 * esk
BLOKO = ALTO_LOGO + BLANKO + CAP_DEV + DESC_DEV
y0 = (O[1] - BLOKO) / 2
x0 = (O[0] - LOGO_L) / 2
baz = y0 + ALTO_LOGO + BLANKO + CAP_DEV   # ligne de base de la devise

og = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {O[0]} {O[1]}">
<rect width="{O[0]}" height="{O[1]}" fill="{PAPER}"/>
<g transform="translate({x0:.2f},{y0:.2f}) scale({k:.5f}) translate(-74,22.79)">
  <g transform="translate(0,{CAP:.0f}) scale(1,-1)" fill="{AZUR}">{letroj}</g>
  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}" fill="{AZUR}"/>
  {stelo(cx, cy, R, PAPER)}
</g>
<g transform="translate({x0:.2f},{baz:.2f}) scale({esk:.6f},{-esk:.6f}) translate(-69,0)"
   fill="{ENK}" fill-opacity=".82">{deviz}</g>
</svg>'''
open('/tmp/og.svg', 'w').write(og)
pymupdf.open(stream=og.encode(), filetype='svg')[0]\
    .get_pixmap(dpi=72).save('og-imajo.png')
print('emblemo.svg, apple-touch-icon.png, og-imajo.png')
