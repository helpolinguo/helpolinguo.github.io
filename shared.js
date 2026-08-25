/* =====================================================================
   THE CROSS THAT CLEARS THE SEARCH FIELD
   =====================================================================
   Companion to /shared.css, and served from the same root: the four sites
   share an origin, so a single file drives all three books. Each carries
   one line of it:

     <script src="/shared.js" defer></script>

   WHY SCRIPT, WHEN EVERYTHING ELSE IS CSS. Because there is nothing to
   style: on iOS a search field has no native cross — WebKit renders
   "::-webkit-search-cancel-button" only on macOS. An element is therefore
   needed, and an element has to be placed. Everything that shows still
   lives in the stylesheet; this file only places the cross and listens to
   it.

   IT BREAKS NOTHING IF IT FAILS TO LOAD. Without it the three fields are
   exactly what they were: you clear from the keyboard, as before.
   ===================================================================== */

(function () {
  'use strict';

  /* The stroke is written here and not in the stylesheet: a pseudo-element
     cannot carry two segments, and a background image would not take the
     text colour on hover. Fifteen units out of twenty-four, like the
     Tabeli's icons. */
  var STROKE = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
               '<path d="M7 7l10 10M17 7L7 17"/></svg>';

  /* --- THE CROSS'S HOST. ---------------------------------------------
     The cross is placed absolutely; it therefore needs a positioned parent
     that hugs the field. The Tabeli already have one — the wrapper around
     their magnifier — and it would be foolish to stack a second.

     A parent qualifies on two conditions, and both are necessary:

       1. it is already positioned, failing which the cross would attach to
          some more distant ancestor and end up anywhere;
       2. the field is its ONLY child in the flow — an icon placed
          absolutely does not count, being out of the flow. Otherwise the
          parent is the whole bar, which carries other controls, and
          hugging it would pin the cross to the edge of the bar rather than
          of the field.

     The bar of the other two books fails on both counts: it is static, and
     it carries the contents button. They therefore get the wrapper. */
  function host(field) {
    var pa = field.parentElement;
    if (!pa) return null;
    if (getComputedStyle(pa).position === 'static') return null;
    for (var i = 0; i < pa.children.length; i++) {
      var e = pa.children[i];
      if (e === field) continue;
      if (getComputedStyle(e).position !== 'absolute') return null;
    }
    return pa;
  }

  /* --- WHAT DECIDES THE FIELD'S PLACE IN THE BAR. --------------------
     A wrapper now stands between the bar and the field: it is THE WRAPPER
     that the bar lays out, and the field does no more than fill it. The
     measurements must therefore pass from one to the other.

     This is not a precaution on principle. Below 900 px the Gramatiko
     brings its field back to "flex:1 1 120px" — and its author says why in
     so many words: at a 260 px basis the field would drop below the
     contents button. A wrapper taking its basis from its content would
     measure wider, and the field would wrap again. Which is exactly what
     happened, at a 340 px viewport.

     THEY ARE RE-READ, NOT COPIED ONCE. These measurements change with the
     screen width, each book having its own; a copy taken at load would be
     wrong from the phone's first rotation. So we clear our overrides,
     re-read what the book says about the field AT THIS WIDTH, and set them
     again. */
  var MEASURES = ['flex-grow', 'flex-shrink', 'flex-basis',
                  'min-width', 'max-width', 'align-self', 'order',
                  'margin-top', 'margin-right', 'margin-bottom', 'margin-left'];

  /* The field, for its part, does no more than fill: null basis and grow,
     so that it hugs the wrapper whatever measurement the wrapper has just
     been given. */
  var FILL = 'flex:1 1 0%;min-width:0;max-width:none;margin:0;' +
             'align-self:auto;order:0';

  function matchMeasures(shell, field, own) {
    shell.removeAttribute('style');
    field.style.cssText = own;
    var s = getComputedStyle(field);
    var read = MEASURES.map(function (p) { return s.getPropertyValue(p); });
    field.style.cssText = own ? own + ';' + FILL : FILL;
    for (var i = 0; i < MEASURES.length; i++) shell.style.setProperty(MEASURES[i], read[i]);
  }

  function wrap(field) {
    var already = host(field);
    if (already) return { shell: already, own: true };

    var shell = document.createElement('span');
    shell.className = 'ido-search-shell';
    field.parentNode.insertBefore(shell, field);
    shell.appendChild(field);

    /* Whatever the book had set as an inline style on the field — nothing,
       today, but we do not take it away for all that. */
    var own = field.getAttribute('style') || '';
    matchMeasures(shell, field, own);

    /* The book's measurements depend on media rules, hence on the
       viewport. We only re-read when the viewport has REALLY changed size:
       scrolling on iPhone emits "resize" when the address bar retracts,
       and there is nothing to redo then. */
    var last = innerWidth + 'x' + innerHeight, pending = false;
    function maybe() {
      var now = innerWidth + 'x' + innerHeight;
      if (now === last || pending) return;
      last = now; pending = true;
      requestAnimationFrame(function () { pending = false; matchMeasures(shell, field, own); });
    }
    addEventListener('resize', maybe);
    addEventListener('orientationchange', maybe);

    return { shell: shell, own: false };
  }

  function prepare(field) {
    if (field.dataset.idoClear) return;      /* already done */
    field.dataset.idoClear = '1';

    var shell = wrap(field).shell;

    var cross = document.createElement('button');
    cross.type = 'button';                   /* never a form submission */
    cross.className = 'ido-clear';
    cross.innerHTML = STROKE;

    /* The name is in Ido, like the rest of the three interfaces. */
    cross.setAttribute('aria-label', 'Efacar la sercho');

    /* OUT OF THE KEYBOARD'S PATH, like the native macOS cross. It inserts
       itself between the field and the next control; making it a tab stop
       would add a halt where there was none, for a service the keyboard
       already renders — select all, then delete. Screen readers reach it
       nonetheless, the button remaining in the document and named. */
    cross.tabIndex = -1;

    shell.appendChild(cross);

    function refresh() {
      shell.classList.toggle('ido-filled', field.value !== '');
    }

    /* THE FINGER MUST NOT SCARE THE KEYBOARD AWAY. Pressing a button takes
       the caret out of the field, and on iPhone the keyboard folds away at
       once only to reopen just after: the page jumps twice. Refusing the
       press's default action leaves the caret where it is, and the click
       follows all the same. */
    cross.addEventListener('pointerdown', function (ev) { ev.preventDefault(); });
    cross.addEventListener('mousedown', function (ev) { ev.preventDefault(); });

    cross.addEventListener('click', function (ev) {
      ev.preventDefault();
      if (field.value === '') return;

      /* Was the caret IN the field? We only give it back if it was.
         Clearing from a page already scrolled — keyboard folded away, a
         result under the eye — must not bring the keyboard back up over
         what was being read. */
      var held = document.activeElement === field;

      field.value = '';

      /* The three books filter on "input". Direct assignment emits none:
         it is for us to say so, or the field would be empty and the list
         still filtered. "change" follows, for whoever listens to that one
         instead. */
      field.dispatchEvent(new Event('input', { bubbles: true }));
      field.dispatchEvent(new Event('change', { bubbles: true }));

      if (held) field.focus();
      refresh();
    });

    field.addEventListener('input', refresh);
    field.addEventListener('change', refresh);

    /* On going back, Safari restores field contents AFTER load, from its
       page cache. Without this listener the cross would be missing from a
       field that is in fact filled. */
    window.addEventListener('pageshow', refresh);

    refresh();
  }

  function sow() {
    var fields = document.querySelectorAll('input[type=search]');
    for (var i = 0; i < fields.length; i++) prepare(fields[i]);
  }

  /* The script is deferred: the document is parsed when it runs. The guard
     covers the case where it were one day called otherwise. */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', sow);
  } else {
    sow();
  }
})();
