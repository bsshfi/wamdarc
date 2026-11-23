# -*- coding: utf-8 -*-
"""صور المشاركة (1200×630) لـ wamdarc.com — تحتاج Playwright وخادم محلي للموقع:
   python3 -m http.server 8201 &   ثم   python3 build/og.py 8201"""
import sys, os, asyncio
sys.path.insert(0, os.path.dirname(__file__))
from content import APPS
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = sys.argv[1] if len(sys.argv) > 1 else '8201'
BASE = f'http://127.0.0.1:{PORT}'
CSS = '''*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1200px;height:630px;overflow:hidden}
body{font-family:'Readex Pro',sans-serif;color:#F3F0FC;background:radial-gradient(90% 80% at 30% 110%,#2A1A78 0%,rgba(42,26,120,0) 62%),linear-gradient(180deg,#17104A 0%,#120C33 100%);position:relative}
.sky{position:absolute;inset:0;opacity:.5;background-image:radial-gradient(1.2px 1.2px at 12% 18%,#fff,transparent),radial-gradient(1px 1px at 26% 62%,#fff,transparent),radial-gradient(1.6px 1.6px at 38% 28%,#fff,transparent),radial-gradient(1px 1px at 52% 12%,#fff,transparent),radial-gradient(1px 1px at 64% 44%,#fff,transparent),radial-gradient(1.6px 1.6px at 77% 20%,#fff,transparent),radial-gradient(1px 1px at 88% 58%,#fff,transparent),radial-gradient(1px 1px at 92% 8%,#fff,transparent),radial-gradient(1px 1px at 6% 46%,#fff,transparent)}
.logo{position:absolute;top:44px;right:56px;height:38px}
.dom{font-family:Montserrat,sans-serif;font-weight:500;letter-spacing:.2em;font-size:19px;color:#AAA3D0}
.nm{display:flex;align-items:baseline;gap:18px;direction:rtl}
.nm b{font-weight:600}
.nm i{font-style:normal;font-weight:300;color:rgba(196,182,255,.35)}
.nm span{font-family:Montserrat,sans-serif;font-weight:600;letter-spacing:.12em}
'''

def page(body, extra=''):
    return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@300;400;500;600&family=Montserrat:wght@500;600&display=swap" rel="stylesheet">
<style>{CSS}{extra}</style></head><body><div class="sky"></div>
<img class="logo" src="{BASE}/assets/logo-horizontal-on-dark.svg" alt="">{body}</body></html>'''

def app_card(a):
    c = a['color']; i = a['id']; s = a['shots']
    extra = f'''.arc{{position:absolute;left:-80px;bottom:-250px;width:760px;height:560px}}
.arc path{{fill:none;stroke:{c};stroke-width:3;filter:drop-shadow(0 0 16px {c})}}
.glow{{position:absolute;left:40px;bottom:-120px;width:560px;height:420px;border-radius:50%;background:radial-gradient(closest-side,{c}55,transparent)}}
.ph{{position:absolute;width:210px;border-radius:30px;border:7px solid #2A2160;background:#2A2160;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.45)}}
.ph img{{width:100%;display:block;border-radius:23px}}
.p1{{left:250px;top:120px}} .p2{{left:70px;top:190px;opacity:.96}}
.txt{{position:absolute;right:56px;top:150px;width:560px;display:flex;flex-direction:column;align-items:flex-start;gap:16px}}
.ic{{width:104px;height:104px;border-radius:28px;box-shadow:0 16px 36px {c}66}}
.nm{{font-size:78px;line-height:1.1}} .nm span{{font-size:40px;color:color-mix(in srgb,{c} 65%,#fff)}}
.tag{{font-size:34px;font-weight:500;line-height:1.4}}
.dom{{margin-top:14px}}'''
    body = f'''<div class="glow"></div><svg class="arc" viewBox="0 0 760 560"><path d="M20 560 C 120 60, 640 60, 740 560"/></svg>
<div class="ph p2"><img src="{BASE}/assets/{i}/{s[1][0]}.webp"></div><div class="ph p1"><img src="{BASE}/assets/{i}/{s[0][0]}.webp"></div>
<div class="txt"><img class="ic" src="{BASE}/assets/{i}/icon.webp"><div class="nm"><b>{a['ar']}</b><i>|</i><span>{a['en']}</span></div>
<div class="tag">{a['tag'][0]}</div><div class="dom">{i.upper()}.WAMDARC.COM</div></div>'''
    return page(body, extra)

def home_card():
    stops = ''.join(f'<img class="s s{n}" src="{BASE}/assets/{a["id"]}/icon.webp">' for n, a in enumerate(APPS))
    extra = '''.arc{position:absolute;left:0;right:0;bottom:-40px;width:1200px;height:520px}
.arc .h{fill:none;stroke:#7B4BF0;stroke-width:44;opacity:.12}.arc .l{fill:none;stroke:url(#g);stroke-width:4;stroke-linecap:round}
.s{position:absolute;width:92px;height:92px;border-radius:26px;box-shadow:0 14px 30px rgba(0,0,0,.4);transform:translate(-50%,-50%)}
.s0{left:1092px;top:420px}.s1{left:1010px;top:262px}.s2{left:880px;top:168px}.s3{left:320px;top:168px}.s4{left:190px;top:262px}.s5{left:108px;top:420px}
.spark{position:absolute;left:600px;top:126px;width:18px;height:18px;margin:-9px;border-radius:50%;background:#FF8A2A;box-shadow:0 0 0 8px rgba(255,138,42,.22),0 0 34px 8px rgba(255,138,42,.7)}
.txt{position:absolute;left:0;right:0;top:220px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:14px}
h1{font-weight:600;font-size:64px;line-height:1.2}
.logo{right:auto;left:50%;transform:translateX(-50%);top:40px}'''
    body = f'''<svg class="arc" viewBox="0 0 1200 520"><defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#6A3DE8"/><stop offset=".55" stop-color="#9B52D8"/><stop offset="1" stop-color="#FF8A2A"/></linearGradient></defs>
<path class="h" d="M40 600 C 190 -20, 1010 -20, 1160 600"/><path class="l" d="M40 600 C 190 -20, 1010 -20, 1160 600"/></svg><i class="spark"></i>{stops}
<div class="txt"><h1>تطبيقات صغيرة<br>تخدم يومك وعائلتك</h1><div class="dom">WAMDARC.COM</div></div>'''
    return page(body, extra)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'],
                                    proxy={'server': 'http://127.0.0.1:37657', 'bypass': '127.0.0.1,localhost'})
        pg = await b.new_page(viewport={'width': 1200, 'height': 630})
        jobs = [('og-image', home_card())] + [(f'og-{a["id"]}', app_card(a)) for a in APPS]
        for name, h in jobs:
            await pg.set_content(h, wait_until='networkidle'); await pg.wait_for_timeout(500)
            await pg.screenshot(path=os.path.join(ROOT, 'assets', name + '.png'))
            print('✓', name)
        await b.close()
asyncio.run(main())
