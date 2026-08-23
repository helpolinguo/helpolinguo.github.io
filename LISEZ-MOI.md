# ido.help — page d'accueil

Une seule page, sans défilement, qui réunit les trois livres transcrits :

| bouton | dépôt | livre |
|---|---|---|
| **Tabeli** | `GPhMorin/tabeli` | *Expliko-Libreto di la Delmas-Tabeli helpanta*, 1926 |
| **Dicionario** | `GPhMorin/dicionario` | *Dicionario de la 10.000 radiki*, 1964 |
| **Gramatiko** | `GPhMorin/gramatiko` | *Kompleta Gramatiko Detaloza*, 1925 |

```
index.html            la page entière — structure, style et script
emblemo.svg           l'emblème seul (favicon)
apple-touch-icon.png  le même, 180 × 180
og-imajo.png          1200 × 630, l'image de partage
polices/              Jost* Bold et Medium, réduites à cette page
outils/emblemo.py     reconstruit le logotype
outils/ikoni.py       refabrique les trois images ci-dessus
CNAME                 le domaine, pour GitHub Pages
```

---

## 1. Pourquoi ce dépôt s'appelle `gphmorin.github.io`

Le nom n'est pas un choix : c'est lui qui fait tenir les adresses.

GitHub Pages sert deux sortes de sites, et une seule des deux donne
`ido.help/tabeli` :

* le **site d'utilisateur**, servi depuis le dépôt qui porte exactement le
  nom `gphmorin.github.io`, à la racine ;
* les **sites de projet**, un par dépôt, servis sous le nom du dépôt.

Quand un domaine personnalisé est posé **sur le site d'utilisateur**, GitHub
lui rattache tout l'arbre — la racine *et* tous les sites de projet du même
compte :

```
ido.help/              <- ce dépôt
ido.help/tabeli/       <- le dépôt tabeli,      automatiquement
ido.help/dicionario/   <- le dépôt dicionario,  automatiquement
ido.help/gramatiko/    <- le dépôt gramatiko,   automatiquement
```

Posé sur un dépôt de projet, le domaine servirait bien cette page à la
racine, mais `ido.help/tabeli` répondrait 404. D'où le nom, et d'où le fait
que le nom du dépôt ne rappelle plus le domaine : celui-ci vit dans le
fichier `CNAME`.

### Comment on en est arrivé là

Le nom était pris par le site *Rare diseases* de juin 2021. Trois contraintes
ont dicté l'ordre des opérations, et méritent d'être notées si l'arrangement
doit un jour être refait :

* **archiver ne libère pas un nom** — un compte ne peut pas avoir deux dépôts
  homonymes ;
* **un dépôt archivé est en lecture seule**, donc impossible à renommer sans
  le désarchiver, et impossible à recevoir un `push` ;
* la redirection que GitHub pose à chaque renommage tombe dès qu'un autre
  dépôt reprend l'ancien nom.

Le site de 2021 a donc d'abord été renommé `rare-diseases`, puis archivé — il
continue d'être servi, un dépôt archivé gardant ses pages, mais sous
`ido.help/rare-diseases/`. Ses anciennes adresses n'ont pas survécu au
déplacement : il n'y avait pas moyen de les garder tout en mettant autre
chose à la racine. Le dépôt `ido.help`, où cette page a été écrite, a ensuite
pris le nom libéré, avec son historique et ses PR.

### Les réglages qui doivent rester en place

**Settings → Pages** de ce dépôt :

* *Source* : `main`, dossier `/` ;
* *Custom domain* : `ido.help` — le fichier `CNAME`, à la racine, le porte ;
* *Enforce HTTPS*.

Chez le registraire de `ido.help` :

| type | nom | valeur |
|---|---|---|
| A | `@` | `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153`, `…8001::153`, `…8002::153`, `…8003::153` |
| CNAME | `www` | `gphmorin.github.io.` |

### Ce qui ne doit pas être rompu

* **Aucun des trois dépôts de livres ne doit avoir son propre domaine
  personnalisé.** Ils n'en ont pas — pas de fichier `CNAME` — et c'est
  précisément ce qui leur permet d'être servis sous `ido.help/…`.
* **Le fichier `CNAME` ne doit pas disparaître.** Le supprimer détacherait le
  domaine, et les trois adresses avec lui.
* Les liens des trois boutons sont **absolus depuis la racine** (`/tabeli/`).
  Ils valent donc aussi bien sous `gphmorin.github.io/` que sous `ido.help/` :
  il n'y a rien à changer si le domaine devait tomber ou revenir.
* Les sous-domaines `*.ido.li` sont de simples redirections HTTP chez IONOS
  (`217.160.0.251`) vers `gphmorin.github.io/<dépôt>`. Ils continuent de
  fonctionner : GitHub redirige à son tour vers `ido.help/<dépôt>`. On peut
  aussi les repointer directement, ou les garder comme adresses courtes.

---

## 2. Le logotype

L'IDO azur est celui de la **page de titre** du *Dicionario* (page 3 de
`dicionario.pdf`, celle où le lettrage est bleu sur blanc). Il n'est pas
repris en image : il est **reconstruit en courbes**, à l'identique, par
`outils/emblemo.py`, d'après le relevé qui se trouve déjà dans
`dicionario/posho/kovrilo.tex` :

* les lettres **ID** sont les contours de Jost\* Bold, chasses comprises ;
* le disque suit le D à 0,0045 × largeur-de-page, soit 12,19 millièmes de
  cadratin, et son diamètre vaut 1,0651 fois la hauteur de capitale ;
