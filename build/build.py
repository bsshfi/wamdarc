# -*- coding: utf-8 -*-
"""يبني صفحات wamdarc.com من build/content.py
python3 build/build.py   ← يكتب index.html وصفحات التطبيقات و privacy و updates و thanks و 404 و sitemap و assets/i18n.js"""
import os, json, html
from content import APPS, S, VOWS, NEWS, MONTHS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = '12'                      # رقم كاش الملفات (?v=)
SITE = 'https://wamdarc.com'
LASTMOD = '2026-11-24'
A = {a['id']: a for a in APPS}

# ---------- النصوص ----------
T = {'ar': {}, 'en': {}}
def reg(k, ar, en):
    T['ar'][k] = ar; T['en'][k] = en
for k, (a, e) in S.items(): reg(k, a, e)
for a in APPS:
    i = a['id']
    reg(i + '_nm', a['ar'], a['name_en'])
    for f in ('tag', 'short', 'lead', 'pv'): reg(f'{i}_{f}', *a[f])
    reg(i + '_open', 'افتح ' + a['ar'], 'Open ' + a['name_en'])
    for n, (x, y) in enumerate(a['tags']): reg(f'{i}_t{n}', x, y)
    for n, (_, x, y) in enumerate(a['shots']): reg(f'{i}_c{n}', x, y)
    for n, (_, t1, d1, t2, d2) in enumerate(a['feats']): reg(f'{i}_f{n}t', t1, t2); reg(f'{i}_f{n}d', d1, d2)
    for n, (q1, a1, q2, a2) in enumerate(a['faq']): reg(f'{i}_q{n}', q1, q2); reg(f'{i}_a{n}', a1, a2)
    reg(f'title_{i}', f"{a['ar']} | {a['en']} — {a['tag'][0]} | ومض آرك", f"{a['name_en']} | {a['en']} — {a['tag'][1]} | WAMD ARC")
for n, (m1, m2) in enumerate(MONTHS, 1): reg(f'm{n}', m1, m2)
for n, (_, _, _, items) in enumerate(NEWS):
    for j, (x, y) in enumerate(items): reg(f'n{n}_{j}', x, y)

def ar(k): return T['ar'][k]
def esc(s): return html.escape(s, quote=True)
def t(k, tag='span', cls='', raw=False, attrs=''):
    c = f' class="{cls}"' if cls else ''
    h = ' data-html' if raw else ''
    return f'<{tag}{c} data-i18n="{k}"{h}{attrs}>{ar(k)}</{tag}>'
def nm(a, tag='span'):
    """اسم التطبيق بالصيغة الموحّدة «سهم | SAHM» (نفسه في اللغتين)"""
    return f'<{tag} class="nm">{a["ar"]}<i aria-hidden="true">|</i><span class="ltr">{a["en"]}</span></{tag}>'
