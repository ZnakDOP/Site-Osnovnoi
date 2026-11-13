#!/usr/bin/env python3
"""Рисует линейные иллюстрации техники для фона блока «Рентал» (images/rental/*.svg).

Запуск из корня репозитория:  python3 scripts/gen_rental_art.py
Цвета — акценты сайта (#5eead4 → #a78bfa). Параметры (размеры колец, детали корпуса) правятся прямо здесь.
"""
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "images" / "rental"
OUT.mkdir(parents=True, exist_ok=True)
def f(x): return ('%.2f'%x).rstrip('0').rstrip('.')
HEAD=lambda w,h,extra='': f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="none" stroke-linecap="round" stroke-linejoin="round">
<defs>
<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="{h}"><stop offset="0" stop-color="#5eead4"/><stop offset="1" stop-color="#a78bfa"/></linearGradient>
<radialGradient id="glass" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#5eead4" stop-opacity=".16"/><stop offset=".7" stop-color="#a78bfa" stop-opacity=".05"/><stop offset="1" stop-color="#a78bfa" stop-opacity="0"/></radialGradient>
<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5eead4" stop-opacity=".28"/><stop offset="1" stop-color="#5eead4" stop-opacity="0"/></linearGradient>
{extra}</defs>
'''

# ---------- LENS (front view) ----------
def lens():
    W=H=640; cx=cy=320
    s=[HEAD(W,H)]
    def circ(r,w=1.2,stroke='url(#g)',op=1,dash=None,fill='none'):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{f(r)}" stroke="{stroke}" stroke-width="{w}" opacity="{op}"{d} fill="{fill}"/>')
    # angle scale outside
    for i in range(0,360,5):
        a=math.radians(i); major=i%30==0; mid=i%10==0
        r1=306; r2=318 if major else (313 if mid else 310)
        s.append(f'<line x1="{f(cx+r1*math.cos(a))}" y1="{f(cy+r1*math.sin(a))}" x2="{f(cx+r2*math.cos(a))}" y2="{f(cy+r2*math.sin(a))}" stroke="url(#g)" stroke-width="{1.4 if major else 0.8}" opacity="{.9 if major else .5}"/>')
    circ(300,1.6); circ(292,.8,'#fff',.25)
    circ(278,15,'url(#g)',.28,'1.4 8.6')          # knurled grip
    circ(262,1.2); circ(256,.7,'#fff',.2)
    circ(238,9,'url(#g)',.35,'1 11.6')               # focus scale ticks
    for i in range(0,360,15):                         # long marks
        a=math.radians(i)
        s.append(f'<line x1="{f(cx+228*math.cos(a))}" y1="{f(cy+228*math.sin(a))}" x2="{f(cx+246*math.cos(a))}" y2="{f(cy+246*math.sin(a))}" stroke="url(#g)" stroke-width="1.2" opacity=".7"/>')
    circ(218,1.4); circ(206,.8,'#fff',.22)
    circ(188,1.2,'url(#g)',.9); circ(176,.8,'#fff',.2)
    circ(168,0,'none',1,None,'url(#glass)')
    circ(150,1,'url(#g)',.75); circ(128,.8,'url(#g)',.55); circ(108,.8,'#fff',.2)
    # reflections arcs
    for r,a0,a1,w,o in [(160,200,250,2.2,.8),(160,262,276,1.2,.6),(138,18,70,1.6,.6),(118,215,235,1.2,.5)]:
        x0,y0=cx+r*math.cos(math.radians(a0)),cy+r*math.sin(math.radians(a0)); x1,y1=cx+r*math.cos(math.radians(a1)),cy+r*math.sin(math.radians(a1))
        s.append(f'<path d="M{f(x0)} {f(y0)} A{r} {r} 0 0 1 {f(x1)} {f(y1)}" stroke="#fff" stroke-width="{w}" opacity="{o*.6}"/>')
    # iris blades
    n=9; ra=34; ro=100
    pts=[(cx+ra*math.cos(math.radians(360*i/n-90)),cy+ra*math.sin(math.radians(360*i/n-90))) for i in range(n)]
    s.append('<path d="M'+' L'.join(f'{f(x)} {f(y)}' for x,y in pts)+' Z" stroke="url(#g)" stroke-width="1.2" fill="#5eead4" fill-opacity=".06"/>')
    for i in range(n):
        a=math.radians(360*i/n-90); ao=a+math.radians(46)
        x0,y0=pts[i]; x1,y1=cx+ro*math.cos(ao),cy+ro*math.sin(ao)
        # blade edge: from aperture vertex tangentially out to rim, then arc back along rim
        a2=a+math.radians(46+22)
        x2,y2=cx+ro*math.cos(a2),cy+ro*math.sin(a2)
        s.append(f'<path d="M{f(x0)} {f(y0)} L{f(x1)} {f(y1)} A{ro} {ro} 0 0 1 {f(x2)} {f(y2)}" stroke="url(#g)" stroke-width="1" opacity=".7"/>')
    circ(ro,1.2,'url(#g)',.8)
    circ(14,1.2,'#fff',.35)
    # cross hairs
    for dx,dy in [(1,0),(0,1)]:
        s.append(f'<line x1="{cx-dx*324}" y1="{cy-dy*324}" x2="{cx-dx*196}" y2="{cy-dy*196}" stroke="#fff" stroke-width=".6" opacity=".25" stroke-dasharray="2 5"/><line x1="{cx+dx*196}" y1="{cy+dy*196}" x2="{cx+dx*324}" y2="{cy+dy*324}" stroke="#fff" stroke-width=".6" opacity=".25" stroke-dasharray="2 5"/>')
    s.append('</svg>')
    return '\n'.join(s)

open(OUT/'lens.svg','w').write(lens())

# ---------- CAMERA: ARRI Alexa Mini (side view) ----------
def camera():
    W,H=900,520
    o=[HEAD(W,H)]
    G='url(#g)'
    def rect(x,y,w,h,rx=0,st=G,w_=1.3,op=1,fill=None):
        fl=f' fill="#5eead4" fill-opacity="{fill}"' if fill else ' fill="none"'
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" stroke="{st}" stroke-width="{w_}" opacity="{op}"{fl}/>')
    def line(x1,y1,x2,y2,st=G,w_=1,op=1,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        o.append(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{st}" stroke-width="{w_}" opacity="{op}"{d}/>')
    def circ(cx,cy,r,st=G,w_=1.2,op=1,fill=None):
        fl=f' fill="#5eead4" fill-opacity="{fill}"' if fill else ' fill="none"'
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" stroke="{st}" stroke-width="{w_}" opacity="{op}"{fl}/>')
    def path(d,st=G,w_=1.3,op=1,fill=None):
        fl=f' fill="#5eead4" fill-opacity="{fill}"' if fill else ' fill="none"'
        o.append(f'<path d="{d}" stroke="{st}" stroke-width="{w_}" opacity="{op}"{fl}/>')
    AX=257  # optical axis
    # ---- body (Alexa Mini: compact slab with chamfered shoulders)
    path('M404 172 H628 Q642 172 642 186 V328 Q642 342 628 342 H404 Q390 342 390 328 V186 Q390 172 404 172 Z',G,1.7,1,.05)
    path('M412 184 H620 Q630 184 630 194 V320 Q630 330 620 330 H412 Q402 330 402 320 V194 Q402 184 412 184 Z','#fff',.6,.2)
    # top plate: threaded holes
    for x in range(424,624,22): circ(x,178,2.4,'#fff',.8,.45)
    # front plate + PL mount
    rect(376,192,16,130,3,G,1.4)
    rect(350,215,28,84,5,G,1.5)
    for dy in (-6,6):
        line(354,AX+dy*0+ (-34 if dy<0 else 34),374,AX+(-34 if dy<0 else 34),'#fff',.8,.4)
    circ(364,AX,26,G,.9,.5)
    # film plane mark
    circ(470,226,7,'#fff',1,.6); line(459,226,481,226,'#fff',1,.6); line(470,172,470,342,'#fff',.6,.22,'2 6')
    # side display + buttons
    rect(552,196,64,38,6,G,1.3,1,.07); line(560,208,606,208,'#fff',.7,.35); line(560,218,590,218,'#fff',.7,.25)
    for x in (566,588,610): circ(x,252,4.5,G,1.1,.8)
    circ(610,252,2,'#5eead4',1,.9,.6)
    # vents
    for i in range(7): line(418+i*11,288,432+i*11,322,G,.9,.38)
    # connectors (rear lower)
    for cx in (584,614): circ(cx,300,10,G,1.3); circ(cx,300,4.5,'#fff',.8,.45)
    # ---- rear: battery plate + EVF
    rect(642,190,52,138,8,G,1.5)
    path('M656 232 L668 252 L680 232','#fff',1.2,.5)
    line(642,218,694,218,'#fff',.6,.25); line(642,300,694,300,'#fff',.6,.25)
    line(668,190,684,150,G,1.4); line(668,196,690,160,G,1.1)         # EVF arm
    rect(676,112,82,50,9,G,1.5,1,.05); rect(758,122,26,30,6,G,1.3); line(686,128,748,128,'#fff',.6,.3)
    # ---- top handle
    rect(430,114,180,20,10,G,1.5); line(462,134,462,172,G,1.3); line(578,134,578,172,G,1.3)
    for x in range(446,596,10): line(x,119,x,129,G,.7,.38)
    # ---- lens (cine prime): rear barrel -> iris ring -> focus ring -> front
    rect(290,205,62,104,6,G,1.4)
    rect(246,198,46,118,7,G,1.5)                                   # iris ring with gears
    for x in range(250,290,5): line(x,200,x,314,G,.7,.4)
    rect(204,204,44,106,6,G,1.3)
    rect(138,194,68,126,9,G,1.6)                                   # focus ring with gears
    for x in range(143,203,5): line(x,197,x,317,G,.8,.42)
    rect(108,203,32,108,6,G,1.4)
    rect(98,208,12,98,4,G,1.3)
    for x in range(214,244,6): line(x,206,x,214,'#fff',.8,.55)     # distance scale ticks
    line(212,214,244,214,'#fff',.7,.35)
    circ(104,AX,38,G,1,.45); circ(104,AX,22,'#fff',.7,.25)
    # ---- matte box
    path('M98 212 L66 188 L66 326 L98 302','' if False else G,1.4,1,.04)
    rect(34,166,34,182,5,G,1.5)
    line(34,166,20,146,G,1.2); line(68,166,82,146,G,1.2); line(20,146,82,146,G,1.3)     # top flag
    line(34,348,20,368,G,1.2); line(68,348,82,368,G,1.2); line(20,368,82,368,G,1.3)     # bottom flag
    for y in range(180,336,12): line(42,y,60,y,G,.6,.3)
    # ---- rods + lens support + follow focus
    for y in (370,380): line(120,y,520,y,G,1.3)
    rect(304,306,22,76,4,G,1.4); circ(315,344,5,'#fff',.8,.5)       # lens support
    rect(222,348,44,40,7,G,1.4); circ(244,368,12,G,1.2); circ(244,368,4,'#fff',.8,.4)  # follow focus
    for i in range(12):
        a=math.radians(i*30); line(244+14*math.cos(a),368+14*math.sin(a),244+18*math.cos(a),368+18*math.sin(a),G,.8,.55)
    # ---- baseplate / bridge plate
    rect(372,342,240,22,5,G,1.5,1,.05); rect(404,364,150,14,4,G,1.3)
    rect(520,364,22,22,4,G,1.2); line(520,375,542,375,'#fff',.6,.3)
    # ---- dimension line
    line(20,446,798,446,'#fff',.7,.3)
    for x in (20,98,390,642,798): line(x,438,x,454,'#fff',.7,.35)
    o.append('</svg>')
    return '\n'.join(o)

# ---------- LIGHT (side view) ----------
def light():
    W,H=640,780
    o=[HEAD(W,H,'<linearGradient id="beam2" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#5eead4" stop-opacity=".30"/><stop offset="1" stop-color="#5eead4" stop-opacity="0"/></linearGradient>')]
    G='url(#g)'
    def line(x1,y1,x2,y2,st=G,w_=1,op=1,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{st}" stroke-width="{w_}" opacity="{op}"{d}/>')
    def circ(cx,cy,r,st=G,w_=1.2,op=1,fill='none'):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{st}" stroke-width="{w_}" opacity="{op}" fill="{fill}"/>')
    def rect(x,y,w,h,rx=0,st=G,w_=1.3,op=1,fill='none'):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" stroke="{st}" stroke-width="{w_}" opacity="{op}" fill="{fill}"/>')
    # beam
    o.append('<path d="M0 -20 L238 60 L238 336 L0 420 Z" fill="url(#beam2)"/>')
    for k in (0.2,0.5,0.8):
        y0=60+(336-60)*k; y1=-20+(420+20)*k
        line(0,y1,238,y0,'#5eead4',.6,.22,'3 8')
    # reflector dish
    o.append('<ellipse cx="238" cy="198" rx="28" ry="138" stroke="url(#g)" stroke-width="1.6" fill="#5eead4" fill-opacity=".05"/>')
    o.append('<ellipse cx="238" cy="198" rx="20" ry="118" stroke="#fff" stroke-width=".7" opacity=".25"/>')
    line(238,60,370,128); line(238,336,370,268)
    for k in (0.25,0.5,0.75):
        y=60+(336-60)*k; y2=128+(268-128)*k
        line(238,y,370,y2,'#fff',.6,.18)
    # head housing + fins
    rect(370,120,150,156,14,G,1.6,1,'#5eead4'); o[-1]=o[-1].replace('fill="#5eead4"','fill="#5eead4" fill-opacity=".05"')
    for x in range(388,508,10): line(x,134,x,262,G,.9,.38)
    rect(520,150,26,96,6,G,1.3)                       # rear cap
    rect(496,276,46,20,5,G,1.2)                       # controller notch
    # yoke + knob
    o.append('<path d="M445 276 L445 306 M445 306 H345" stroke="url(#g)" stroke-width="1.4"/>')
    circ(445,306,16,G,1.4); circ(445,306,6,'#fff',.8,.45)
    # stand column
    rect(437,322,16,190,3,G,1.3)
    rect(433,512,24,130,4,G,1.3); line(433,566,457,566,'#fff',.6,.3); line(433,600,457,600,'#fff',.6,.3)
    circ(445,512,9,G,1.2,.9); circ(445,512,3.5,'#fff',.8,.4)
    # legs
    o.append('<path d="M445 642 L300 742 M445 642 L590 742 M445 642 L445 752" stroke="url(#g)" stroke-width="1.4"/>')
    for x,y in ((300,742),(590,742),(445,752)): circ(x,y,6,G,1.2)
    line(380,700,510,700,'#fff',.6,.25)
    # cable
    o.append('<path d="M533 246 C 600 250, 610 400, 560 520 S 520 700, 470 742" stroke="#fff" stroke-width="1" opacity=".3" stroke-dasharray="1.5 5"/>')
    o.append('</svg>')
    return '\n'.join(o)

open(OUT/'lens.svg','w').write(lens())
open(OUT/'camera.svg','w').write(camera())
open(OUT/'light.svg','w').write(light())
print('ok')
