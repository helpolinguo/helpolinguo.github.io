# Jost\*

Les deux coupes de la couverture du *Dicionario*, **réduites aux seuls signes
de la page d'accueil** : 5,7 ko chacune au format WOFF 2, contre 59 ko pour
les TTF complètes.

| fichier | usage |
|---|---|
| `Jost-Bold.woff2` | les lettres **ID** du logotype (converties en courbes dans `index.html`, la fonte ne sert que de secours) |
| `Jost-Medium.woff2` | la devise et les trois boutons |

Elles sont produites à partir de `dicionario/posho/polices/*.ttf` :

```sh
pyftsubset Jost-Medium.ttf --flavor=woff2 --layout-features=kern,liga \
  --text="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 …" \
  --output-file=polices/Jost-Medium.woff2
```

Jost\* est la reprise libre de la **Futura** de Paul Renner, dessinée par
*indestructible type\**, sous licence **SIL Open Font License 1.1** — texte
complet dans `OFL.txt`. Elle permet la redistribution avec le document, à la
condition — remplie ici — que la licence accompagne les fichiers.

Version : Jost\* v20, telle que servie par Google Fonts.
