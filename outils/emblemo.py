#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reconstruction du logotype IDO azur de la page de titre du Dicionario.

Tout ce qui suit est RELEVE sur `dicionario/posho/kovrilo.tex` et verifie
sur la page 3 de `dicionario.pdf` (cote impair, page de titre) :

  * les lettres ID sont composees en Jost* Bold, corps 115,083 pt ;
  * le disque suit le D a 0,0045 x largeur-de-page, soit 12,19/1000 em ;
  * son diametre vaut 1,0651 fois la hauteur de capitale (700/1000 em) ;
  * il est centre sur la hauteur de capitale ;
  * l'etoile est reguliere, construite selon les quatre regles de
    kovrilo.tex, ses trois longues pointes sur le cercle et ses trois
    petites a mi-rayon.

Le repere de sortie a pour origine l'origine typographique du I, l'axe y
vers le bas, l'unite le millieme de cadratin : la ligne de base est donc
a y = 700 et le haut des capitales a y = 0.
"""
import math, subprocess, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

JOST = '/home/user/dicionario/posho/polices/Jost-Bold.ttf'
CAP = 700.0            # hauteur de capitale, en unites de 1000
KERN = 12.19           # 0,0045 x 311,811 pt rapporte au corps 115,083
DIAM = 1.0651 * CAP    # diametre du disque

f = TTFont(JOST)
gs = f.getGlyphSet()
upm = f['head'].unitsPerEm
assert upm == 1000, upm

# --- Les deux lettres -------------------------------------------------
x, letters = 0.0, []
for g in ('I', 'D'):
    pen = SVGPathPen(gs, ntos=lambda v: f'{v:.1f}')
    gs[g].draw(pen)
    letters.append((x, pen.getCommands()))
    x += f['hmtx'][g][0]
largo_ID = x

# --- Le disque --------------------------------------------------------
cx = largo_ID + KERN + DIAM / 2
cy = CAP / 2
R = DIAM / 2

# --- L'etoile ---------------------------------------------------------
s3 = math.sqrt(3)
POINTI = [(0, 1), (-s3/12, .25), (-s3/4, .25), (-s3/6, 0), (-s3/2, -.5),
          (-s3/12, -.25), (0, -.5), (s3/12, -.25), (s3/2, -.5), (s3/6, 0),
          (s3/4, .25), (s3/12, .25)]
stelo = ' '.join(f'{cx + px*R:.1f},{cy - py*R:.1f}' for px, py in POINTI)

LARGO = cx + R          # largeur totale du logotype

# Les lettres sont dessinees dans le repere de la fonte (y vers le haut,
# origine sur la ligne de base) : une seule transformation les amene dans
# le repere de la page.
korpo = [f'<g transform="translate(0,{CAP:.0f}) scale(1,-1)" fill="currentColor">']
for dx, d in letters:
    korpo.append(f'<path transform="translate({dx:.0f},0)" d="{d}"/>')
korpo.append('</g>')
korpo.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}" fill="currentColor"/>')
korpo.append(f'<polygon class="stelo" points="{stelo}" fill="var(--stelo,#fbfaf7)"/>')

print(f'largeur={LARGO:.1f}  ID={largo_ID:.0f}  disque=({cx:.1f},{cy:.1f}) r={R:.1f}',
      file=sys.stderr)
open('/tmp/logo-korpo.svg', 'w').write('\n'.join(korpo))
open('/tmp/logo-largo.txt', 'w').write(f'{LARGO:.1f}')
