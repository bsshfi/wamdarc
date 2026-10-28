(function () {
  var T = window.T || { ar: {}, en: {} };
  var html = document.documentElement, lang = 'ar';
  var qa = 0, qb = 0;
  function rnd() { qa = 2 + Math.floor(Math.random() * 8); qb = 1 + Math.floor(Math.random() * 9); }
  function fmt(s, o) { return String(s).replace(/\{(\w)\}/g, function (_, k) { return o[k] != null ? o[k] : _; }); }
  function $(s) { return document.querySelector(s); }

  function setLang(l) {
    lang = l === 'en' ? 'en' : 'ar';
    var d = T[lang];
    html.lang = lang; html.dir = lang === 'ar' ? 'rtl' : 'ltr';
    if (d[html.dataset.title]) document.title = d[html.dataset.title];
    var md = document.querySelector('meta[name=description]');
    if (md && d[html.dataset.desc]) md.content = d[html.dataset.desc];
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var v = d[el.getAttribute('data-i18n')]; if (v == null) return;
      if (el.hasAttribute('data-fmt')) v = fmt(v, { y: new Date().getFullYear() });
      if (el.hasAttribute('data-html')) el.innerHTML = v; else el.textContent = v;
    });
    document.querySelectorAll('[data-ph]').forEach(function (el) { var v = d[el.getAttribute('data-ph')]; if (v != null) el.placeholder = v; });
    var q = $('#qText'); if (q) q.textContent = fmt(d.f_q, { a: qa, b: qb });
    var sub = $('#fSubject'); if (sub) sub.value = d.subject;
    var nx = $('#fNext'); if (nx) nx.value = 'https://wamdarc.com/thanks.html' + (lang === 'en' ? '?lang=en' : '');
    var er = $('#fErr'); if (er) er.textContent = '';
    try { localStorage.setItem('lang', lang); } catch (e) {}
  }

  rnd();
  var q = null, saved = null;
  try { q = new URLSearchParams(location.search).get('lang'); } catch (e) {}
  try { saved = localStorage.getItem('lang'); } catch (e) {}
  setLang(q || saved || 'ar');
  var lb = $('#langBtn');
  if (lb) lb.addEventListener('click', function () { setLang(lang === 'ar' ? 'en' : 'ar'); });

  // nav: solid after scrolling
  var nav = $('#nav');
  function onScroll() { if (nav) nav.classList.toggle('solid', window.scrollY > 20); }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  // reveal on scroll
  var els = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    els.forEach(function (el) { io.observe(el); });
  } else els.forEach(function (el) { el.classList.add('in'); });

  // QR picker
  var qrImg = $('#qrImg');
  document.querySelectorAll('[data-qr]').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('[data-qr]').forEach(function (x) { x.classList.toggle('on', x === b); });
      if (qrImg) qrImg.src = qrImg.src.replace(/qr\/\w+\.svg/, 'qr/' + b.dataset.qr + '.svg');
    });
  });

  // contact form check
  var form = $('#contactForm');
  if (form) form.addEventListener('submit', function (e) {
    var err = $('#fErr');
    var ans = $('#qAns').value.trim().replace(/[٠-٩]/g, function (c) { return '٠١٢٣٤٥٦٧٨٩'.indexOf(c); });
    if (!form.checkValidity()) { e.preventDefault(); form.reportValidity(); return; }
    if (parseInt(ans, 10) !== qa + qb) {
      e.preventDefault(); err.textContent = T[lang].err_q;
      rnd(); $('#qText').textContent = fmt(T[lang].f_q, { a: qa, b: qb }); $('#qAns').value = '';
      return;
    }
    var tp = form.querySelector('input[name=topic]:checked');
    $('#fSubject').value = T[lang].subject + (tp ? ' — ' + tp.value : '');
  });
})();
