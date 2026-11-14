# Translate built HTML by text node, keeping layout and links.
# Run with cwd = <workdir>/build.
#   python3 i18n.py extract            -> ../i18n/en.json (every translatable string, deduplicated)
#   python3 i18n.py apply te hi ...    -> <name>_<lang>.html using ../i18n/<lang>.json ({english: translation})
# Supported scripts: te (Telugu), hi (Hindi), kn (Kannada), ta (Tamil); fonts in fonts/indic.
import json, re, sys, os
from bs4 import BeautifulSoup, NavigableString, Comment, Doctype
FILES=["brochure","poster","itinerary"]
I18N="../i18n"
KEEP=re.compile(r"^[\s\d:–\-—·/.,+%₹()|→⇄↗&×\"'’]*$")
NOTR=re.compile(r"(www\.|@|https?:|\.com|\.org|^\s*[\d\s]+\s*$|^\s*\d{2}:\d{2})")
def nodes(soup):
    for t in soup.find_all(string=True):
        if isinstance(t,(Comment,Doctype)) or t.parent.name in ("style","script"): continue
        s=t.strip()
        if not s or KEEP.match(s) or NOTR.search(s): continue
        yield t,s
def extract():
    seen={}
    for f in FILES:
        if not os.path.exists(f"{f}.html"): continue
        soup=BeautifulSoup(open(f"{f}.html"),"html.parser")
        for t,s in nodes(soup): seen.setdefault(s,f)
    os.makedirs(I18N,exist_ok=True)
    json.dump(list(seen),open(f"{I18N}/en.json","w"),ensure_ascii=False,indent=0)
    print(len(seen),"strings",sum(len(s.split()) for s in seen),"words")
RANGES={"te":"U+0C00-0C7F,U+0964-0965,U+200C-200D,U+25CC","hi":"U+0900-097F,U+A8E0-A8FF,U+1CD0-1CFF,U+200C-200D,U+25CC","kn":"U+0C80-0CFF,U+0964-0965,U+200C-200D,U+25CC","ta":"U+0B80-0BFF,U+0964-0965,U+200C-200D,U+25CC"}
SCRIPT={"te":"telugu","hi":"devanagari","kn":"kannada","ta":"tamil"}
def fontcss(lang,prefix):
    out=[]
    for fam,kind in (("Poppins","sans"),("Montserrat","sans"),("Playfair Display","serif"),("Great Vibes","serif"),("sans-serif-indic","sans")):
        for w,src in ((400,400),(500,400),(600,600),(700,700),(800,800),(900,800)):
            for style in ("normal","italic"):
                out.append(f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{w};src:url({prefix}fonts/indic/noto-{kind}-{SCRIPT[lang]}-{src}.woff2) format('woff2');unicode-range:{RANGES[lang]}}}")
    out.append("body{font-family:Poppins,'sans-serif-indic',sans-serif}*{letter-spacing:0 !important}")
    return "\n".join(out)
ZOOMFIT="""window.__fit=(window.__fit||document.fonts.ready).then(()=>{document.querySelectorAll('.page .body').forEach(b=>{
 let z=1;const over=()=>b.scrollHeight>b.clientHeight+1;
 while(over()&&z>0.78){z-=0.02;b.style.zoom=z;}
 if(over()) document.title+=' OVERFLOW';});});"""
POSTERFIT="""window.__fit=document.fonts.ready.then(()=>{
 const q=s=>document.querySelector(s), r=e=>e.getBoundingClientRect();
 const shrink=(el,limit,min)=>{let f=parseFloat(getComputedStyle(el).fontSize);while(limit()&&f>min){f-=1;el.style.fontSize=f+'px';}};
 const t2=q('.po .t2'); t2.style.marginTop='4px'; t2.style.lineHeight='1.25';
 [q('.po h1'),t2].forEach(el=>{el.style.whiteSpace='nowrap';el.style.display='table';el.style.margin=(el===t2?'4px':'8px')+' auto 0';shrink(el,()=>r(el).width>1000,30);});
 const bar=q('.po .bar'),bk=q('.po .book'),ph=q('.po .ph'); ph.style.whiteSpace='nowrap';
 let g=0; const fs=e=>parseFloat(getComputedStyle(e).fontSize); const web=q('.po .web'); const tight=()=>bar.scrollWidth>bar.clientWidth+1||r(web).right>1080-34; while(tight()&&g++<60){ if(fs(bk)>19) bk.style.fontSize=(fs(bk)-1)+'px'; else if(fs(ph)>36) ph.style.fontSize=(fs(ph)-1)+'px'; else break; }
 const hl=q('.po .hl'),ex=q('.po .ex'); let f=19;
 while(r(hl).bottom>r(ex).top-6&&f>13){f-=0.5;hl.querySelectorAll('div').forEach(d=>d.style.fontSize=f+'px');}
});"""
def apply(lang):
    tr=json.load(open(f"{I18N}/{lang}.json"))
    missing=set()
    for f in FILES:
        if not os.path.exists(f"{f}.html"): continue
        soup=BeautifulSoup(open(f"{f}.html"),"html.parser")
        for t,s in list(nodes(soup)):
            if s in tr and tr[s]:
                lead=t[:len(t)-len(t.lstrip())]; trail=t[len(t.rstrip()):]
                t.replace_with(NavigableString(lead+tr[s]+trail))
            else: missing.add(s)
        if soup.html: soup.html["lang"]={"te":"te","hi":"hi","kn":"kn","ta":"ta"}[lang]
        st=soup.new_tag("style"); st.string=fontcss(lang,"")
        soup.head.append(st)
        if soup.body and soup.select(".po"):
            sc=soup.new_tag("script"); sc.string=POSTERFIT; soup.body.append(sc)
        if soup.body and soup.select(".page .body"):
            sc=soup.new_tag("script"); sc.string=ZOOMFIT; soup.body.append(sc)
        open(f"{f}_{lang}.html","w").write(str(soup))
    print(lang,"missing",len(missing)); 
    if missing: json.dump(sorted(missing),open(f"{I18N}/missing_{lang}.json","w"),ensure_ascii=False,indent=0)
if __name__=="__main__":
    if sys.argv[1]=="extract": extract()
    else:
        for l in sys.argv[2:]: apply(l)