* l'**étoile** est régulière et construite, non décalquée : trois longues
  pointes sur le cercle, trois petites à mi-rayon, la base d'une longue
  pointe valant le tiers du côté du triangle central.

La largeur totale calculée — 1810,8 millièmes de cadratin — retombe au
dixième près sur celle mesurée dans le PDF (208,389 pt à corps 115,083).

La boîte du SVG est celle de l'**encre** et non celle de la chasse : elle
commence à l'approche gauche du I et finit au bord du disque, et déborde la
hauteur de capitale de 22,79 millièmes en haut comme en bas, puisque le
disque est plus haut que les lettres. C'est ce qui permet à la devise de
faire *exactement* la largeur de ce qu'on voit.

**L'étoile tourne.** Un clic sur la marque la fait pivoter d'un tiers de
tour — et elle revient sur elle-même, puisque la figure est invariante par
rotation de 120 degrés. C'est la seule fantaisie de la page, et elle dit
quelque chose de vrai sur le dessin.

---

## 3. La devise

« helpolinguo internaciona » fait la largeur du logotype **au pixel près, à
toute taille**. Le texte est posé dans un SVG de même boîte, avec
`textLength` et `lengthAdjust="spacing"` : c'est l'approche entre les lettres
qui s'étire, jamais leur dessin. L'accord ne dépend donc pas de la police
réellement chargée — il tient même si Jost\* n'arrive pas.

Le corps, 132 millièmes, et les approches extrêmes retranchées donnent une
interlettre de 0,102 cadratin : assez pour que la ligne respire sous une
marque de cette taille, pas assez pour la disloquer.

---

## 4. Le ciel

« Langue auxiliaire internationale » dans **soixante langues nationales**,
posées derrière la marque. Le script les place sur les rectangles réels : deux
mots ne se recouvrent jamais, et aucun n'approche le bloc central. Chacun
dérive à son pas ; le calque entier se décale de quelques pixels sous le
pointeur. Sous un vrai pointeur, survoler un mot affiche le nom de sa langue.

Le tirage est pseudo-aléatoire **à graine fixe** : la disposition est la même
à chaque visite pour une même fenêtre. Sur une petite fenêtre, où le bloc
central occupe les deux tiers de la place, les écarts se resserrent et les
essais se multiplient — sans quoi il ne resterait que six ou sept mots.

`prefers-reduced-motion` arrête la dérive et la parallaxe.

> **À relire.** Les traductions ont été écrites à la main. Celles dont je suis
> le moins sûr, et qui gagneraient à être vérifiées par quelqu'un qui parle la
> langue : le basque, le gallois, l'irlandais, le philippin, le swahili, le
> mongol, le kazakh, le tamoul et le thaï. Elles sont toutes dans le tableau
> `VORTI`, au début du script, une ligne par langue.

---

## 5. La page ne défile pas

Ni sur écran, ni sur téléphone. La scène est fixée à la vue (`100dvh`, qui
suit la barre d'adresse quand elle se rétracte), et tout ce qu'elle contient
est mesuré en `svh` — la **plus petite** hauteur que le navigateur puisse
offrir, celle où la barre d'adresse est déployée. Le bloc tient donc dans le
cas le plus étroit, et rien ne dépasse dans les autres.

Une seule mesure commande la page, `--largo` :

```css
--largo: min(74vw, 54svh, 560px)
```

C'est la largeur du logotype ; la devise et les trois boutons s'y alignent.
Bornée à la fois par la largeur de la vue, par sa hauteur et par un maximum
absolu, elle tient aussi bien sur un téléphone couché (844 × 390) que sur un
grand écran. Sur un téléphone tenu debout et étroit, les trois boutons passent
l'un sous l'autre — trois mots côte à côte deviennent illisibles bien avant
d'être à l'étroit.

Vérifié dans Chromium à 1440 × 900, 820 × 1180, 390 × 844, 844 × 390 et
320 × 568, en thème clair et en thème sombre : `scrollHeight` égale
`clientHeight` partout.

---

## 6. Ce que la page demande au réseau

Rien, hors d'elle-même. Le style et le script sont dans `index.html` ; les
deux polices sont servies par le site (5,7 ko chacune, réduites aux seuls
signes employés) ; le logotype est du SVG. Aucune requête vers un tiers, donc
aucun traceur. Sans JavaScript, la page reste entière — marque, devise et
trois boutons ; seul le ciel manque.

Les couleurs sont les cinq jetons des trois pages de lecture — papier
`#fbfaf7`, encre `#1a1a1a`, gris `#6b6560`, filet `#e2ddd5` — plus l'azur du
livre, `#007FFF`. Le thème sombre reprend les mêmes valeurs que les trois
autres pages ; l'azur s'y éclaircit en `#4da3ff`, faute de quoi il ne tiendrait
pas le contraste sur `#16161a`.

---

## 7. Refabriquer les images

```sh
python3 outils/emblemo.py   # le logotype, à recopier dans index.html
python3 outils/ikoni.py     # emblemo.svg, apple-touch-icon.png, og-imajo.png
```

Les deux scripts lisent `Jost-Bold.ttf` et `Jost-Medium.ttf` dans
`dicionario/posho/polices/` ; ils demandent `fonttools` et `pymupdf`.

Jost\* est sous licence SIL OFL 1.1 — voir `polices/OFL.txt` et
`polices/LISEZ-MOI.md`.
