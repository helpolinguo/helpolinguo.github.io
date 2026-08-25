#!/usr/bin/env python3
"""Engendre les fichiers d'accueil pour les MACHINES : robots, plan, llms.

POURQUOI A LA RACINE. Les quatre sites partagent une origine — la page
d'accueil est le site d'utilisateur, les trois livres en sont des sites
de projet. Or « /robots.txt » et « /sitemap.xml » ne sont lus qu'a la
RACINE d'un domaine : un robots.txt depose dans /tabeli/ ne serait lu par
personne. Ces trois fichiers ne peuvent donc vivre qu'ici, et ils parlent
pour les quatre.

CE QUE CHACUN FAIT

  robots.txt   dit oui a tout le monde, nommement — y compris aux robots
               des modeles de langue, que beaucoup de sites bloquent et
               qui, faute de mention, s'abstiennent parfois d'eux-memes.
  sitemap.xml  enumere les pages pour les moteurs de recherche.
  llms.txt     la carte, a l'usage des modeles : ce que le site contient,
               sous quelle forme, ET A QUEL PRIX. C'est le poids indique
               qui compte : il permet de choisir AVANT de telecharger,
               et c'est la, bien plus que dans la compression, que
               l'economie se fait.

CE SCRIPT LIT LES DEPOTS VOISINS. Les trois livres sont des depots
separes ; le script attend leurs clones a cote de celui-ci. Il faut donc
le relancer quand un livre change, et la ligne du bas le rappelle.

    python3 outils/robotoj.py
"""

import datetime
import os
from pathlib import Path

RACINO = Path(__file__).resolve().parent.parent
VOISINS = RACINO.parent
SITO = 'https://ido.help'


def poido(p: Path) -> str:
    """Un poids lisible d'un coup d'oeil, pour choisir sans calculer."""
    n = p.stat().st_size
    if n >= 1_048_576:
        return '%.1f Mo' % (n / 1_048_576)
    if n >= 1024:
        return '%d Ko' % (n / 1024)
    return '%d o' % n


def trovar(livro: str, *nomi):
    """Les fichiers d'un livre qui existent vraiment, avec leur poids.

    On ne DECLARE jamais un fichier sans l'avoir vu : une carte qui
    annonce ce qui n'est pas la est pire qu'une carte absente.
    """
    baz = VOISINS / livro
    for n in nomi:
        f = baz / n
        if f.exists():
            yield n, poido(f)


# --------------------------------------------------------------------------
# robots.txt
# --------------------------------------------------------------------------
# Les robots des modeles de langue sont nommes UN A UN, et non couverts par
# la seule etoile. La raison est pratique : plusieurs d'entre eux cherchent
# leur propre nom avant de se rabattre sur la regle generale, et certains
# exploitants s'abstiennent quand rien ne les vise. Une permission explicite
# leve le doute. Ils ne sont pas non plus soumis a un delai : le site est
# statique et tient sur GitHub Pages, qui n'a que faire de la cadence.
ROBOTOJ = """# ido.help — tri verki dil helpolinguo internaciona Ido.
#
# Tout est ouvert, a tous, sans delai. Le site est statique : aucune
# cadence de visite ne le met en peine.
#
# Les versions LISIBLES PAR LES MACHINES sont annoncees dans /llms.txt —
# texte brut et JSON, bien moins couteux que les pages elles-memes.

User-agent: *
Allow: /

# Robots des modeles de langue, nommes un a un : plusieurs cherchent leur
# propre nom avant la regle generale, et s'abstiennent quand rien ne les
# vise. Ici, rien ne les empeche.
User-agent: ClaudeBot
Allow: /
User-agent: Claude-Web
Allow: /
User-agent: ClaudeBot-User
Allow: /
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: CCBot
Allow: /
User-agent: Applebot
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Bytespider
Allow: /
User-agent: Amazonbot
Allow: /
User-agent: meta-externalagent
Allow: /
User-agent: cohere-ai
Allow: /
User-agent: Diffbot
Allow: /
User-agent: omgili
Allow: /

Sitemap: {sito}/sitemap.xml
"""


def fari_robotoj():
    (RACINO / 'robots.txt').write_text(ROBOTOJ.format(sito=SITO), encoding='utf-8')


# --------------------------------------------------------------------------
# sitemap.xml
# --------------------------------------------------------------------------
def fari_planon(hodie: str):
    adresi = [(f'{SITO}/', '1.0'),
              (f'{SITO}/tabeli/', '0.9'),
              (f'{SITO}/dicionario/', '0.9'),
              (f'{SITO}/gramatiko/', '0.9'),
              (f'{SITO}/llms.txt', '0.5')]

    # Les derivees lisibles par les machines entrent au plan : sans cela un
    # moteur ne les trouverait que par le lien de la page, et un aspirateur
    # pas du tout.
    for livro, nomi in (('tabeli', ('tabeli.md', 'tabeli.json')),
                        ('dicionario', ('dicionario.md', 'dicionario.json',
                                        'vortlisto.md')),
                        ('gramatiko', ('gramatiko.md',))):
        for n, _ in trovar(livro, *nomi):
            adresi.append((f'{SITO}/{livro}/{n}', '0.6'))

    ch = VOISINS / 'gramatiko' / 'chapitri'
    if (ch / 'index.md').exists():
        adresi.append((f'{SITO}/gramatiko/chapitri/index.md', '0.6'))
        for f in sorted(ch.glob('*.md')):
            if f.name != 'index.md':
                adresi.append((f'{SITO}/gramatiko/chapitri/{f.name}', '0.4'))

    lin = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, prio in adresi:
        lin += ['  <url>', f'    <loc>{u}</loc>', f'    <lastmod>{hodie}</lastmod>',
                f'    <priority>{prio}</priority>', '  </url>']
    lin.append('</urlset>')
    (RACINO / 'sitemap.xml').write_text('\n'.join(lin) + '\n', encoding='utf-8')
    return len(adresi)


