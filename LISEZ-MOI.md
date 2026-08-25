# ido.help — page d'accueil

Une seule page, sans défilement, qui réunit les trois livres transcrits :

| bouton | dépôt | livre |
|---|---|---|
| **Tabeli** | `GPhMorin/tabeli` | *Expliko-Libreto di la Delmas-Tabeli helpanta*, 1926 |
| **Dicionario** | `GPhMorin/dicionario` | *Dicionario de la 10.000 radiki*, 1934/1964 |
| **Gramatiko** | `GPhMorin/gramatiko` | *Kompleta Gramatiko Detaloza*, 1925 |

```
index.html            la page entière — structure, style et script
sw.js                 le servanto : hors-ligne pour les quatre pages (§ 9)
manifest.webmanifest  le nom et les icônes de l'application (§ 9)
pordo.css             le bouton de retour des trois livres (§ 8)
emblemo.svg           l'emblème seul (favicon) et le dessin du bouton
apple-touch-icon.png  le même, 180 × 180 ; ikono-192/512.png pour le manifeste
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

## 5. L'entrée

Au chargement, on ne voit d'abord que le disque : il entre par la gauche en
**roulant**, et les deux lettres se tracent à mesure qu'il les dépasse. Puis
la devise, les trois portes et le pied montent d'un cran. L'ensemble dure une
seconde et demie.

**La distance n'est pas choisie à l'œil.** Une roue qui roule tourne d'un
angle proportionnel au chemin parcouru : un tiers de tour vaut exactement un
rayon fois 2π/3, soit 780,76 millièmes de cadratin. Le trajet en vaut deux —
1561,52 —, et ce nombre a deux conséquences heureuses :

1. l'étoile étant invariante par rotation d'un tiers de tour, elle **arrive
   dans sa position canonique sans le moindre recalage** ;
2. au départ, le bord droit du disque tombe à 249,3, et l'encre du I finit à
   246 : le disque **couvre exactement le I**, ni plus ni moins.

Le roulement est donc vrai, non mimé. C'est la même figure que le clic fait
tourner ensuite, d'un tiers de tour à son tour (§ 2).

**Les lettres ne sont pas animées : c'est un rideau qui les découvre.** Elles
étaient d'abord découpées chacune par sa propre animation, avec son propre
retard — et la coupure verticale se détachait du disque, qui avait déjà roulé
plus loin. On voyait la limite de l'animation au lieu de voir la roue poser
les lettres.

Le rideau est un rectangle de la couleur du papier, posé par-dessus les
lettres et sous le disque, dont le bord gauche suit exactement le centre du
disque : même durée, même retard, même courbe d'accélération, et une
translation qui est la *même fonction du temps*. Les deux ne peuvent donc plus
se désaccorder — ce n'est pas un réglage, c'est une identité.

**Et la coupure est invisible**, pour la raison même que vous relèverez en
regardant la marque : le disque est plus haut que les lettres, 745,6 contre
700 de hauteur de capitale. Au sommet des capitales, là où il est le plus
étroit, il s'étend encore de 128,3 millièmes de part et d'autre de son centre.
Le bord du rideau, qui passe par ce centre, est donc couvert sur toute la
hauteur où il est peint.

Le rideau est confiné à la boîte de l'encre des lettres, élargie de trois
millièmes sur les quatre côtés : sans cette marge, son bord tombait exactement
sur celui des lettres et les deux anticrénelages ne se recouvraient pas tout à
fait — il restait une ligne d'un pixel, azurée, sur la ligne de base. La marge
ne compromet rien : à y = −3 comme à y = 703, le disque s'étend encore de
119,8 millièmes de part et d'autre de son centre. Hors de cette boîte, le
rideau s'efface de lui-même — à la fin du roulement comme au repos.

Trois précautions :

* la classe `enkonduko` est posée **dans le HTML** et non par le script —
  sinon la page serait peinte une fois dans son état final avant que le
  script n'agisse, et l'entrée commencerait par un sursaut ;
* elle est retirée quand la roue s'arrête, mais aussi **au premier geste** :
  qui touche la page a autre chose à faire que regarder une animation. Le
  retrait fige tout dans l'état final, l'entrée est donc abrégeable à tout
  instant. Un filet de sécurité la retire de toute façon au bout de 3,2 s ;
* `prefers-reduced-motion` la supprime entièrement : la page se peint dans
  son état final.

Sans JavaScript, l'entrée se déroule quand même — elle est en CSS — et se
termine d'elle-même sur l'état final.

---

## 6. La page ne défile pas

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

## 7. Ce que la page demande au réseau

Rien, hors d'elle-même — `sw.js` et `manifest.webmanifest` (§ 9) sont servis
par le site comme le reste. Le style et le script sont dans `index.html` ; les
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

## 8. La feuille commune aux trois livres

Les trois livres portent, dans le coin inférieur gauche, l'emblème azur en
petit : un lien vers cette page. **Toute son apparence tient dans un seul
fichier**, `pordo.css`, servi depuis cette racine.

C'est possible parce que les quatre sites sont servis depuis la **même
origine** — c'est tout l'objet du § 1. Un fichier posé ici est lisible par
`ido.help/tabeli/`, `…/dicionario/` et `…/gramatiko/`. Chacun des trois
dépôts n'en porte donc que trois lignes, qui ne changeront plus :

```html
<link rel="stylesheet" href="/pordo.css">
<script src="/pordo.js" defer></script>
<a class="ido-pordo" href="/">Ido</a>
```

Le mot « Ido » est dans le lien et non dans la feuille : si celle-ci ne se
charge pas — page ouverte hors du site, fichier déplacé — il reste un lien
lisible en fin de document au lieu d'un carré vide.

**Il est caché par un corps nul, et non par le débordement.** Il était
d'abord poussé hors du disque par `text-indent`, et c'est `overflow: hidden`
qui le retenait — mais le débordement doit être rendu visible au survol,
sinon l'étiquette ne pourrait pas sortir du disque. Le mot sortait donc avec
elle, et « Ido » paraissait deux fois : une en étiquette, une en toutes
lettres, dans la police et la couleur des liens. Un corps nul ne dépend
d'aucun débordement.

**Et l'étiquette ne compte pas dans le nom du lien.** Le navigateur ajoute le
contenu du pseudo-élément au nom accessible, qui devenait « Ido Ido » — le
même doublon, mais pour qui écoute la page. La syntaxe
`content: "Ido" / ""` lui donne un texte de remplacement vide : elle se voit,
elle ne se dit plus. Elle est posée sous `@supports`, car un navigateur qui
l'ignore écarterait la déclaration entière, et l'étiquette ne paraîtrait plus
du tout. Le dessin, lui, est
`emblemo.svg`, déjà servi comme icône de cette page : un seul fichier pour
les quatre.

Retoucher le bouton — taille, couleur, position, étiquette — se fait donc
**ici seulement**, et les trois livres suivent au prochain rafraîchissement.
GitHub Pages sert ses fichiers avec un cache de dix minutes ; c'est le
délai qu'il faut compter.

Deux choses à savoir :

* **L'écart au coin est de 24 px, et ce n'est pas un réglage d'apparence.**
  Un écran de téléphone a des coins arrondis, et l'arrondi mange la vue en
  diagonale : un coin de rayon *r* coupe tout ce qui se trouve, sur la
  diagonale, à moins de *r*(√2−1) ≈ 0,414 *r* du coin. Le point du disque le
  plus proche du coin est à √2(*m* + *R*) − (*R* + *h*), où *m* est l'écart,
  *R* le rayon du disque et *h* le halo. Avec l'écart de 12 px qu'avait
  d'abord ce bouton, cela donnait 20,8 px : il fallait un écran de rayon
  inférieur à 50 px pour que rien ne soit rogné — or un iPhone récent tourne
  autour de 55 à 62, et le bouton y était mangé. À 24 px, le jeu passe à
  37,8 px et tient jusqu'à un rayon de 91. Le nombre est isolé dans la
  variable `--marjo`, en tête de `pordo.css`.

  Les encoches restent prises en compte par-dessus, `max` retenant la plus
  grande des deux contraintes — mais `env(safe-area-inset-*)` ne vaut que sur
  une page déclarant `viewport-fit=cover`, ce que les trois livres ne font
  pas. C'est donc bien l'écart littéral qui les protège.

* **Sur les deux livres à volet latéral** — la *Gramatiko* et les *Tabeli* —
  le disque flotte au-dessus de la table des matières et en recouvre le
  début d'une ligne. La ligne reste cliquable : le disque fait 42 px sur
  une colonne de 250, et le lien s'atteint partout ailleurs. Réserver le
  coin demanderait de retoucher la mise en page de chaque livre, ce qui
  ferait perdre le bénéfice du fichier unique.
* **Le bouton est posé par le haut, et non par le bas.** Sur iPhone, la barre
  d'adresse se rétracte quand on descend dans la page, et le bas de la vue
  change alors de place : un bouton posé par `bottom` suivait ce bas, et
  bougeait — alors qu'un point de repère ne doit pas bouger. Il est donc posé
  par le haut, un bord qui ne bouge jamais, à la hauteur de la vue **la plus
  petite** que le navigateur puisse offrir :

  ```css
  top: calc(100svh - var(--grando) - max(var(--marjo), env(safe-area-inset-bottom)))
  ```

  `svh` ne varie pas quand les barres se rétractent. Le bouton reste donc
  immobile quel que soit leur état, et reste visible dans tous les cas
  puisqu'il tient dans la plus petite vue. La déclaration `bottom` est laissée
  avant, en repli : un navigateur qui ignore `svh` — Safari d'avant 15.4 —
  écarte le `top` et retrouve l'ancien comportement ; quand les deux sont
  comprises, c'est `top` qui l'emporte, la hauteur étant fixée.

  Le disque est en outre promu sur sa propre couche par une transformation en
  trois dimensions nulle. WebKit ne repositionne pas les éléments fixes en
  continu pendant l'inertie du défilement : ils dérivent avec le texte, puis
  reviennent d'un coup. C'est le remède usuel, et il ne coûte rien pour un
  disque de 42 px.

* **Le bouton passe sous les volets** (`z-index: 12`). Sur écran étroit, la
  table des matières se déploie par-dessus la page avec un voile ; le
  bouton n'a rien à dire tant qu'elle est ouverte.

### La croix qui vide le champ de recherche

**Première tentative, et pourquoi elle ne pouvait pas aboutir.** La croix
avait d'abord été redemandée au navigateur, en redonnant au pseudo-élément
`::-webkit-search-cancel-button` son apparence propre — WebKit abandonnant le
rendu natif d'un contrôle dès qu'on lui pose une bordure et un fond, ce que
font les trois livres. Sur iPhone, rien n'a paru, et **rien ne pouvait
paraître** : WebKit ne rend ce pseudo-élément que sur macOS. Sur iOS il
n'existe pas ; le champ de recherche y est un champ de texte ordinaire, et
l'usage veut qu'on le vide au clavier. Aucune CSS n'y changera quoi que ce
soit.

Il faut donc **dessiner la croix nous-mêmes**. Elle est posée par
`pordo.js`, compagnon de `pordo.css` et servi de la même racine : chaque
livre n'en porte qu'une ligne de plus. La croix native est du même coup
écartée — macOS la dessinait, et il y en aurait eu deux. Mesuré dans
Chromium : règle annulée, deux croix ; règle active, une seule.

`color-scheme: light dark` reste. Il ne sert plus la croix, mais il accorde
au thème sombre des trois livres les barres de défilement et le menu de choix
de langue, ce qu'il faisait déjà.

**Rien ne casse si le script ne se charge pas.** Sans lui, les trois champs
sont exactement ce qu'ils étaient : on vide au clavier, comme avant.

#### L'enveloppe, et le seul vrai piège

La croix se pose en absolu ; il lui faut donc un parent positionné qui épouse
le champ. Les *Tabeli* en ont déjà un — l'enveloppe de leur loupe —, et le
script s'en sert tel quel plutôt que d'en empiler un second. Il le reconnaît
à deux conditions, nécessaires toutes les deux : le parent est déjà
positionné, et le champ est son **seul enfant dans le flux** (une icône posée
en absolu ne compte pas). La barre des deux autres livres échoue aux deux —
elle est statique, et porte le bouton du sommaire ; ils reçoivent donc une
enveloppe.

Et là est le piège. Une enveloppe s'interpose entre la barre et le champ :
c'est elle, désormais, que la barre range. Les mesures qui décident de la
place du champ doivent donc passer de l'un à l'autre. Ce n'est pas une
précaution de principe :

```css
/* gramatiko, sous 900 px */
input[type=search]{flex:1 1 120px;min-width:0}
```

L'auteur dit pourquoi en toutes lettres — à 260 px de base, le champ
passerait sous le bouton du sommaire. Une enveloppe qui prendrait sa base de
son contenu mesurerait plus large, et le champ repasserait à la ligne. C'est
exactement ce qui arrivait, à 340 px de vue.

**Les mesures sont donc relues, et non recopiées une fois.** Elles changent
avec la largeur de l'écran, chaque livre ayant les siennes ; une copie prise
au chargement serait fausse dès la première rotation du téléphone. À chaque
changement réel de la vue, le script efface ses surcharges, relit ce que le
livre dit du champ *à cette largeur*, et repose. Vérifié en comparant la
boîte du champ, avant et après, à dix-huit largeurs de 1280 à 300 px sur les
trois livres : identique partout, aux deux centièmes de pixel.

Sur le reste de l'en-tête, à champ vide : aucune différence sur les *Tabeli*,
qui n'ont pas d'enveloppe ; quinze à vingt-cinq pixels sur les deux autres,
d'une amplitude maximale de 2 sur 255, tous sur le bord arrondi du champ.
C'est du crénelage, non un déplacement.

#### Quelques choix qui ne se devinent pas

* **Elle ne paraît que si le champ porte quelque chose**, et le retrait de
  34 px qui lui fait place arrive avec elle. Un champ vide n'a rien à vider,
  et la croix mangerait la place du texte d'invite — déjà coupé sur un
  téléphone. Le retrait arrive avec la première lettre frappée : à ce moment
  le texte d'invite a disparu et le champ ne porte qu'un caractère, de sorte
  que rien ne se déplace sous l'œil.

* **La pression du doigt ne doit pas faire fuir le clavier.** Une pression
  sur un bouton retire le curseur du champ, et sur iPhone le clavier se
  replie aussitôt pour se rouvrir juste après : la page saute deux fois.
  Refuser l'effet par défaut de la pression laisse le curseur où il est, et
  le clic suit tout de même.

* **Le curseur n'est rendu au champ que s'il y était.** Vider depuis une page
  déjà parcourue — le clavier replié, un résultat sous les yeux — ne doit pas
  faire remonter le clavier par-dessus ce qu'on lisait.

* **L'événement `input` est émis à la main.** Les trois livres filtrent
  dessus, et affecter `value` directement n'en émet aucun : sans cela le
  champ serait vide et la liste toujours filtrée.

* **La croix n'est pas une halte de tabulation**, comme la croix native de
  macOS. Elle s'insère entre le champ et la commande suivante ; en faire un
  arrêt en ajouterait un là où il n'y en avait pas, pour un service que le
  clavier rend déjà. Les lecteurs d'écran l'atteignent néanmoins, le bouton
  restant dans le document et nommé — « Efacar la sercho », en ido comme le
  reste des trois interfaces.

* **La zone tactile fait 34 px sur toute la hauteur du champ**, pour un trait
  de 15 px : un doigt ne vise pas un trait.

Cette section est la raison pour laquelle `pordo.css` n'est plus seulement le
bouton de retour, mais **la feuille commune** : ce qui doit être uniforme sur
les trois livres et ne peut pas l'être autrement y a désormais sa place —
l'apparence dans la feuille, le peu de conduite qu'il faut dans `pordo.js`,
à côté.

---

## 9. Hors-ligne, et le nom de l'application

### Le nom

Le titre de l'onglet reste **« Ido — helpolinguo internaciona »**. Sous une
icône, un nom dispose de deux mots au plus : le manifeste et la balise
d'Apple donnent donc **« Ido »** seul.

```html
<link rel="manifest" href="manifest.webmanifest">
<meta name="apple-mobile-web-app-title" content="Ido">
```

`manifest.webmanifest` porte aussi `short_name`, les icônes (`ikono-192.png`,
`ikono-512.png`, refaites par `outils/ikoni.py`) et trois raccourcis vers les
livres.

**La couleur de la barre de fenêtre.** Le navigateur retient **le premier**
`theme-color` dont le `media` correspond. L'inconditionnel était en tête : il
correspondait toujours, et celui du thème sombre n'était jamais atteint — d'où
une barre blanche en mode sombre dans l'application du Dock, alors que les
trois livres suivaient le thème, n'en déclarant aucun et laissant Safari
déduire la couleur du fond réellement peint.

Les deux portent donc leur condition, et **la claire vient en premier** : un
navigateur qui ignorerait l'attribut `media` prendrait la première, et le
clair est le parti par défaut de la page.

```html
<meta name="theme-color" media="(prefers-color-scheme:light)" content="#fbfaf7">
<meta name="theme-color" media="(prefers-color-scheme:dark)"  content="#16161a">
```

Le manifeste **ne déclare plus de `theme_color`** : c'était une seconde source,
statique et claire, qui n'aurait pas su suivre le thème. Sans elle, il ne reste
que les deux balises — et si un navigateur les ignorait, il ferait comme pour
les trois livres, qui n'en ont pas et vont bien. `:root` déclare en outre
`color-scheme: light dark`, pour que le navigateur accorde ses propres
surfaces.

> **Un choix qui mérite d'être su.** Le manifeste déclare
> `"display": "standalone"`, et la balise `apple-mobile-web-app-capable`
> l'accompagne pour les iOS antérieurs à 16.4 : l'application enregistrée
> s'ouvre donc **sans l'habillage de Safari**. C'est ce que « web-app »
> suppose, mais c'est un changement visible. Un seul mot à changer pour
> revenir en arrière.

### Le hors-ligne

`sw.js`, posé à la racine, a pour **portée tout le site** : la porte et les
trois livres, qui sont servis sous la même origine. Les trois dépôts n'ont
donc rien à porter — ils sont pris en charge dès que la page d'accueil a été
ouverte une fois. C'est le même bénéfice que pour `pordo.css` (§ 8).

**La fraîcheur passe avant la vitesse**, puisque les textes sont corrigés
souvent :

| ce qui est demandé | comment | pourquoi |
|---|---|---|
| une **page** | réseau d'abord, copie en secours | en ligne, on lit toujours la dernière version |
| **le reste** — feuille, polices, images, PDF | copie d'abord, revalidation derrière | ces fichiers changent rarement, l'attente ne se justifierait pas |

Les requêtes au réseau portent `cache: 'reload'` : sans cela, le cache HTTP
du navigateur rendrait une copie vieille de dix minutes — c'est la durée que
GitHub Pages annonce.

**Au retour de la connexion**, la page prévient le servanto, qui reprend au
réseau *tout ce qu'il détient*. C'est ce qui répond au « dès que possible ».

### Le téléchargement complet

Le site entier — les trois textes, les PDF, les 52 langues et les 38 planches
gravées dans leurs **deux** résolutions — pèse **69 Mo**, soit 106 fichiers.

* **Installée**, l'application le prend d'elle-même, quatre secondes après
  l'ouverture. C'est ce qu'on attend d'une application, et c'est le moment le
  plus proche de l'ajout à l'écran d'accueil qu'un site puisse observer : iOS
  n'annonce pas cet ajout, contrairement à Android.
* **Dans un onglet**, rien n'est pris sans qu'on le demande : un visiteur de
  passage n'a pas à payer 69 Mo. Un disque dans le coin inférieur gauche le
  propose.

**Le disque n'a aucun mot**, et c'est délibéré : le site s'adresse à toutes
les langues, et « Deskargar » ne disait rien à qui ne lit pas l'ido. Il occupe
sur la porte la place que le bouton de retour occupe sur les trois livres —
même coin, même taille, même écart —, de sorte que le coin porte toujours
« l'action globale » : le retour quand on lit, le téléchargement quand on est
à la porte.

| état | signe | anneau |
|---|---|---|
| au repos | une flèche vers le bas | vide |
| pendant | la flèche | il fait le tour à mesure |
| terminé | un crochet | plein, azur |
| armé pour l'effacement | une corbeille | plein, terre de Sienne |

Le compte des méga-octets paraît à droite du disque pendant la prise, et
seulement là : « 18 MB » se lit partout, ce qu'une phrase ne fait pas. Il dit
ce qui est **descendu**, sans dénominateur — c'est l'anneau qui dit la part
faite, et un total annoncé d'avance reposerait sur une estimation, les
fichiers non versionnés n'annonçant pas leur taille.

**Un clic sur l'état « terminé » n'efface pas** : il arme. Le signe devient
une corbeille pendant quatre secondes, et il faut cliquer une seconde fois.
Effacer 69 Mo par mégarde serait pénible, et une confirmation en toutes
lettres reviendrait à remettre du texte. L'effacement garde la coquille : sans
elle, on ne pourrait plus redemander le téléchargement hors ligne.

Le nom accessible, lui, reste en ido et suit l'état — les lecteurs d'écran
ont besoin de mots, pas les yeux.

L'état affiché n'est pas un marqueur posé après coup : le servanto compte
réellement ce qu'il détient du plan. Si le navigateur vidait le cache, le
bouton se reproposerait de lui-même.

**Le poids se connaît sans une seule requête**, parce que le `?v=` de chaque
adresse **est** la taille du fichier en octets — vérifié sur les 90 adresses
versionnées. Le plan lui-même est lu dans la page des *Tabeli*, jamais écrit
en dur.

**Un repli pour la loupe.** Les planches existent en « vido » (200 ko) et en
« detalo » (1,8 Mo). Si la grande manque hors ligne — téléchargement
interrompu, cache partiel —, le servanto sert la petite : une loupe floue,
mais une image, au lieu d'un cadre vide.

### Et sur Android ?

Oui, et mieux qu'ailleurs. Service worker, cache et manifeste sont ceux du
standard ; Chrome sur Android sait en outre proposer l'installation
(`beforeinstallprompt`), annonce l'installation faite (`appinstalled`), et
honore `navigator.storage.persist()`, qui écarte l'effacement automatique
quand la place manque. Le test `(display-mode: standalone)` qui déclenche le
téléchargement automatique vaut sur les deux systèmes.

Sur iOS, la persistance est accordée d'office aux applications de l'écran
d'accueil ; c'est dans un simple onglet Safari que le cache peut être effacé
après sept jours sans visite.

### Ce qui est pris, et quand

| | poids | quand |
|---|---|---|
| la coquille — porte, feuille, script, polices, icônes | 0,09 Mo | à l'installation, pour tout visiteur |
| les trois textes et les quatre PDF | ≈ 12 Mo | **seulement en application installée**, quatre secondes après l'ouverture |
| les 52 langues des *Tabeli* | 24,5 Mo | à la suite, dans l'ordre où la page les cite |
| les 38 planches gravées, deux résolutions | 32 Mo | avec le reste |

Soit **69 Mo**, chiffre que le disque affiche à la fin et que
`navigator.storage.estimate()` confirme.

**Pourquoi les langues.** La page des *Tabeli* est bilingue : l'ido à gauche,
une autre langue à droite. Cette autre langue n'est pas dans la page — elle
est prise au moment où on la choisit, un fichier par langue. Hors ligne, une
langue jamais ouverte manquait donc, et le sélecteur restait sans effet.

**La liste n'est pas écrite dans `sw.js`.** Elle est lue dans la page
elle-même, déjà en cache : une liste recopiée vieillirait au premier
changement d'adresse. Les langues sont prises dans l'ordre où la page les
cite, de sorte qu'une prise interrompue couvre d'abord les plus courantes.

**Les adresses versionnées sont immuables.** Langues et planches portent
toutes un `?v=` : une correction en change l'adresse, et la page — toujours
prise au réseau — cite la nouvelle. Deux conséquences : on ne les revalide
jamais au retour de la connexion, ce qui éviterait de reprendre 24 Mo pour
rien ; et on purge celles que la page ne cite plus, sans quoi les anciennes
resteraient indéfiniment.

### Deux points de sûreté

* **`addAll` n'est pas employé.** Il est atomique : un seul fichier manquant,
  ou une seule requête qui échoue, et rien n'est mis en cache — la coquille
  entière perdue pour un détail. Chaque fichier est pris séparément.
* **Un déploiement fautif ne peut pas rester coincé**, puisque les pages sont
  prises au réseau d'abord. Et pour tout purger : changer `VERSIO` en tête de
  `sw.js` ; l'ancien cache est effacé à l'activation.

### Vérifié dans Chromium

Servi localement dans l'arborescence réelle, avec coupure du réseau :

* la coquille est prise à l'installation — 10 entrées ; le corps sur demande —
  7 entrées, soit 16 en tout ;
* **hors ligne**, la porte, les trois livres et les PDF répondent tous, sans
  qu'aucun livre ait été ouvert au préalable ;
* une correction publiée est visible **au rechargement suivant** tant qu'on
  est en ligne, et se retrouve ensuite hors ligne ;
* une correction publiée *pendant* une coupure est reprise **une demi-seconde
  après** le retour du réseau ;
* les 52 langues sont prises, et **hors ligne le sélecteur fonctionne** — le
  français, l'allemand et le japonais remplissent leurs 672 blocs sans que
  les *Tabeli* aient été ouvertes auparavant ;
* une entrée versionnée devenue périmée est **purgée** au passage suivant ;
* le téléchargement complet mène les **106 fichiers** à leur terme, et
  **hors ligne les 106 répondent, 0 en échec**, pour 69 Mo restitués ;
* les planches paraissent hors ligne sans que les *Tabeli* aient été ouvertes ;
* la grande résolution supprimée, la demande hors ligne reçoit la petite —
  218 ko au lieu de 1,8 Mo ;
* l'état est reconnu au rechargement : le bouton dit « Senrete disponebla » ;
* le disque passe par ses quatre états, s'arme, se désarme seul au bout de
  quatre secondes, et l'effacement ne laisse que les 9 fichiers de la
  coquille ;
* aucun mot du ciel ne tombe sous le disque, aux six formats essayés et sur
  six mesures espacées — la réserve tient compte de la dérive des mots, qui
  vaut treize pixels au plus ;
* l'entrée, le clic sur l'étoile et l'absence de défilement sont intacts.

---

## 10. Le site, pour les machines

Le site s'adresse d'abord à l'œil. Cette section-ci décrit ce qui a été
ajouté pour ce qui n'a pas d'yeux : les moteurs de recherche, les
aspirateurs, et les modèles de langue qui vont chercher une adresse.

### Le vrai problème n'était pas le poids

On croit d'abord que la difficulté est le nombre de jetons. Mesuré, elle
était ailleurs :

| page | poids | texte visible sans JavaScript |
| --- | ---: | ---: |
| `/dicionario/` | 2,1 Mo | **213 caractères** |
| `/tabeli/` | 3,3 Mo | 257 Ko |
| `/gramatiko/` | 1,2 Mo | 467 Ko |

Le Dicionario est bâti par du JavaScript : ses 9473 articles vivent dans
un tableau que le navigateur déroule au chargement. Excellent pour la
recherche instantanée, désastreux pour tout ce qui n'exécute pas de
script. La page ne rend d'ailleurs que 400 articles à la fois, même avec
JavaScript. Un robot d'indexation sans moteur JS n'y voyait rien, et rien
ne le lui disait.

### Les fichiers engendrés

Chaque livre porte désormais un `outils/robotoj.py` qui tire de sa page
des versions lisibles par les machines. **Ils sont engendrés, jamais
édités à la main** ; la source reste `index.html`.

| livre | fichiers | contenu |
| --- | --- | --- |
| Dicionario | `dicionario.json` | les 9473 articles, données nues |
| | `dicionario.md` | le livre à plat |
| | `vortlisto.md` | vedette et premier sens seulement |
| Gramatiko | `chapitri/*.md` | **un fichier par chapitre**, ~10 Ko |
| | `chapitri/index.md` | la table, avec la taille de chacun |
| | `gramatiko.md` | le livre entier |
| Tabeli | `tabeli.json` | les 672 clés, ido et français |
| | `tabeli.md` | le tableau à plat |
| | `lingui/index.json` | les 55 autres langues offertes |

### Le découpage vaut mieux que la compression

C'est le point à retenir. Une grammaire ne se lit pas d'un bout à
l'autre : on y cherche un point. Qui veut savoir comment se forme le
pluriel n'a pas à charger 1,2 Mo — il charge un chapitre de 10 Ko. Le
gain n'est pas de quelques pourcents, il est de deux ordres de grandeur,
et il ne doit rien à une quelconque compression : il tient à ce que le
texte soit **découpé et étiqueté**, et à ce que les tailles soient
annoncées d'avance pour qu'on puisse choisir avant de télécharger.

### La charnière des Tabeli

Les clés des rangées (`data-cle`) sont exactement celles des fichiers
`lingui/*.json`. Publier les paires ido/français sous ces mêmes clés rend
donc tout le corpus des 57 langues joignable par programme : qui veut le
couple ido-japonais joint `tabeli.json` et `lingui/ja.json` sur la clé,
sans ouvrir la page ni exécuter son JavaScript. Les 672 clés
correspondent à 100 %.

### À la racine, et pourquoi seulement là

`robots.txt` et `sitemap.xml` ne sont lus qu'à la RACINE d'un domaine :
déposés dans `/tabeli/`, personne ne les lirait. Comme la feuille commune
et le service worker, ils ne peuvent vivre qu'ici, et ils parlent pour
les quatre pages. `outils/robotoj.py` les engendre — il lit les dépôts
voisins, et doit donc être relancé quand un livre change.

* **`robots.txt`** dit oui à tout le monde, et nomme un à un les robots
  des modèles de langue. Ce n'est pas de la redondance avec l'étoile :
  plusieurs cherchent leur propre nom avant la règle générale, et
  certains exploitants s'abstiennent quand rien ne les vise.
* **`sitemap.xml`** énumère les pages ET les fichiers engendrés. Sans
  cela un moteur ne les trouverait que par le lien de la page, et un
  aspirateur pas du tout.
* **`llms.txt`** est la carte : ce que le site contient, sous quelle
  forme, et à quel poids. C'est la dernière colonne qui compte.

### Ce que porte chaque page

Une description, un lien canonique — le site répond aussi sous
`gphmorin.github.io`, et sans cette ligne un moteur peut tenir les deux
pour deux sites —, un lien `alternate` vers la version Markdown, et un
bloc JSON-LD qui dit ce que le document EST : un livre, son auteur, sa
date, sa langue.

Le Dicionario porte en plus un `<noscript>` qui ne tente pas de rendre le
dictionnaire en HTML, mais indique où il est. Sans JavaScript, la page
offrait 213 caractères et aucune issue ; elle en offre 465 et trois
chemins vers le texte.

**Aucune mention de licence n'a été inscrite.** Les données structurées
pourraient porter un champ `license`, et il a été délibérément laissé
vide : les trois œuvres n'ont pas le même statut — 1925 et 1926 d'un
côté, une seconde édition de 1964 de l'autre — et cette décision-là
revient à l'auteur du site, non à son outillage.

## 11. Refabriquer les images

```sh
python3 outils/emblemo.py   # le logotype, à recopier dans index.html
python3 outils/ikoni.py     # emblemo.svg, apple-touch-icon.png, og-imajo.png
```

Les deux scripts lisent `Jost-Bold.ttf` et `Jost-Medium.ttf` dans
`dicionario/posho/polices/` ; ils demandent `fonttools` et `pymupdf`.

Jost\* est sous licence SIL OFL 1.1 — voir `polices/OFL.txt` et
`polices/LISEZ-MOI.md`.
