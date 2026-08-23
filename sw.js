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
  const k = await c.match(req);
  const reseau = fetch(req)
    .then(r => { if (r && r.ok) c.put(req, r.clone()); return r; })
    .catch(() => null);
  return k || (await reseau) || Response.error();
}

self.addEventListener('message', e => {
  if (e.data === 'korpuso')  e.waitUntil(prenKorpuson());
  if (e.data === 'refresho') e.waitUntil(refreshigi());
});

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
}

/* Au retour de la connexion : tout ce qui est détenu est repris au réseau.
   Rien n'est ajouté — on ne fait que rafraîchir ce qu'on a déjà. */
async function refreshigi() {
  const c = await caches.open(VERSIO);
  for (const req of await c.keys()) {
    try { const r = await fetch(freshe(req.url)); if (r && r.ok) await c.put(req, r.clone()); }
    catch (_) { break; /* la connexion est repartie : inutile d'insister */ }
  }
}
