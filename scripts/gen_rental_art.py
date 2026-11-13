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
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5eead4"/><stop offset="1" stop-color="#a78bfa"/></linearGradient>
<linearGradient id="gv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5eead4"/><stop offset="1" stop-color="#a78bfa"/></linearGradient>
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

# ---------- CAMERA (side view) ----------
def camera():
    W,H=900,520
    o=[HEAD(W,H)]
    G='url(#g)'
    def rect(x,y,w,h,rx=0,st=G,w_=1.3,op=1,fill='none'):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" stroke="{st}" stroke-width="{w_}" opacity="{op}" fill="{fill}"/>')
    def line(x1,y1,x2,y2,st=G,w_=1,op=1,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{st}" stroke-width="{w_}" opacity="{op}"{d}/>')
    def circ(cx,cy,r,st=G,w_=1.2,op=1,fill='none'):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{st}" stroke-width="{w_}" opacity="{op}" fill="{fill}"/>')
    cy=255
    # body
    rect(330,150,310,210,20,G,1.6,1,'#5eead4'); o[-1]=o[-1].replace('fill="#5eead4"','fill="#5eead4" fill-opacity=".05"')
    rect(346,166,278,178,12,'#fff',.6,.2)
    # mount + lens
    rect(298,190,34,130,6,G,1.4)
    rect(192,178,108,154,10,G,1.4); line(192,214,300,214,'#fff',.6,.25); line(192,296,300,296,'#fff',.6,.25)
    rect(128,168,66,174,9,G,1.6)                     # focus ring
    for x in range(136,190,6): line(x,176,x,334,G,.8,.45)
    rect(94,186,36,138,6,G,1.4)
    o.append(f'<path d="M94 192 L40 148 L40 362 L94 318" stroke="{G}" stroke-width="1.4" fill="none"/>')   # hood
    line(40,148,40,362,G,1.4)
    for y in range(160,356,14): line(52,y,86,y,G,.6,.3)
    for x in range(204,290,10): line(x,184,x,190,'#fff',.8,.5)    # scale ticks
    circ(110,255,52,G,.9,.55); circ(110,255,34,'#fff',.7,.25); circ(110,255,16,G,.9,.6)  # front element hint
    # top handle
    rect(392,98,190,22,11,G,1.4); line(424,120,424,150,G,1.2); line(552,120,552,150,G,1.2)
    for x in range(416,566,10): line(x,104,x,114,G,.7,.4)
    # EVF
    rect(594,108,86,54,10,G,1.4); rect(680,118,22,34,6,G,1.2); line(604,126,670,126,'#fff',.6,.25)
    # sensor-plane mark
    circ(470,136,7,'#fff',1,.55); line(460,136,480,136,'#fff',1,.55); line(470,150,470,372,'#fff',.6,.25,'2 6')
    # controls
    circ(592,212,15,G,1.3); circ(592,212,8,'#fff',.8,.4); 
    for a in range(0,360,45):
        import math as m
        line(592+15*m.cos(m.radians(a)),212+15*m.sin(m.radians(a)),592+19*m.cos(m.radians(a)),212+19*m.sin(m.radians(a)),G,.8,.6)
    circ(556,190,6,'#5eead4',1.2,.9,'#5eead4'); o[-1]=o[-1].replace('fill="#5eead4"','fill="#5eead4" fill-opacity=".35"')
    circ(520,196,4,G,1,.6)
    for y in range(284,336,8): line(372,y,492,y,G,.8,.4)
    # rear battery plate
    rect(640,176,66,158,10,G,1.4); line(640,205,706,205,'#fff',.6,.25); line(640,305,706,305,'#fff',.6,.25)
    o.append(f'<path d="M656 240 L673 262 L690 240" stroke="{G}" stroke-width="1.2"/>')
    # cage rails
    line(250,392,724,392,G,1.3); line(250,404,724,404,G,1.3)
    for x in (330,640): line(x,360,x,412,G,1.2)
    for x in (250,724):
        circ(x,392,3,G,1,.8); circ(x,404,3,G,1,.8)
    # dimension line
    line(40,452,706,452,'#fff',.7,.3); line(40,444,40,460,'#fff',.7,.35); line(706,444,706,460,'#fff',.7,.35)
    line(330,444,330,460,'#fff',.7,.25); line(640,444,640,460,'#fff',.7,.25)
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