def icon(a, size=72, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="/assets/{a["id"]}/icon.webp" alt="" width="{size}" height="{size}">'

SUN = '<svg class="i-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M4.6 4.6l1.6 1.6M17.8 17.8l1.6 1.6M2.5 12h2.2M19.3 12h2.2M4.6 19.4l1.6-1.6M17.8 6.2l1.6-1.6"/></svg>'
MOON = '<svg class="i-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.6A8.5 8.5 0 0 1 9.4 4a8.5 8.5 0 1 0 10.6 10.6z"/></svg>'
MENU = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
CHEV = '<svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>'

# ---------- القالب ----------
def head(path, title_k, desc_k, og='og-image', ld=None, extra=''):
    url = SITE + path
    ldj = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n' if ld else ''
    return f'''<!doctype html>
<html lang="ar" dir="rtl" data-d="day" data-title="{title_k}" data-desc="{desc_k}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(ar(title_k))}</title>
<meta name="description" content="{esc(ar(desc_k))}">
<meta name="theme-color" content="#F6F5FC" id="tc">
<script>(function(){{var d=document.documentElement,m='day',l='ar';try{{m=localStorage.getItem('wa-theme')==='night'?'night':'day';l=new URLSearchParams(location.search).get('lang')||localStorage.getItem('lang')||'ar'}}catch(e){{}}d.dataset.d=m;if(m==='night')document.getElementById('tc').content='#17104A';if(l==='en'){{d.lang='en';d.dir='ltr'}}}})();</script>
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ar" href="{url}"><link rel="alternate" hreflang="en" href="{url}?lang=en"><link rel="alternate" hreflang="x-default" href="{url}">
<link rel="icon" href="/assets/favicon.svg?v={V}" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png?v={V}">
<meta property="og:type" content="website"><meta property="og:site_name" content="ومض آرك | WAMD ARC">
<meta property="og:url" content="{url}"><meta property="og:title" content="{esc(ar(title_k))}"><meta property="og:description" content="{esc(ar(desc_k))}">
<meta property="og:image" content="{SITE}/assets/{og}.png?v={V}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="ar_SA"><meta property="og:locale:alternate" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:site" content="@wamdarc">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={V}">
{ldj}{extra}</head>
<body>
<a class="skip" href="#main" data-i18n="skip">{ar("skip")}</a>
'''

def nav(home=False):
    h = '' if home else '/'
    links = [('apps', 'nav_apps'), ('promise', 'nav_promise'), ('install', 'nav_install'), ('about', 'nav_about'), ('contact', 'nav_contact')]
    lis = ''.join(f'<li><a href="{h}#{x}" data-i18n="{k}">{ar(k)}</a></li>' for x, k in links) + f'<li><a href="/updates/" data-i18n="nav_news">{ar("nav_news")}</a></li>'
    return f'''<header class="nav" id="nav">
  <div class="wrap">
    <a class="brand" href="/" aria-label="ومض آرك WAMD ARC">
      <img class="on-light" src="/assets/logo-horizontal-on-light.svg?v={V}" alt="WAMD ARC ومض ارك" width="206" height="32">
      <img class="on-dark" src="/assets/logo-horizontal-on-dark.svg?v={V}" alt="WAMD ARC ومض ارك" width="206" height="32">
    </a>
    <nav aria-label="{ar('nav_menu')}" data-i18n-aria="nav_menu">
      <ul id="navList">{lis}</ul>
      <div class="tools">
        <button class="ib" id="themeBtn" type="button" aria-label="{ar('th_dark')}">{MOON}{SUN}</button>
        <button class="lang" id="langBtn" type="button" lang="en" aria-label="{ar('lang_aria')}" data-i18n-aria="lang_aria" data-i18n="lang_btn">{ar('lang_btn')}</button>
        <button class="ib menu" id="menuBtn" type="button" aria-expanded="false" aria-controls="navList" aria-label="{ar('nav_menu')}" data-i18n-aria="nav_menu">{MENU}</button>
      </div>
    </nav>
  </div>
</header>
'''

def footer():
    apps = ''.join(f'<a href="/{a["id"]}/" style="--c:{a["color"]}">{nm(a)}</a>' for a in APPS)
    return f'''<footer class="foot">
  <div class="wrap foot-in">
    <div class="fbrand">
      <img class="on-light" src="/assets/logo-horizontal-on-light.svg?v={V}" alt="WAMD ARC ومض ارك" width="190" height="30" loading="lazy">
      <img class="on-dark" src="/assets/logo-horizontal-on-dark.svg?v={V}" alt="WAMD ARC ومض ارك" width="190" height="30" loading="lazy">
      {t('foot_tag', 'p')}
    </div>
    <div>{t('foot_apps', 'b')}{apps}</div>
    <div>{t('foot_co', 'b')}<a href="/#about" data-i18n="nav_about">{ar('nav_about')}</a><a href="/updates/" data-i18n="nav_news">{ar('nav_news')}</a><a href="/#contact" data-i18n="nav_contact">{ar('nav_contact')}</a><a href="/privacy/" data-i18n="privacy">{ar('privacy')}</a></div>
  </div>
  <div class="wrap legal"><span>© <span id="yr">2026</span> WAMD ARC · {t('made_in')}</span><a class="ltr" href="mailto:contact@wamdarc.com">contact@wamdarc.com</a></div>
</footer>
<script src="/assets/i18n.js?v={V}"></script>
<script src="/assets/site.js?v={V}"></script>
<script src="/assets/wamd-stats.js?v={V}" data-app="site" defer></script>
</body>
</html>
'''

def tags(a):
    return '<ul class="tags">' + ''.join(f'<li data-i18n="{a["id"]}_t{n}">{x}</li>' for n, (x, _) in enumerate(a['tags'])) + '</ul>'

def faq_list(items):
    return ''.join(f'<details><summary>{t(q)}{CHEV}</summary>{t(a_, "p")}</details>' for q, a_ in items)

# ---------- الرئيسية ----------
def home():
    stops = ''.join(f'<a class="stop" href="#app-{a["id"]}" style="--c:{a["color"]}"><img src="/assets/{a["id"]}/icon.webp" alt="" width="72" height="72"><span data-i18n="{a["id"]}_nm">{a["ar"]}</span></a>' for a in APPS)
    apps = ''
    for a in APPS:
        i = a['id']
        badge = f' <em data-i18n="new">{ar("new")}</em>' if a.get('new') else ''
        apps += f'''
        <article class="app" id="app-{i}" style="--c:{a['color']}">
          <a class="ai" href="/{i}/" tabindex="-1" aria-hidden="true">{icon(a)}</a>
          <div class="meta">
            <h3><a href="/{i}/">{nm(a)}</a>{badge}</h3>
            {t(i + '_short', 'p')}
            {tags(a)}
          </div>
          <div class="acts"><a class="btn sm primary" href="https://{i}.wamdarc.com/" data-i18n="open">{ar('open')}</a><a class="more" href="/{i}/" data-i18n="details">{ar('details')}</a></div>
        </article>'''
    vows = ''.join(f'<li><svg viewBox="0 0 24 24" aria-hidden="true">{p}</svg>{t(k + "t", "b")}{t(k + "d")}</li>' for k, p in VOWS)
    steps = lambda os_: ''.join(f'<li>{t(f"{os_}{n}t", "b", raw=True)}{t(f"{os_}{n}d")}</li>' for n in (1, 2, 3))
    gfaq = faq_list([(f'g{n}q', f'g{n}a') for n in range(6)])
    opts = ''.join(f'<option value="{a["name_en"]}" data-i18n="{a["id"]}_nm">{a["ar"]}</option>' for a in APPS)
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": "WAMD ARC", "alternateName": "ومض آرك", "url": SITE + '/',
          "logo": SITE + '/assets/icon-512.png', "email": "contact@wamdarc.com",
          "sameAs": ["https://x.com/wamdarc", "https://instagram.com/wamdarc", "https://www.tiktok.com/@wamd.arc"]}
    body = f'''{nav(True)}
<main id="main">
  <section class="hero" id="top">
    <div class="sky" aria-hidden="true"></div>
    <div class="wrap hero-in">
      <div class="hero-txt">
        {t('h1', 'h1', raw=True)}
        {t('lead', 'p', 'lead')}
        <div class="cta"><a class="btn primary" href="#apps" data-i18n="cta_apps">{ar('cta_apps')}</a><a class="btn ghost" href="#contact" data-i18n="cta_contact">{ar('cta_contact')}</a></div>
        {t('store', 'p', 'store', raw=True)}
      </div>
      <div class="orbit" id="orbit">
        <svg class="arc" viewBox="0 0 1200 560" preserveAspectRatio="none" aria-hidden="true">
          <defs><linearGradient id="ag" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#6A3DE8"/><stop offset=".55" stop-color="#9B52D8"/><stop offset="1" stop-color="#FF8A2A"/></linearGradient></defs>
          <path class="halo" d="M40 560 C 190 40, 1010 40, 1160 560"/>
          <path class="line" id="arcPath" d="M40 560 C 190 40, 1010 40, 1160 560"/>
        </svg>
        <i class="spark" id="spark" aria-hidden="true"></i>
        {stops}
      </div>
    </div>
  </section>

  <section class="sec apps" id="apps">
    <div class="wrap">
      <div class="head">{t('apps_h2', 'h2')}{t('apps_sub', 'p')}</div>
      <div class="list">{apps}
      </div>
    </div>
  </section>

  <section class="sec promise" id="promise">
    <div class="wrap">
      <div class="head">{t('prom_h2', 'h2')}</div>
      <ul class="vows">{vows}</ul>
      {t('prom_note', 'p', 'fine', raw=True)}
    </div>
  </section>

  <section class="sec install" id="install">
    <div class="wrap">
      <div class="head">{t('inst_h2', 'h2')}{t('inst_sub', 'p')}</div>
      <div class="seg" role="group"><button class="on" type="button" data-os="ios" aria-pressed="true" data-i18n="ios">{ar('ios')}</button><button type="button" data-os="and" aria-pressed="false" data-i18n="android">{ar('android')}</button></div>
      <ol class="steps" data-os="ios">{steps('ios')}</ol>
      <ol class="steps" data-os="and" hidden>{steps('and')}</ol>
      {t('inst_note', 'p', 'fine')}
    </div>
  </section>

  <section class="sec about" id="about">
    <div class="wrap about-in">
      <div>{t('about_h2', 'h2')}{t('about_p1', 'p')}{t('about_p2', 'p')}</div>
      <aside class="idea">{t('idea_t', 'b')}{t('idea_d')}<a class="btn ghost sm" href="#contact" data-topic="idea" data-i18n="idea_b">{ar('idea_b')}</a></aside>
    </div>
  </section>

  <section class="sec faq" id="faq">
    <div class="wrap faq-in">
      <div class="head">{t('faq_h2', 'h2')}</div>
      <div class="qa">{gfaq}</div>
    </div>
  </section>

  <section class="sec contact" id="contact">
    <div class="wrap contact-in">
      <div>
        {t('contact_h2', 'h2')}{t('contact_lead', 'p')}
        <ul class="ways">
          <li>{t('w_mail')}<a class="ltr" href="mailto:contact@wamdarc.com">contact@wamdarc.com</a></li>
          <li>{t('w_x')}<a class="ltr" href="https://x.com/wamdarc" rel="noopener">@wamdarc</a></li>
          <li>{t('w_ig')}<a class="ltr" href="https://instagram.com/wamdarc" rel="noopener">@wamdarc</a></li>
          <li>{t('w_tt')}<a class="ltr" href="https://www.tiktok.com/@wamd.arc" rel="noopener">@wamd.arc</a></li>
        </ul>
      </div>
      <form class="form" id="contactForm" action="https://formsubmit.co/contact@wamdarc.com" method="POST" novalidate>
        <input type="hidden" name="_subject" id="fSubject" value="{ar('subject')}">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="true">
        <input type="hidden" name="_next" id="fNext" value="{SITE}/thanks.html">
        <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <label>{t('f_topic')}<select name="topic" id="fTopic"><option value="General" data-i18n="t_general">{ar('t_general')}</option>{opts}<option value="Idea" data-i18n="t_idea">{ar('t_idea')}</option></select></label>
        <div class="two">
          <label>{t('f_name')}<input type="text" name="name" required maxlength="80" autocomplete="name" data-ph="ph_name" placeholder="{ar('ph_name')}"></label>
          <label>{t('f_email')}<input type="email" name="email" dir="ltr" required maxlength="120" autocomplete="email" data-ph="ph_email" placeholder="{ar('ph_email')}"></label>
        </div>
        <label>{t('f_msg')}<textarea name="message" rows="5" required minlength="10" maxlength="3000" data-ph="ph_msg" placeholder="{ar('ph_msg')}"></textarea></label>
        <label class="q"><span id="qText"></span><input type="text" id="qAns" inputmode="numeric" autocomplete="off" required data-ph="ph_q" placeholder="{ar('ph_q')}"></label>
        <p class="err" id="fErr" role="alert"></p>
        <button class="btn primary" type="submit" data-i18n="f_send">{ar('f_send')}</button>
        {t('f_note', 'p', 'note')}
      </form>
    </div>
  </section>
</main>
'''
    return head('/', 'title_home', 'desc_home', 'og-image', ld) + body + footer()

