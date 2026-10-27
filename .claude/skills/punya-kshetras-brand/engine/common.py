# Load a package spec (package.py in a work folder) and fill brand defaults.
# Scripts run with cwd = <workdir>/build; the package path comes from argv[1] or $PKG.
import json, os, sys, html, importlib.util, datetime
from brand import *
E=html.escape

def load_pkg(path=None):
    path=os.path.abspath(path or os.environ["PKG"])
    spec=importlib.util.spec_from_file_location("package",path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    pk=dict(mod.PKG); wd=os.path.dirname(path); pk["_dir"]=wd
    d=pk.setdefault
    d("gst_note","+ 5% GST"); d("price_note","per person · all-inclusive · excluding flight charges")
    d("seats_note","Limited seats."); d("cover_note",f"Registrations close {pk['reg_close']}" if pk.get("reg_close") else "")
    d("reg_short",pk.get("reg_close",""))
    d("kicker","Premium Pilgrimage"); d("show_heli_icon",False); d("hero_pos","50% 50%")
    d("greeting","Hare Krishna!"); d("closing","Hare Krishna!")
    d("stats",[(pk["days"],"Days"),(pk["nights"],"Nights")]+([(pk["km"],"Km by road")] if pk.get("km") else [])+([(pk["temples"],"Temples & shrines")] if pk.get("temples") else []))
    d("why",WHY); d("extra_terms",[]); d("faq_common",FAQ_COMMON); d("faq",[])
    d("dos",COMMON_DOS); d("donts",COMMON_DONTS); d("flights",[]); d("flights_title","Flight info · please book accordingly")
    d("meal_subtitle","Pure vegetarian · sattvic")
    d("meal_note","All breakfasts, lunches and dinners are included. Meals are pure vegetarian at hotels and selected restaurants. No onion-garlic food on request.")
    d("timing_note",TIMING_NOTE); d("journey_title","Your Journey at a Glance")
    po=pk.setdefault("poster",{}); po.setdefault("hero",pk["hero"]); po.setdefault("pos",pk["hero_pos"]); po.setdefault("kicker",pk["kicker"])
    po.setdefault("hl",pk["highlights"][:8]); po.setdefault("circ",[k for k,_ in pk.get("cover_circles",[])][:3])
    po.setdefault("price_small",f'{pk["gst_note"]} · per person · excl. flights'); po.setdefault("reg",f'Registrations close<br>{E(pk["reg_short"])}' if pk["reg_short"] else "")
    it=pk.setdefault("itinerary",{}); it.setdefault("hero",pk["hero"]); it.setdefault("kicker",pk["kicker"])
    it.setdefault("special",[]); it.setdefault("memo",MEMO); it.setdefault("footer_closing",pk["closing"]); it.setdefault("days",[])
    it.setdefault("meal_note",MEAL_TABLE_NOTE)
    pk["rows_path"]=os.path.join(wd,pk.get("rows","rows.json"))
    pk["restaurants_path"]=os.path.join(wd,pk.get("restaurants","restaurants.json"))
    return pk

def load_img(pk):
    m=dict(BRAND_IMG)
    p=os.path.join(pk["_dir"],"imgmap.json")
    if os.path.exists(p): m.update(json.load(open(p)))
    return m

def day_date(pk,n,fmt):
    if not pk.get("start_date"): return ""
    return (datetime.date.fromisoformat(pk["start_date"])+datetime.timedelta(n-1)).strftime(fmt)

def load_rows(pk): return json.load(open(pk["rows_path"]))
