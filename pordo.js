/* =====================================================================
   LA CROIX QUI VIDE LE CHAMP DE RECHERCHE
   =====================================================================
   Compagnon de /pordo.css, et servi de la même racine : les quatre sites
   partagent une origine, de sorte qu'un seul fichier tient la conduite
   des trois livres. Chacun n'en porte qu'une ligne :

     <script src="/pordo.js" defer></script>

   POURQUOI DU SCRIPT, ALORS QUE TOUT LE RESTE EST EN CSS. Parce qu'il
   n'y a rien à styler : sur iOS, le champ de recherche n'a pas de croix
   native — WebKit ne rend « ::-webkit-search-cancel-button » que sur
   macOS. Il faut donc un élément, et un élément se pose. Tout ce qui se
   voit reste néanmoins dans la feuille ; ce fichier ne fait que placer
   la croix et l'écouter.

   IL NE CASSE RIEN S'IL NE SE CHARGE PAS. Sans lui, les trois champs
   sont exactement ce qu'ils étaient : on vide au clavier, comme avant.
   ===================================================================== */

(function () {
  'use strict';

  /* Le trait est écrit ici et non dans la feuille : un pseudo-élément ne
     peut pas porter deux segments, et une image de fond ne prendrait pas
     la couleur du texte au survol. Quinze unités sur vingt-quatre, comme
     les icônes des Tabeli. */
  var TRAIT = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
              '<path d="M7 7l10 10M17 7L7 17"/></svg>';

  /* --- L'HOTE DE LA CROIX. -------------------------------------------
     La croix se pose en absolu ; il lui faut donc un parent positionné
     qui épouse le champ. Les Tabeli en ont déjà un — l'enveloppe de leur
     loupe —, et il serait sot d'en empiler un second.

     Le parent convient à deux conditions, et les deux sont nécessaires :

       1. il est déjà positionné, sans quoi la croix se rangerait sur un
          ancêtre plus lointain et se retrouverait n'importe où ;
       2. le champ est son SEUL enfant dans le flux — une icône posée en
          absolu ne compte pas, elle est hors du flux. Sinon le parent est
          la barre entière, qui porte d'autres commandes, et l'épouser
          collerait la croix au bord de la barre et non du champ.

     La barre des deux autres livres échoue aux deux : elle est statique,
     et elle porte le bouton du sommaire. Ils reçoivent donc l'enveloppe. */
  function hoto(kampo) {
    var pa = kampo.parentElement;
    if (!pa) return null;
    if (getComputedStyle(pa).position === 'static') return null;
    for (var i = 0; i < pa.children.length; i++) {
      var e = pa.children[i];
      if (e === kampo) continue;
      if (getComputedStyle(e).position !== 'absolute') return null;
    }
    return pa;
  }

  /* --- CE QUI DECIDE DE LA PLACE DU CHAMP DANS LA BARRE. -------------
     Une enveloppe s'interpose entre la barre et le champ : c'est ELLE,
     desormais, que la barre range, et le champ ne fait plus que remplir
     l'enveloppe. Les mesures doivent donc passer de l'un a l'autre.

     Ce n'est pas une precaution de principe. Sous 900 px, la Gramatiko
     ramene son champ a « flex:1 1 120px » — et son auteur dit pourquoi
     en toutes lettres : a 260 px de base, le champ passerait sous le
     bouton du sommaire. Une enveloppe qui prendrait sa base de son
     contenu, elle, mesurerait plus large, et le champ repasserait a la
     ligne. C'est exactement ce qui arrivait, a 340 px de vue.

     ELLES SONT RELUES, ET NON RECOPIEES UNE FOIS. Ces mesures changent
     avec la largeur de l'ecran, chaque livre ayant les siennes ; une
     copie prise au chargement serait fausse des la premiere rotation du
     telephone. On efface donc nos surcharges, on relit ce que le livre
     dit du champ A CETTE LARGEUR, et on repose. */
  var MEZURI = ['flex-grow', 'flex-shrink', 'flex-basis',
                'min-width', 'max-width', 'align-self', 'order',
                'margin-top', 'margin-right', 'margin-bottom', 'margin-left'];

  /* Le champ, lui, ne fait plus que remplir : base nulle et croissance,
     de sorte qu'il epouse l'enveloppe quelle que soit la mesure que
     celle-ci vient de recevoir. */
  var PLENIGA = 'flex:1 1 0%;min-width:0;max-width:none;margin:0;' +
                'align-self:auto;order:0';

  function akordigi(env, kampo, propra) {
    env.removeAttribute('style');
    kampo.style.cssText = propra;
    var s = getComputedStyle(kampo);
    var legita = MEZURI.map(function (p) { return s.getPropertyValue(p); });
    kampo.style.cssText = propra ? propra + ';' + PLENIGA : PLENIGA;
    for (var i = 0; i < MEZURI.length; i++) env.style.setProperty(MEZURI[i], legita[i]);
  }

  function envelopar(kampo) {
    var jam = hoto(kampo);
    if (jam) return { env: jam, propra: true };

    var env = document.createElement('span');
    env.className = 'ido-envelopo';
    kampo.parentNode.insertBefore(env, kampo);
    env.appendChild(kampo);

    /* Ce que le livre avait pose en style en ligne sur le champ — rien,
       aujourd'hui, mais on ne le lui prend pas pour autant. */
    var propra = kampo.getAttribute('style') || '';
    akordigi(env, kampo, propra);

    /* Les mesures du livre dependent de regles de media, donc de la vue.
       On ne relit que si la vue a REELLEMENT change de taille : un
       defilement sur iPhone emet « resize » quand la barre d'adresse se
       retracte, et il n'y a alors rien a refaire. */
    var lasta = innerWidth + 'x' + innerHeight, atendas = false;
    function eble() {
      var nun = innerWidth + 'x' + innerHeight;
      if (nun === lasta || atendas) return;
      lasta = nun; atendas = true;
      requestAnimationFrame(function () { atendas = false; akordigi(env, kampo, propra); });
    }
    addEventListener('resize', eble);
    addEventListener('orientationchange', eble);

    return { env: env, propra: false };
  }

  function pretigar(kampo) {
    if (kampo.dataset.idoKruco) return;      /* déjà fait */
    kampo.dataset.idoKruco = '1';

    var env = envelopar(kampo).env;

    var kruco = document.createElement('button');
    kruco.type = 'button';                   /* jamais un envoi de formulaire */
    kruco.className = 'ido-kruco';
    kruco.innerHTML = TRAIT;

    /* Le nom est en ido comme le reste des trois interfaces. */
    kruco.setAttribute('aria-label', 'Efacar la sercho');

    /* HORS DU PARCOURS DU CLAVIER, comme la croix native de macOS. Elle
       s'insère entre le champ et la commande suivante ; en faire une
       halte de tabulation ajouterait un arrêt là où il n'y en avait pas,
       pour un service que le clavier rend déjà — tout sélectionner, puis
       effacer. Les lecteurs d'écran l'atteignent néanmoins, le bouton
       restant dans le document et nommé. */
    kruco.tabIndex = -1;

    env.appendChild(kruco);

    function montrar() {
      env.classList.toggle('ido-plena', kampo.value !== '');
    }

    /* LE DOIGT NE DOIT PAS FAIRE FUIR LE CLAVIER. Une pression sur un
       bouton retire le curseur du champ, et sur iPhone le clavier se
       replie aussitôt pour se rouvrir juste après : la page saute deux
       fois. Refuser l'effet par défaut de la pression laisse le curseur
       où il est, et le clic suit tout de même. */
    kruco.addEventListener('pointerdown', function (ev) { ev.preventDefault(); });
    kruco.addEventListener('mousedown', function (ev) { ev.preventDefault(); });

    kruco.addEventListener('click', function (ev) {
      ev.preventDefault();
      if (kampo.value === '') return;

      /* Le curseur était-il DANS le champ ? On ne le rend que s'il y
         était. Vider depuis une page déjà parcourue — le clavier replié,
         un résultat sous les yeux — ne doit pas faire remonter le clavier
         par-dessus ce qu'on lisait. */
      var tenis = document.activeElement === kampo;

      kampo.value = '';

      /* Les trois livres filtrent sur « input ». L'affectation directe
         n'en émet aucun : c'est à nous de le dire, sans quoi le champ
         serait vide et la liste toujours filtrée. « change » suit pour
         qui écouterait plutôt celui-là. */
      kampo.dispatchEvent(new Event('input', { bubbles: true }));
      kampo.dispatchEvent(new Event('change', { bubbles: true }));

      if (tenis) kampo.focus();
      montrar();
    });

    kampo.addEventListener('input', montrar);
    kampo.addEventListener('change', montrar);

    /* Au retour en arrière, Safari restitue le contenu des champs APRES
       le chargement, depuis son cache de pages. Sans cette écoute la
       croix manquerait sur un champ pourtant rempli. */
    window.addEventListener('pageshow', montrar);

    montrar();
  }

  function semar() {
    var kampi = document.querySelectorAll('input[type=search]');
    for (var i = 0; i < kampi.length; i++) pretigar(kampi[i]);
  }

  /* Le script est différé : le document est analysé quand il s'exécute.
     La garde couvre le cas où il serait un jour appelé autrement. */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', semar);
  } else {
    semar();
  }
})();