# ---------- صفحة التطبيق ----------
def app_page(a):
    i = a['id']
    feats = ''.join(f'<li><span class="fi" aria-hidden="true">{e}</span><div>{t(f"{i}_f{n}t", "b")}{t(f"{i}_f{n}d")}</div></li>' for n, (e, *_r) in enumerate(a['feats']))
    sh = a['shots']
    def phone(n, cls=''):
        return f'<figure class="shot{cls}"><div class="phone"><img src="/assets/{i}/{sh[n][0]}.webp" alt="{esc(sh[n][1])}" width="600" height="1298" loading="{"eager" if n == 0 else "lazy"}"></div>{t(f"{i}_c{n}", "figcaption") if n else ""}</figure>'
    others = ''.join(f'<a href="/{o["id"]}/" style="--c:{o["color"]}">{icon(o, 56)}<span class="ot">{nm(o)}{t(o["id"] + "_tag", "small")}</span></a>' for o in APPS if o['id'] != i)
    badge = f'<em data-i18n="new">{ar("new")}</em>' if a.get('new') else ''
    ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": f"{a['ar']} | {a['en']}", "alternateName": [a['name_en'], a['ar']],
          "url": f"https://{i}.wamdarc.com/", "applicationCategory": a['cat'], "operatingSystem": "iOS, Android, Web",
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "SAR"}, "inLanguage": ["ar", "en"],
          "publisher": {"@type": "Organization", "name": "WAMD ARC", "url": SITE + '/'}, "description": a['short'][1],
          "image": f"{SITE}/assets/{i}/icon.webp"}
    body = f'''{nav()}
<main id="main" style="--c:{a['color']}">
  <section class="ahero">
    <div class="wrap ahero-in">
      <div class="ahero-txt">
        <div class="aid">{icon(a, 88, 'aicon')}{badge}</div>
        <h1>{nm(a)}</h1>
        {t(i + '_tag', 'p', 'atag')}
        {t(i + '_lead', 'p', 'lead')}
        <div class="cta"><a class="btn primary" href="https://{i}.wamdarc.com/" data-i18n="{i}_open">{ar(i + '_open')}</a><a class="btn ghost" href="/#install" data-i18n="how_install">{ar('how_install')}</a></div>
        {tags(a)}
      </div>
      <div class="ahero-art">
        <svg class="ribbon" viewBox="0 0 600 600" preserveAspectRatio="none" aria-hidden="true"><path d="M-40 640 C 60 120, 540 120, 640 640"/></svg>
        {phone(0)}
        <figure class="qr"><img src="/assets/qr/{i}.svg" alt="" width="104" height="104" loading="lazy">{t('scan', 'figcaption')}</figure>
      </div>
    </div>
  </section>

  <section class="sec inside">
    <div class="wrap inside-in">
      <div class="duo">{phone(1)}{phone(2, ' low')}</div>
      <div>{t('feat_h2', 'h2')}<ul class="feats">{feats}</ul></div>
    </div>
  </section>

  <section class="sec afaq">
    <div class="wrap faq-in">
      <div class="head">{t('faq_app', 'h2')}</div>
      <div class="qa">{faq_list([(f'{i}_q{n}', f'{i}_a{n}') for n in range(len(a['faq']))])}
        <p class="pvnote"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/></svg><span>{t(i + '_pv')} <a href="https://{i}.wamdarc.com/privacy.html" data-i18n="pv_more">{ar('pv_more')}</a></span></p>
      </div>
    </div>
  </section>

  <section class="sec others">
    <div class="wrap">
      {t('others_h2', 'h2')}
      <div class="orow">{others}</div>
    </div>
  </section>
</main>
'''
    return head(f'/{i}/', f'title_{i}', f'{i}_short', f'og-{i}', ld) + body + footer()

