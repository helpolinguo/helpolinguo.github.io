# Jost\*

The two cuts from the *Dicionario*'s cover, **subset to the glyphs the home
page uses**: 5.7 kB each as WOFF 2, against 59 kB for the full TTFs.

| file | use |
|---|---|
| `Jost-Bold.woff2` | the letters **ID** of the logotype (converted to outlines in `index.html`; the font is only a fallback) |
| `Jost-Medium.woff2` | the motto and the three buttons |

They are produced from `dicionario/pocket/fonts/*.ttf`:

```sh
pyftsubset Jost-Medium.ttf --flavor=woff2 --layout-features=kern,liga \
  --text="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 …" \
  --output-file=fonts/Jost-Medium.woff2
```

Jost\* is the free revival of Paul Renner's **Futura**, drawn by
*indestructible type\**, under the **SIL Open Font License 1.1** — full text
in `OFL.txt`. It permits redistribution with the document, on the condition —
met here — that the licence accompanies the files.

Version: Jost\* v20, as served by Google Fonts.
