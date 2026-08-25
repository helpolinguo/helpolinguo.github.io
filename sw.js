/* =====================================================================
   THE SERVICE WORKER — offline, for all four pages
   =====================================================================

   WHY ONE FILE IS ENOUGH. The worker sits at the root, so its SCOPE is the
   whole site: the home page and the three books, which are project sites
   served from the same origin. The three repositories carry nothing — they
   are taken care of as soon as the home page has been opened once, and
   they stay so.

   FRESHNESS COMES BEFORE SPEED, because the texts are corrected often. Two
   rules:

     * PAGES are fetched from the network first, and the cached copy serves
       only if the network is missing. Online, one therefore always reads
       the latest version — never yesterday's;
     * EVERYTHING ELSE — stylesheet, fonts, images, PDFs — is served from
       the copy and revalidated in the background. These files change
       rarely, and the wait would not be justified.

   Network requests carry "cache: reload": without it the browser's HTTP
   cache could hand back a copy ten minutes old — the lifetime GitHub Pages
   announces.

   WHEN THE CONNECTION RETURNS, the page tells the worker, which
   revalidates everything it holds. That is what answers "as soon as
   possible".

   TO PURGE EVERYTHING: change CACHE. The old cache is deleted on
   activation, and everything is fetched afresh.

   NOTE ON THE 2026 RENAMING. Several shell files were renamed when the
   source was put in order for release (/pordo.css became /shared.css,
   /emblemo.svg became /emblem.svg, and so on). CACHE was deliberately NOT
   bumped for it: a reader who had taken the whole site offline — some
   sixty megabytes — would have lost it all and had to fetch it again. The
   handful of stale entries left behind are harmless, and CLEAR sweeps
   them, since it keeps only what is in SHELL.
   ===================================================================== */

const CACHE = 'ido-2';

/* The shell: a few tens of kilobytes, fetched at install by every
   visitor. */
const SHELL = [
  '/', '/shared.css', '/shared.js', '/emblem.svg', '/manifest.webmanifest',
  '/apple-touch-icon.png', '/icon-192.png', '/icon-512.png',
  '/fonts/Jost-Medium.woff2', '/fonts/Jost-Bold.woff2'
];

/* The body of the three books — about twelve megabytes. It is NOT fetched
   at install: a visitor who merely passes through the door should not pay
   that price. The page asks for it only if it is running as an installed
   application. The engraved plates, for their part, are cached as they are
   read, in whichever resolution the device has chosen — fetching both
   resolutions in advance would cost 32 MB for nothing. */
const BOOKS = [
  '/tabeli/', '/dicionario/', '/gramatiko/',
  '/tabeli/tabeli.pdf', '/tabeli/tableaux.pdf',
  '/dicionario/dicionario.pdf', '/gramatiko/gramatiko.pdf'
];

/* THE VERSIONED ADDRESSES. The Tabeli page cites its languages and its
   plates with a "?v=" that IS the file's size in bytes — checked on all
   90 of them. Two consequences: the addresses are immutable, so a
   correction changes the address; and the total weight is known without a
   single request.

   THE PATTERN NAMES NO DIRECTORY. It used to name them one by one, and a
   directory renamed on the Tabeli's side would have silently emptied the
   plan here. Any relative address bearing a "?v=" is a versioned asset,
   which is all this file needs to know. */
const VERSIONED = /[a-z]+\/[A-Za-z0-9._-]+\.(?:json|webp)\?v=\d+/g;

const fresh = u => new Request(u, { cache: 'reload', credentials: 'same-origin' });