# ---------- جديدنا ----------
def news():
    chips = f'<button class="on" type="button" data-f="all" aria-pressed="true" data-i18n="all">{ar("all")}</button>' + ''.join(
        f'<button type="button" data-f="{a["id"]}" aria-pressed="false" style="--c:{a["color"]}"><img src="/assets/{a["id"]}/icon.webp" alt="" width="22" height="22"><span data-i18n="{a["id"]}_nm">{a["ar"]}</span></button>' for a in APPS)
    out, cur = '', None
    for n, (app, ver, (y, m), items) in enumerate(NEWS):
        if (y, m) != cur:
            if cur: out += '</div>'
            cur = (y, m)
            out += f'<h2 class="mh">{t(f"m{m}")} <span class="ltr">{y}</span></h2><div class="news">'
        lis = ''.join(f'<li data-i18n="n{n}_{j}">{x}</li>' for j, (x, _) in enumerate(items))
        if app == 'all':
            hd = f'<div class="nh"><img src="/assets/favicon.svg?v={V}" alt="" width="40" height="40"><b data-i18n="all_apps">{ar("all_apps")}</b></div>'
            c = '#7B4BF0'
        else:
            a = A[app]; c = a['color']
            hd = f'<a class="nh" href="/{app}/">{icon(a, 40)}<b>{nm(a)}</b></a>'
        vv = f'<span class="ver ltr">v{ver}</span>' if ver else ''
        out += f'<article class="nc" data-app="{app}" style="--c:{c}">{hd}{vv}<ul>{lis}</ul></article>'
    out += '</div>'
    body = f'''{nav()}
<main id="main" class="doc">
  <section class="dhead"><div class="wrap">{t('news_h1', 'h1')}{t('news_sub', 'p')}</div></section>
  <div class="wrap dbody">
    <div class="chips" id="chips" role="group">{chips}</div>
    {out}
  </div>
</main>
'''
    return head('/updates/', 'title_news', 'desc_news') + body + footer()

