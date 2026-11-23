/* ومض آرك | WAMD ARC — wamdarc.com
   المظهر (نهار/ليل)، اللغة (عربي/English)، القائمة، القوس، التثبيت، نموذج التواصل، فلتر جديدنا */
(function () {
  'use strict';
  var T = window.T || { ar: {}, en: {} };
  var html = document.documentElement, lang = 'ar';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var store = function (k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } };
  var qa = 0, qb = 0;
  function rnd() { qa = 2 + Math.floor(Math.random() * 8); qb = 1 + Math.floor(Math.random() * 9); }
  function fmt(s, o) { return String(s).replace(/\{(\w)\}/g, function (_, k) { return o[k] != null ? (lang === 'ar' ? String(o[k]).replace(/\d/g, function (d) { return '٠١٢٣٤٥٦٧٨٩'[d]; }) : o[k]) : _; }); }

  /* ---------- اللغة ---------- */
  function setLang(l) {
    lang = l === 'en' ? 'en' : 'ar';
    var d = T[lang];
    html.lang = lang; html.dir = lang === 'ar' ? 'rtl' : 'ltr';
    if (d[html.dataset.title]) document.title = d[html.dataset.title];
    var md = $('meta[name=description]'); if (md && d[html.dataset.desc]) md.content = d[html.dataset.desc];
    $$('[data-i18n]').forEach(function (el) {
      var v = d[el.getAttribute('data-i18n')]; if (v == null) return;
      if (el.hasAttribute('data-html')) el.innerHTML = v; else el.textContent = v;
    });
    $$('[data-ph]').forEach(function (el) { var v = d[el.getAttribute('data-ph')]; if (v != null) el.placeholder = v; });
    $$('[data-i18n-aria]').forEach(function (el) { var v = d[el.getAttribute('data-i18n-aria')]; if (v != null) el.setAttribute('aria-label', v); });
    var lb = $('#langBtn'); if (lb) lb.lang = lang === 'ar' ? 'en' : 'ar';
    var q = $('#qText'); if (q) q.textContent = fmt(d.f_q, { a: qa, b: qb });
    var sub = $('#fSubject'); if (sub) sub.value = d.subject;
    var nx = $('#fNext'); if (nx) nx.value = 'https://wamdarc.com/thanks.html' + (lang === 'en' ? '?lang=en' : '');
    var er = $('#fErr'); if (er) er.textContent = '';
    themeLabel();
    store('lang', lang);
    if (window.__place) window.__place();
  }

  /* ---------- المظهر: نهار (افتراضي) / ليل ---------- */
  function themeLabel() {
    var b = $('#themeBtn'); if (!b) return;
    var k = html.dataset.d === 'night' ? 'th_light' : 'th_dark';
    b.setAttribute('aria-label', (T[lang] || T.ar)[k] || '');
    b.setAttribute('aria-pressed', html.dataset.d === 'night' ? 'true' : 'false');
  }
  function setTheme(m) {
    html.dataset.d = m === 'night' ? 'night' : 'day';
    var tc = $('#tc'); if (tc) tc.content = m === 'night' ? '#17104A' : '#F6F5FC';
    store('wa-theme', html.dataset.d);
    themeLabel();
    if (window.__place) window.__place(true);
  }
  var tb = $('#themeBtn');
  if (tb) tb.addEventListener('click', function () { setTheme(html.dataset.d === 'night' ? 'day' : 'night'); });

  rnd();
  var ql = null; try { ql = new URLSearchParams(location.search).get('lang'); } catch (e) {}
  setLang(ql || store('lang') || 'ar');
  var lbtn = $('#langBtn');
  if (lbtn) lbtn.addEventListener('click', function () { setLang(lang === 'ar' ? 'en' : 'ar'); });
  var yr = $('#yr'); if (yr) yr.textContent = new Date().getFullYear();

  /* ---------- الشريط العلوي والقائمة ---------- */
  var nav = $('#nav'), menu = $('#menuBtn');
  function onScroll() { if (nav) nav.classList.toggle('solid', scrollY > 12); }
  onScroll(); addEventListener('scroll', onScroll, { passive: true });
  function closeMenu() { if (!nav) return; nav.classList.remove('open'); if (menu) menu.setAttribute('aria-expanded', 'false'); }
  if (menu) menu.addEventListener('click', function () {
    var o = !nav.classList.contains('open'); nav.classList.toggle('open', o); menu.setAttribute('aria-expanded', o ? 'true' : 'false');
  });
  $$('#navList a').forEach(function (a) { a.addEventListener('click', closeMenu); });
  addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });
  // الصفحة الحالية
  $$('#navList a').forEach(function (a) { if (a.getAttribute('href') === location.pathname) a.setAttribute('aria-current', 'page'); });

  /* ---------- التثبيت: آيفون / أندرويد ---------- */
  var ua = navigator.userAgent;
  $$('.seg button').forEach(function (b) {
    b.addEventListener('click', function () {
      $$('.seg button').forEach(function (x) { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      $$('.steps').forEach(function (o) { o.hidden = o.dataset.os !== b.dataset.os; });
    });
  });
  if (/android/i.test(ua)) { var ab = $('.seg button[data-os=and]'); if (ab) ab.click(); }

  /* ---------- «أرسل فكرتك» يختار الموضوع ---------- */
  $$('[data-topic]').forEach(function (a) { a.addEventListener('click', function () { var s = $('#fTopic'); if (s) s.value = 'Idea'; }); });

  /* ---------- نموذج التواصل ---------- */
  var form = $('#contactForm');
  if (form) form.addEventListener('submit', function (e) {
    var err = $('#fErr');
    if (!form.checkValidity()) { e.preventDefault(); err.textContent = T[lang].err_form; form.reportValidity(); return; }
    var ans = $('#qAns').value.trim().replace(/[٠-٩]/g, function (c) { return '٠١٢٣٤٥٦٧٨٩'.indexOf(c); });
    if (parseInt(ans, 10) !== qa + qb) {
      e.preventDefault(); err.textContent = T[lang].err_q;
      rnd(); $('#qText').textContent = fmt(T[lang].f_q, { a: qa, b: qb }); $('#qAns').value = ''; $('#qAns').focus();
      return;
    }
    var tp = $('#fTopic');
    $('#fSubject').value = T[lang].subject + (tp && tp.value !== 'General' ? ' — ' + tp.value : '');
  });

  /* ---------- جديدنا: فلتر حسب التطبيق ---------- */
  var chips = $('#chips');
  if (chips) chips.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    var f = b.dataset.f;
    $$('button', chips).forEach(function (x) { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    $$('.nc').forEach(function (c) { c.hidden = !(f === 'all' || c.dataset.app === f || c.dataset.app === 'all'); });
    $$('.mh').forEach(function (h) { var n = h.nextElementSibling; h.hidden = n && !$$('.nc', n).some(function (c) { return !c.hidden; }); if (n) n.hidden = h.hidden; });
  });

  /* ---------- القوس (الليل): التطبيقات محطات عليه، والشرارة تمشي عليه مرة عند الفتح ---------- */
  var orbit = $('#orbit'), path = $('#arcPath'), spark = $('#spark');
  if (!orbit || !path) return;
  var stops = $$('.stop', orbit);
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var Tn = function () { return innerWidth <= 900 ? [.93, .77, .6, .4, .23, .07] : [.95, .855, .755, .245, .145, .05]; };
  function at(t) {
    var L = path.getTotalLength(), p = path.getPointAtLength(L * t), r = orbit.getBoundingClientRect();
    return { x: p.x / 1200 * r.width, y: p.y / 560 * r.height };
  }
  // في الإنجليزي (يسار لليمين) يبدأ الترتيب من اليسار
  function pos(i) { var T_ = Tn(), t_ = T_[i]; return html.dir === 'ltr' ? 1 - t_ : t_; }
  function place(fromToggle) {
    if (html.dataset.d !== 'night') {
      stops.forEach(function (s) { s.style.left = s.style.top = s.style.opacity = s.style.transition = ''; });
      path.style.strokeDasharray = path.style.strokeDashoffset = ''; return;
    }
    stops.forEach(function (s, i) { var p = at(pos(i)); s.style.left = p.x + 'px'; s.style.top = p.y + 'px'; });
    var a = at(.5); spark.style.left = a.x + 'px'; spark.style.top = a.y + 'px';
    if (fromToggle === true) run();
  }
  window.__place = place;
  var ran = false;
  function run() {
    if (html.dataset.d !== 'night') return;
    var L = path.getTotalLength();
    if (still || ran) { orbit.classList.add('shown'); stops.forEach(function (s) { s.style.opacity = 1; }); spark.style.opacity = 1; path.style.strokeDasharray = path.style.strokeDashoffset = ''; return; }
    ran = true;
    path.style.strokeDasharray = L; path.style.strokeDashoffset = L;
    stops.forEach(function (s) { s.style.opacity = 0; });
    var t0 = performance.now(), D = 1600;
    var ease = function (x) { return 1 - Math.pow(1 - x, 3); };
    (function frame(now) {
      var k = Math.min(1, (now - t0) / D), e = ease(k);
      path.style.strokeDashoffset = L * (1 - e);
      var p = at(Math.min(e, .5)); spark.style.left = p.x + 'px'; spark.style.top = p.y + 'px'; spark.style.opacity = 1;
      stops.forEach(function (s, i) { if (e >= pos(i)) { s.style.transition = 'opacity .4s'; s.style.opacity = 1; } });
      if (k < 1) requestAnimationFrame(frame);
      else { orbit.classList.add('shown'); stops.forEach(function (s) { s.style.opacity = 1; }); path.style.strokeDasharray = path.style.strokeDashoffset = ''; var a = at(.5); spark.style.left = a.x + 'px'; spark.style.top = a.y + 'px'; }
    })(t0);
  }
  place(); run();
  var rt; addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(place, 80); });
})();
