/* =====================================================================
   LE SERVANTO — hors-ligne pour les quatre pages
   =====================================================================

   POURQUOI UN SEUL FICHIER SUFFIT. Le servanto est posé à la racine, il a
   donc pour PORTÉE tout le site : la page d'accueil et les trois livres,
   qui sont des sites de projet servis sous la même origine. Les trois
   dépôts n'ont rien à porter — ils sont pris en charge dès que la page
   d'accueil a été ouverte une fois, et le restent.

   LA FRAÎCHEUR PASSE AVANT LA VITESSE, parce que les textes sont corrigés
   souvent. Deux règles :

     * les PAGES sont prises au réseau d'abord, et la copie ne sert que
       si le réseau manque. En ligne, on lit donc toujours la dernière
       version — jamais celle de la veille ;
     * le RESTE — feuille, polices, images, PDF — est servi de la copie
       puis revalidé en arrière-plan. Ces fichiers changent rarement, et
       l'attente ne se justifierait pas.

   Les requêtes au réseau portent « cache: reload » : sans cela, le cache
   HTTP du navigateur pourrait rendre une copie vieille de dix minutes —
   c'est la durée que GitHub Pages annonce.

   AU RETOUR DE LA CONNEXION, la page prévient le servanto, qui revalide
   tout ce qu'il détient. C'est ce qui répond au « dès que possible ».

   POUR TOUT PURGER : changer VERSIO. L'ancien cache est effacé à
   l'activation, et tout est repris au réseau.
   ===================================================================== */

const VERSIO = 'ido-1';

/* La coquille : quelques dizaines de kilo-octets, prise à l'installation
   par tout visiteur. */
const SHELO = [
  '/', '/pordo.css', '/emblemo.svg', '/manifest.webmanifest',
  '/apple-touch-icon.png', '/ikono-192.png', '/ikono-512.png',
  '/polices/Jost-Medium.woff2', '/polices/Jost-Bold.woff2'
];

/* Le corps des trois livres — environ douze méga-octets. Il n'est PAS pris
   à l'installation : un visiteur qui ne fait que passer par la porte n'a
   pas à payer ce prix. La page ne le demande que si elle tourne comme
   application installée. Les planches gravées, elles, se mettent en cache
   à la lecture, dans la résolution que l'appareil aura choisie — les
   prendre d'avance dans les deux résolutions coûterait 32 Mo pour rien. */
const KORPUSO = [
  '/tabeli/', '/dicionario/', '/gramatiko/',
  '/tabeli/tabeli.pdf', '/tabeli/tableaux.pdf',
  '/dicionario/dicionario.pdf', '/gramatiko/gramatiko.pdf'
];

const freshe = u => new Request(u, { cache: 'reload', credentials: 'same-origin' });