# ---------- الخصوصية ----------
def privacy():
    apps = ''
    for a in APPS:
        i = a['id']
        ps = ''.join(t(f'pv_{i}_{n}', 'p') for n in (1, 2))
        apps += f'''<section class="pvapp" id="{i}" style="--c:{a['color']}"><h3>{icon(a, 40)}{nm(a)}</h3>{ps}<a class="more" href="https://{i}.wamdarc.com/privacy.html"><span data-i18n="pv_full">{ar('pv_full')}</span> <span class="ltr">{i}.wamdarc.com</span></a></section>'''
    tl = ''.join(f'<li data-i18n="pv_t{n}">{ar(f"pv_t{n}")}</li>' for n in (1, 2, 3, 4))
    body = f'''{nav()}
<main id="main" class="doc">
  <section class="dhead"><div class="wrap narrow">{t('pv_h1', 'h1')}{t('pv_upd', 'p')}</div></section>
  <div class="wrap narrow dbody prose">
    <div class="tldr">{t('pv_tldr', 'h2')}<ul>{tl}</ul></div>
    <section>{t('pv_site_h', 'h2')}{t('pv_site_1', 'p')}{t('pv_site_2', 'p')}{t('pv_site_3', 'p')}</section>
    {apps}
    <section>{t('pv_stats_h', 'h2')}{t('pv_stats_1', 'p')}{t('pv_stats_2', 'p')}</section>
    <section>{t('pv_kids_h', 'h2')}{t('pv_kids_1', 'p')}</section>
    <section>{t('pv_del_h', 'h2')}{t('pv_del_1', 'p')}</section>
    <section>{t('pv_chg_h', 'h2')}{t('pv_chg_1', 'p')}</section>
    <section>{t('pv_ct_h', 'h2')}{t('pv_ct_1', 'p', raw=True)}</section>
  </div>
</main>
'''
    return head('/privacy/', 'title_pv', 'desc_pv') + body + footer()

