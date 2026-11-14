# Poster (1080x1350, WhatsApp/print). Usage (cwd = <workdir>/build): python3 poster.py <package.py>
import json, html, sys
from common import *
PK=load_pkg(sys.argv[1] if len(sys.argv)>1 else None)
IMG=load_img(PK)
CSS=open("style.css").read()+"""
html,body{background:#000}
.po{width:1080px;height:1350px;position:relative;overflow:hidden;background:var(--plum3);color:#fff;font-family:Poppins}
.po .bg{position:absolute;left:0;right:0;top:0;height:900px}
.po .bg img{width:100%;height:100%;object-fit:cover}
.po .sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(42,13,61,.78) 0%,rgba(42,13,61,.2) 34%,rgba(42,13,61,.1) 48%,rgba(42,13,61,.9) 64%,var(--plum3) 70%)}
.po .top{position:absolute;top:28px;left:36px;right:36px;display:flex;justify-content:space-between;align-items:center}
.po .lg{background:#fff;border-radius:16px;padding:10px 16px}.po .lg img{height:74px;display:block}
.po .seal{height:96px;border-radius:50%;box-shadow:0 0 0 5px #fff}
.po .tt{position:absolute;top:150px;left:0;right:0;text-align:center;text-shadow:0 4px 18px rgba(0,0,0,.6)}
.po .kick{display:inline-flex;align-items:center;gap:12px;font-family:Montserrat;font-weight:800;letter-spacing:3px;text-transform:uppercase;font-size:24px;color:#fff;background:linear-gradient(90deg,var(--coral),var(--orange));border-radius:40px;padding:8px 26px;text-shadow:none;box-shadow:0 4px 14px rgba(0,0,0,.4)}
.po .kick .hico{width:44px;height:28px;fill:#fff}
.po h1{font-size:104px;line-height:1;margin-top:8px;font-weight:800}
.po .t2{font-family:'Great Vibes';font-size:84px;color:var(--gold2);margin-top:-12px}
.po .with{display:inline-block;margin-top:6px;background:linear-gradient(90deg,var(--gold),var(--gold2));color:var(--plum3);border-radius:40px;padding:9px 28px;font-family:Montserrat;font-weight:800;font-size:22px;text-shadow:none}
.po .circ{position:absolute;width:190px;height:190px;border-radius:50%;overflow:hidden;border:7px solid #fff;box-shadow:0 8px 24px rgba(0,0,0,.5);top:500px}
.po .circ img{width:100%;height:100%;object-fit:cover}
.po .when{position:absolute;top:712px;left:0;right:0;text-align:center}
.po .dates{display:inline-block;background:#fff;color:var(--plum3);border-radius:14px;padding:10px 30px;font-family:Montserrat;font-weight:800;font-size:38px;letter-spacing:1px}
.po .dur{display:inline-block;margin-left:14px;background:linear-gradient(90deg,var(--coral),var(--orange));border-radius:40px;padding:12px 30px;font-family:Montserrat;font-weight:800;font-size:30px;vertical-align:middle}
.po .route{font-family:'Playfair Display';color:var(--gold2);font-size:25px;margin-top:8px;padding:0 40px}
.po .price{display:inline-block;margin-top:12px;background:linear-gradient(90deg,var(--gold),var(--gold2));color:var(--plum3);border-radius:14px;padding:6px 26px;font-family:Montserrat;font-weight:800;font-size:40px;text-shadow:none;vertical-align:middle}
.po .price small{font-size:20px;font-weight:700}
.po .reg{display:inline-block;margin-top:12px;margin-left:12px;vertical-align:middle;font-size:18px !important;line-height:1.15;background:var(--coral);border-radius:10px;padding:6px 20px;font-family:Montserrat;font-weight:800;font-size:22px}
.po .hl{position:absolute;top:948px;left:60px;right:60px;display:grid;grid-template-columns:1fr 1fr;gap:10px 30px}
.po .hl div{font-size:19px;line-height:1.15;padding-left:32px;position:relative}
.po .hl div:before{content:"\\2605";position:absolute;left:0;color:var(--orange);font-size:24px}
.po .ex{position:absolute;top:1106px;left:40px;right:40px;display:grid;grid-template-columns:repeat(6,1fr);gap:10px}
.po .ex div{background:rgba(255,255,255,.1);border:1px solid rgba(246,213,139,.4);border-radius:14px;text-align:center;padding:10px 4px;font-family:Montserrat;font-size:14px;font-weight:600;line-height:1.2}
.po .ex .i{width:46px;height:46px;border-radius:50%;background:#fff;margin:0 auto 6px;display:flex;align-items:center;justify-content:center}
.po .ex svg{width:28px;height:28px}
.po .bar{position:absolute;left:0;right:0;bottom:0;height:118px;line-height:1;background:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 36px}
.po .book{background:linear-gradient(90deg,var(--coral),var(--orange));color:#fff;border-radius:40px;padding:14px 26px;font-family:Montserrat;font-weight:800;font-size:26px;white-space:nowrap}
.po .ph{font-family:Montserrat;font-weight:800;font-size:52px;color:var(--plum)}
.po .bar>span{display:flex;flex-direction:column;justify-content:center}
.po .book,.po .ph{height:auto}
.po .web{text-align:right;color:var(--plum);font-family:Montserrat;font-weight:600;font-size:19px;line-height:1.45}
"""
def poster(pk):
    c=pk["poster"]
    circ="".join(f'<div class="circ" style="left:{x}px"><img src="{IMG[k]["src"]}"></div>' for k,x in zip(c["circ"],[70,445,820]))
    hl="".join(f"<div>{E(h)}</div>" for h in c["hl"])
    ex="".join(f'<div><div class="i">{ICONS[i]}</div>{E(x)}</div>' for i,x in enumerate(EXPERIENCES))
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="po">
<div class="bg"><img src="{IMG[c["hero"]]["src"]}" style="object-position:{c["pos"]}"></div><div class="sh"></div>
<div class="top"><div class="lg"><img src="brand/hkgt_logo.png"></div><img class="seal" src="brand/seal.png"><div class="lg"><img src="brand/pk_logo.png"></div></div>
<div class="tt"><div class="kick">{HELI if pk["show_heli_icon"] else ""}{E(c["kicker"])}</div><h1>{E(pk["title"])}</h1><div class="t2">{E(pk["title2"])}</div><div class="with">{E(WITH_LINE)}</div></div>
{circ}
<div class="when"><span class="dates">{E(pk["dates"])}</span><span class="dur">{E(pk["duration"])}</span><div class="route">{E(pk["tagline"])}</div><div><span class="price">{E(pk["price"])} <small>{E(c["price_small"])}</small></span>{f'<span class="reg">{c["reg"]}</span>' if c["reg"] else ""}</div></div>
<div class="hl">{hl}</div>
<div class="ex">{ex}</div>
<div class="bar"><span class="book">{E(CTA)}</span><span class="ph" style="flex-direction:row;align-items:center;gap:14px">{PHONE_SVG.format(w="46",c="#3A1452",s="")}{CONTACT["phone"]}</span><span class="web">{CONTACT["web1"]}<br>{CONTACT["web2"]}<br>{CONTACT["social"]}</span></div>
</div></body></html>'''
if __name__=="__main__":
    open("poster.html","w").write(poster(PK)); print("wrote poster.html")