/* UN FICHIER À LA FOIS, ET NON « addAll ». « addAll » est atomique : un
   seul fichier manquant, ou une seule requête qui échoue, et RIEN n'est
   mis en cache — la coquille entière est perdue pour un détail. Chaque
   fichier est donc pris séparément, et un échec n'emporte que lui. */
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(VERSIO)
      .then(c => Promise.all(SHELO.map(u => c.add(freshe(u)).catch(() => null))))
      .then(() => self.skipWaiting())
      .catch(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(nomi => Promise.all(nomi.filter(n => n !== VERSIO).map(n => caches.delete(n))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  if (new URL(req.url).origin !== location.origin) return;
  e.respondWith(req.mode === 'navigate' ? reto(req) : kopio(req));
});

/* Réseau d'abord : la page lue est toujours la dernière publiée. */
async function reto(req) {
  const c = await caches.open(VERSIO);
  try {
    const r = await fetch(freshe(req.url));
    if (r && r.ok) c.put(req.url, r.clone());
    return r;
  } catch (_) {
    return (await c.match(req.url)) || (await c.match('/')) || Response.error();
  }
}

/* Copie d'abord, revalidation derrière. */
async function kopio(req) {
  const c = await caches.open(VERSIO);
  let k = await c.match(req);

  /* LE REPLI DE LA LOUPE. Les planches gravées existent en deux
     résolutions : « vido » pour l'écran, « detalo » pour la loupe, sept
     fois plus lourde. Si la grande manque hors ligne, servir la petite
     donne une loupe floue — mais une image, au lieu d'un cadre vide.
     « ignoreSearch » retrouve la petite quelle que soit sa version. */
  if (!k && req.url.includes('-detalo.webp')) {
    k = await c.match(req.url.split('?')[0].replace('-detalo.webp', '-vido.webp'),
                      { ignoreSearch: true });
    if (k) return k;
  }
  const reseau = fetch(req)
    .then(r => { if (r && r.ok) c.put(req, r.clone()); return r; })
    .catch(() => null);
  return k || (await reseau) || Response.error();
}

self.addEventListener('message', e => {
  if (e.data === 'korpuso')  e.waitUntil(prenKorpuson());
  if (e.data === 'refresho') e.waitUntil(refreshigi());
  if (e.data === 'tuto')     e.waitUntil(deskargi());
  if (e.data === 'stato')    e.waitUntil(diriStaton());
});

async function sciigi(msg) {
  for (const kl of await self.clients.matchAll({ includeUncontrolled: true })) kl.postMessage(msg);
}

/* --- LE PLAN COMPLET -------------------------------------------------
   Tout ce que le site sert : la coquille, les trois textes, les PDF, les
   52 langues et les 38 planches — les deux résolutions comprises.

   Les adresses versionnées sont LUES DANS LA PAGE des Tabeli, comme pour
   les langues (voir akordigiTabelin) : rien n'est écrit en dur, donc rien
   ne peut vieillir. Et comme le « ?v= » de chaque adresse EST la taille du
   fichier en octets — vérifié sur les 90 —, le poids total se connaît
   sans une seule requête. */
async function planoTuta(c) {
  const listo = [...SHELO, ...KORPUSO];
  if (!(await c.match('/tabeli/'))) {
    try {
      const r = await fetch(freshe('/tabeli/'));
      if (r && r.ok) await c.put('/tabeli/', r.clone());
    } catch (_) { return listo; }
  }
  const enhavo = await c.match('/tabeli/');
  if (enhavo) {
    const teksto = await enhavo.text();
    const bazo = new URL('/tabeli/', location).href;
    const trovi = teksto.match(/(?:lingui|gravuri)\/[A-Za-z0-9._-]+\.(?:json|webp)\?v=\d+/g) || [];
    for (const u of new Set(trovi)) listo.push(bazo + u);
  }
  return [...new Set(listo)];
}

/* Le poids annoncé par les adresses elles-mêmes, en octets. Les fichiers
   non versionnés — coquille, textes, PDF — n'annoncent rien : ils sont
   comptés à la pesée, quand ils arrivent. */
const pezoAnoncita = u => {
  const m = u.match(/\?v=(\d+)$/);
  return m ? +m[1] : 0;
};

async function deskargi() {
  const c = await caches.open(VERSIO);
  const listo = await planoTuta(c);
  let faritaj = 0, oktetoj = 0;
  const anoncita = listo.reduce((s, u) => s + pezoAnoncita(u), 0);
  await sciigi({ tipo: 'progreso', faritaj, totalaj: listo.length, oktetoj, anoncita });

  for (const u of listo) {
    if (!(await c.match(u))) {
      try {
        const r = await fetch(freshe(u));
        if (r && r.ok) { const kopio = r.clone(); await c.put(u, r); oktetoj += (await kopio.blob()).size; }
      } catch (_) {
        await sciigi({ tipo: 'rompita', faritaj, totalaj: listo.length, oktetoj });
        return;
      }
    } else {
      oktetoj += pezoAnoncita(u);
    }
    faritaj++;
    if (faritaj % 2 === 0 || faritaj === listo.length) {
      await sciigi({ tipo: 'progreso', faritaj, totalaj: listo.length, oktetoj, anoncita });
    }
  }
  await sciigi({ tipo: 'preta', totalaj: listo.length, oktetoj });
}

/* L'état vrai : combien du plan est réellement détenu. On ne pose pas de
   marqueur — un marqueur mentirait si le navigateur vidait le cache. */
async function diriStaton() {
  const c = await caches.open(VERSIO);
  if (!(await c.match('/tabeli/'))) return sciigi({ tipo: 'stato', faritaj: 0, totalaj: 0 });
  const listo = await planoTuta(c);
  let faritaj = 0;
  for (const u of listo) if (await c.match(u)) faritaj++;
  await sciigi({ tipo: 'stato', faritaj, totalaj: listo.length });
}

/* Le corps des livres, un fichier à la fois : douze méga-octets d'un coup
   sur un réseau lent bloqueraient tout le reste. Un échec n'arrête rien —
   ce qui manque sera pris à la prochaine occasion. */
async function prenKorpuson() {
  const c = await caches.open(VERSIO);
  for (const u of KORPUSO) {
    if (await c.match(u)) continue;
    try { const r = await fetch(freshe(u)); if (r && r.ok) await c.put(u, r.clone()); }
    catch (_) { /* on continue */ }
  }
  await akordigiTabelin(c);
}

/* --- LES LANGUES DES TABELI ------------------------------------------
   La page de lecture est bilingue : l'ido à gauche, une autre langue à
   droite. Cette autre langue n'est PAS dans la page — elle est prise au
   moment où on la choisit, un fichier par langue, cinquante-deux en tout
   pour 24,5 Mo. Hors ligne, une langue jamais ouverte manquait donc, et
   le sélecteur restait sans effet.

   LA LISTE N'EST PAS ECRITE ICI. Elle est LUE DANS LA PAGE elle-même,
   déjà en cache : une liste recopiée dans ce fichier vieillirait au
   premier changement d'adresse. Les langues sont prises dans l'ordre où
   la page les cite, de sorte qu'une prise interrompue couvre d'abord les
   plus courantes.

   AU PASSAGE, ON PURGE. Toutes ces adresses portent un « ?v= » : elles
   sont donc immuables, et une correction en change l'adresse. L'ancienne
   resterait en cache indéfiniment si on ne retirait pas ce que la page
   ne cite plus. */
async function akordigiTabelin(c) {
  const enhavo = await c.match('/tabeli/');
  if (!enhavo) return;
  const teksto = await enhavo.text();
  const bazo = new URL('/tabeli/', location).href;
  const citita = new Set(
    (teksto.match(/(?:lingui|gravuri)\/[A-Za-z0-9._-]+\.(?:json|webp)\?v=\d+/g) || [])
      .map(u => bazo + u)
  );
  if (!citita.size) return;

  for (const req of await c.keys()) {
    if (req.url.startsWith(bazo) && req.url.includes('?v=') && !citita.has(req.url)) {
      await c.delete(req);
    }
  }
  for (const u of citita) {
    if (!u.includes('/lingui/')) continue;   /* les planches se prennent à la lecture */
    if (await c.match(u)) continue;
    try { const r = await fetch(freshe(u)); if (r && r.ok) await c.put(u, r.clone()); }
    catch (_) { break; }                     /* la connexion est repartie */
  }
}

/* Au retour de la connexion : tout ce qui est détenu est repris au réseau.
   Rien n'est ajouté — on ne fait que rafraîchir ce qu'on a déjà. */
async function refreshigi() {
  const c = await caches.open(VERSIO);
  for (const req of await c.keys()) {
    /* Les adresses versionnées sont immuables : une correction en change
       l'adresse, et la page — toujours prise au réseau — cite la nouvelle.
       Les revalider serait reprendre 24 Mo pour rien à chaque retour de
       connexion. Elles sont purgées ailleurs, quand la page ne les cite
       plus (voir akordigiTabelin). */
    if (req.url.includes('?v=')) continue;
    try { const r = await fetch(freshe(req.url)); if (r && r.ok) await c.put(req, r.clone()); }
    catch (_) { break; /* la connexion est repartie : inutile d'insister */ }
  }
  await akordigiTabelin(c);
}