# ---------- شكرًا و404 ----------
def simple(path, title_k, h_k, p_k, show_apps=False):
    apps = ('<div class="orow mini">' + ''.join(f'<a href="/{a["id"]}/" style="--c:{a["color"]}">{icon(a, 56)}<span class="ot">{nm(a)}</span></a>' for a in APPS) + '</div>') if show_apps else ''
    extra = '<meta name="robots" content="noindex">\n'
    body = f'''{nav()}
<main id="main" class="doc solo">
  <section class="dhead"><div class="wrap">{t(h_k, 'h1')}{t(p_k, 'p')}<p><a class="btn primary" href="/" data-i18n="back_home">{ar('back_home')}</a></p>{apps}</div></section>
</main>
'''
    return head(path, title_k, p_k, extra=extra) + body + footer()

def sitemap():
    urls = ['/'] + [f'/{a["id"]}/' for a in APPS] + ['/updates/', '/privacy/']
    rows = ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{LASTMOD}</lastmod><xhtml:link rel="alternate" hreflang="ar" href="{SITE}{u}"/><xhtml:link rel="alternate" hreflang="en" href="{SITE}{u}?lang=en"/></url>\n' for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{rows}</urlset>\n'

def write(rel, s):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)
    print('✓', rel, len(s.encode()))

if __name__ == '__main__':
    write('index.html', home())
    for a in APPS: write(f'{a["id"]}/index.html', app_page(a))
    write('updates/index.html', news())
    write('privacy/index.html', privacy())
    write('thanks.html', simple('/thanks.html', 'title_th', 'th_h1', 'th_p'))
    write('404.html', simple('/404.html', 'title_404', 'nf_h1', 'nf_p', True))
    write('sitemap.xml', sitemap())
    js = '/* مولّد من build/content.py — لا تعدّله يدويًا */\nwindow.T=' + json.dumps(T, ensure_ascii=False, separators=(',', ':')) + ';\n'
    write('assets/i18n.js', js)
    print(len(T['ar']), 'keys')