/* ONE FILE AT A TIME, AND NOT "addAll". "addAll" is atomic: a single
   missing file, or a single request that fails, and NOTHING is cached —
   the whole shell is lost over a detail. Each file is therefore fetched
   separately, and a failure carries off only itself. */
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => Promise.all(SHELL.map(u => c.add(fresh(u)).catch(() => null))))
      .then(() => self.skipWaiting())
      .catch(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(names => Promise.all(names.filter(n => n !== CACHE).map(n => caches.delete(n))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  if (new URL(req.url).origin !== location.origin) return;
  e.respondWith(req.mode === 'navigate' ? fromNetwork(req) : fromCache(req));
});

/* Network first: the page one reads is always the latest published. */
async function fromNetwork(req) {
  const c = await caches.open(CACHE);
  try {
    const r = await fetch(fresh(req.url));
    if (r && r.ok) c.put(req.url, r.clone());
    return r;
  } catch (_) {
    return (await c.match(req.url)) || (await c.match('/')) || Response.error();
  }
}

/* Cache first, revalidation behind. */
async function fromCache(req) {
  const c = await caches.open(CACHE);
  let hit = await c.match(req);

  /* THE MAGNIFIER'S FALLBACK. The engraved plates exist in two
     resolutions: "vido" for the screen, "detalo" for the magnifier, seven
     times heavier. If the large one is missing offline, serving the small
     one gives a blurred magnifier — but an image, instead of an empty
     frame. "ignoreSearch" finds the small one whatever its version. */
  if (!hit && req.url.includes('-detalo.webp')) {
    hit = await c.match(req.url.split('?')[0].replace('-detalo.webp', '-vido.webp'),
                        { ignoreSearch: true });
    if (hit) return hit;
  }
  const network = fetch(req)
    .then(r => { if (r && r.ok) c.put(req, r.clone()); return r; })
    .catch(() => null);
  return hit || (await network) || Response.error();
}

self.addEventListener('message', e => {
  if (e.data === 'fetch-books') e.waitUntil(fetchBooks());
  if (e.data === 'revalidate')  e.waitUntil(revalidate());
  if (e.data === 'fetch-all')   e.waitUntil(fetchAll());
  if (e.data === 'state')       e.waitUntil(reportState());
  if (e.data === 'clear')       e.waitUntil(clear());
});

/* Uninstalling: everything goes, except the shell. The door has to stay
   readable offline — that is seventy kilobytes, and without it one could
   not even ask for the download again. */
async function clear() {
  const c = await caches.open(CACHE);
  const keep = new Set(SHELL.map(u => new URL(u, location).href));
  for (const req of await c.keys()) if (!keep.has(req.url)) await c.delete(req);
  await notify({ kind: 'cleared' });
}

async function notify(msg) {
  for (const cl of await self.clients.matchAll({ includeUncontrolled: true })) cl.postMessage(msg);
}

/* --- THE FULL PLAN ---------------------------------------------------
   Everything the site serves: the shell, the three texts, the PDFs, the
   52 languages and the 38 plates — both resolutions included.

   The versioned addresses are READ FROM the Tabeli's page, as the
   languages are (see syncTabeli): nothing is written here in the source,
   so nothing here can go stale. */
async function fullPlan(c) {
  const list = [...SHELL, ...BOOKS];
  if (!(await c.match('/tabeli/'))) {
    try {
      const r = await fetch(fresh('/tabeli/'));
      if (r && r.ok) await c.put('/tabeli/', r.clone());
    } catch (_) { return list; }
  }
  const held = await c.match('/tabeli/');
  if (held) {
    const text = await held.text();
    const base = new URL('/tabeli/', location).href;
    for (const u of new Set(text.match(VERSIONED) || [])) list.push(base + u);
  }
  return [...new Set(list)];
}

async function fetchAll() {
  const c = await caches.open(CACHE);
  const list = await fullPlan(c);
  let done = 0, bytes = 0;
  await notify({ kind: 'progress', done, total: list.length, bytes });

  for (const u of list) {
    const already = await c.match(u);
    if (!already) {
      try {
        const r = await fetch(fresh(u));
        if (r && r.ok) { const copy = r.clone(); await c.put(u, r); bytes += (await copy.blob()).size; }
      } catch (_) {
        await notify({ kind: 'interrupted', done, total: list.length, bytes });
        return;
      }
    } else {
      /* Already held: we WEIGH it, we do not guess it. Unversioned files
         announce no size, and "/tabeli/" is precisely one of those —
         fetched before the loop in order to read the plan from it.
         Counting it as zero lost its three megabytes. */
      bytes += (await already.blob()).size;
    }
    done++;
    if (done % 2 === 0 || done === list.length) {
      await notify({ kind: 'progress', done, total: list.length, bytes });
    }
  }
  await notify({ kind: 'done', total: list.length, bytes });
}

/* The true state: how much of the plan is actually held. We set no marker
   — a marker would lie if the browser emptied the cache. */
async function reportState() {
  const c = await caches.open(CACHE);
  if (!(await c.match('/tabeli/'))) return notify({ kind: 'state', done: 0, total: 0 });
  const list = await fullPlan(c);
  let done = 0;
  for (const u of list) if (await c.match(u)) done++;
  await notify({ kind: 'state', done, total: list.length });
}

/* The body of the books, one file at a time: twelve megabytes at once on a
   slow network would block everything else. A failure stops nothing —
   what is missing will be fetched at the next opportunity. */
async function fetchBooks() {
  const c = await caches.open(CACHE);
  for (const u of BOOKS) {
    if (await c.match(u)) continue;
    try { const r = await fetch(fresh(u)); if (r && r.ok) await c.put(u, r.clone()); }
    catch (_) { /* carry on */ }
  }
  await syncTabeli(c);
}

/* --- THE TABELI'S LANGUAGES ------------------------------------------
   The reading page is bilingual: Ido on the left, another language on the
   right. That other language is NOT in the page — it is fetched at the
   moment it is chosen, one file per language, fifty-two in all for
   24.5 MB. Offline, a language never opened was therefore missing, and the
   selector had no effect.

   THE LIST IS NOT WRITTEN HERE. It is READ FROM the page itself, already
   cached: a list copied into this file would go stale at the first change
   of address. The languages are fetched in the order the page cites them,
   so that an interrupted fetch covers the commonest first.

   AND WE PURGE ON THE WAY. All these addresses carry a "?v=": they are
   immutable, and a correction changes the address. The old one would stay
   cached indefinitely if we did not remove what the page no longer
   cites. */
async function syncTabeli(c) {
  const held = await c.match('/tabeli/');
  if (!held) return;
  const text = await held.text();
  const base = new URL('/tabeli/', location).href;
  const cited = new Set((text.match(VERSIONED) || []).map(u => base + u));
  if (!cited.size) return;

  for (const req of await c.keys()) {
    if (req.url.startsWith(base) && req.url.includes('?v=') && !cited.has(req.url)) {
      await c.delete(req);
    }
  }
  for (const u of cited) {
    if (!u.includes('/lingui/')) continue;   /* plates are fetched as they are read */
    if (await c.match(u)) continue;
    try { const r = await fetch(fresh(u)); if (r && r.ok) await c.put(u, r.clone()); }
    catch (_) { break; }                     /* the connection has gone again */
  }
}

/* When the connection returns: everything held is fetched afresh. Nothing
   is added — we only refresh what we already have. */
async function revalidate() {
  const c = await caches.open(CACHE);
  for (const req of await c.keys()) {
    /* Versioned addresses are immutable: a correction changes the address,
       and the page — always fetched from the network — cites the new one.
       Revalidating them would mean fetching 24 MB for nothing every time
       the connection came back. They are purged elsewhere, when the page
       stops citing them (see syncTabeli). */
    if (req.url.includes('?v=')) continue;
    try { const r = await fetch(fresh(req.url)); if (r && r.ok) await c.put(req, r.clone()); }
    catch (_) { break; /* the connection has gone: no point insisting */ }
  }
  await syncTabeli(c);
}