# --------------------------------------------------------------------------
# llms.txt
# --------------------------------------------------------------------------
def fari_llms():
    def tabelo(livro, nomi, sufixo=''):
        lin = []
        for n, p in trovar(livro, *nomi):
            lin.append(f'- [{n}]({SITO}/{livro}/{n}) — {p}{sufixo}')
        return lin

    L = [
        '# ido.help',
        '',
        '> Tri verki dil helpolinguo internaciona **Ido**, transskribita ed '
        'exhaustive serchebla : la Delmas-Tabeli (1926), la Dicionario de la '
        '10.000 radiki (1934/1964), e la Kompleta Gramatiko Detaloza (1925). '
        'Pri la yuri di singla verko, videz la pagino di la deposito.',
        '',
        'Ido esas helpolinguo internaciona, publikigita en 1907, derivita de '
        'Esperanto. Ca sito ofras la tri verki fundamentala en formo lektebla '
        'da homi ed da mashini.',
        '',
        '## Por komencar',
        '',
        'Se vu volas **lernar la gramatiko**, la chapitri esas la maxim '
        'ekonomiala voyo : singla chapitro esas apartra dosiero de cirkum '
        '10 Ko. Ne deskargez la tota libro por un questiono.',
        '',
        '- [Tabelo dil chapitri](%s/gramatiko/chapitri/index.md) — la 49 '
        'chapitri, kun lia grandeso' % SITO,
        '',
        'Se vu volas **serchar vorto**, la vortlisto esas kurta ; la kompleta '
        'artikli esas plu longa.',
        '',
        '## Gramatiko — *Kompleta Gramatiko Detaloza*, L. de Beaufront, 1925',
        '',
    ]
    L += ['- [chapitri/index.md](%s/gramatiko/chapitri/index.md) — la tabelo, '
          'kun la grandeso di singla chapitro' % SITO]
    ch = VOISINS / 'gramatiko' / 'chapitri'
    if ch.exists():
        n = len([f for f in ch.glob('*.md') if f.name != 'index.md'])
        L += ['- %d chapitri apartra, en `%s/gramatiko/chapitri/` — '
              'cirkum 10 Ko singla' % (n, SITO)]
    L += tabelo('gramatiko', ('gramatiko.md',), ' — la tota libro')
    L += ['- [gramatiko/](%s/gramatiko/) — la pagino, kun sercho' % SITO, '']

    L += ['## Dicionario — *Dicionario de la 10.000 radiki*, M. Pesch, 1934/1964',
          '']
    L += tabelo('dicionario', ('vortlisto.md',), ' — vedvorto e unesma senco nur')
    L += tabelo('dicionario', ('dicionario.md',), ' — la kompleta artikli')
    L += tabelo('dicionario', ('dicionario.json',), ' — la datumi, por interogar')
    L += ['- [dicionario/](%s/dicionario/) — la pagino, kun sercho' % SITO, '']

    L += ['## Tabeli — *Expliko-Libreto di la Delmas-Tabeli*, J. Guignon, 1926',
          '',
          'Tabelo komparanta en **57 lingui**. La klefi di `tabeli.json` esas '
          'ti di `lingui/*.json` : por obtenar irga paro di lingui, junktez li '
          'per la klefo.',
          '']
    L += tabelo('tabeli', ('tabeli.md',), ' — Ido e Franca en regardo')
    L += tabelo('tabeli', ('tabeli.json',), ' — la klefi e la du lingui')
    L += tabelo('tabeli', ('lingui/index.json',), ' — la 55 altra lingui ofrata')
    L += ['- [tabeli/](%s/tabeli/) — la pagino, kun sercho' % SITO, '']

    L += ['## Noti',
          '',
          '- La `.md` e `.json` esas ENGENDRATA de la pagini. La fonto restas '
          '`index.html` en singla deposito.',
          '- Nula limito di frequeso : la sito esas statika.',
          '- Kodexo e transskribi : https://github.com/GPhMorin',
          '']
    (RACINO / 'llms.txt').write_text('\n'.join(L), encoding='utf-8')


def main():
    hodie = os.environ.get('DATO') or datetime.date.today().isoformat()
    fari_robotoj()
    n = fari_planon(hodie)
    fari_llms()
    for f in ('robots.txt', 'sitemap.xml', 'llms.txt'):
        print('  %-14s %8s' % (f, poido(RACINO / f)))
    print('  %d adresses au plan du site' % n)
    print('  (relancer quand un livre change : le script lit les depots voisins)')


if __name__ == '__main__':
    main()
