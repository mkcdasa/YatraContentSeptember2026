"""
Route-optimised version of the London & Europe Grand Tour (17 Apr – 2 May 2027), as a proposal.
Same arrival (London Heathrow, 17 Apr) and departure (Milan Malpensa, 2 May); stops re-ordered so the
coach never doubles back. Road distances come from OSRM (cached in maps/cache).

Main changes against itinerary_data.py:
 1. London → Paris by Eurostar through the Channel Tunnel (2 h 16 m) instead of coach + Dover ferry (≈11 h door to door).
 2. Paris done in 1½ days; ISKCON Paris (Sevran) visited on the way out to Brussels (it lies on the A1/A2).
 3. Brussels → Keukenhof → Amsterdam in one line; Zaanse Schans on the way out of Amsterdam.
 4. Radhadesh (Château de Petite Somme + Museum of Sacred Art) dropped: a 215 km detour into the Ardennes.
 5. Milan Duomo moved to the evening of the Como day; Villaggio Hare Krishna (Bergamo) visited on the A4 towards Venice.
 6. Venice → Rome by Frecciarossa with a night in Rome (no 05:00 start), Rome → Florence next afternoon, Pisa on the way to Malpensa.
"""
import os, sys, json, math, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import itinerary_data as D  # noqa: E402

CO = json.load(open(os.path.join(ROOT, "maps", "coords.json")))
CO.update({"ST_PANCRAS": [51.5308, -0.1260], "GARE_NORD": [48.8809, 2.3553], "MILANO_C": [45.4855, 9.2040],
           "H_ROM": [41.9000, 12.5010], "PANTHEON": [41.8986, 12.4769], "NAVONA": [41.8992, 12.4731],
           "SPANISH": [41.9060, 12.4828], "PISA_LUNCH": [43.7180, 10.4000], "TROCADERO": [48.8616, 2.2893]})
NAME = {k: v[0] for k, v in D.PLACES.items()}
NAME.update({"ST_PANCRAS": "London St Pancras International", "GARE_NORD": "Paris Gare du Nord", "MILANO_C": "Milano Centrale",
             "H_ROM": "Hotel, Rome – near Termini (TBC)", "PANTHEON": "Pantheon", "NAVONA": "Piazza Navona",
             "SPANISH": "Spanish Steps", "PISA_LUNCH": "Pisa – lunch (packed Satvik lunch / Indian restaurant, TBC)",
             "TROCADERO": "Trocadéro"})
CACHE = os.path.join(ROOT, "maps", "cache")

def osrm(a, b):
    (la, oa), (lb, ob) = CO[a], CO[b]
    key = f"{oa:.5f},{la:.5f};{ob:.5f},{lb:.5f}"
    p = os.path.join(CACHE, "dist_" + key.replace(",", "_").replace(";", "__") + ".json")
    if not os.path.exists(p):
        u = f"https://router.project-osrm.org/route/v1/driving/{key}?overview=false"
        with urllib.request.urlopen(u, timeout=30) as r:
            open(p, "w").write(r.read().decode())
    r = json.load(open(p))["routes"][0]
    return r["distance"] / 1000, r["duration"] / 60

def hav(a, b):
    (la, oa), (lb, ob) = CO[a], CO[b]
    x = math.sin(math.radians(lb - la) / 2) ** 2 + math.cos(math.radians(la)) * math.cos(math.radians(lb)) * math.sin(math.radians(ob - oa) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(x))

# row: (start, end, kind, text) or (start, end, "GO", frm, to, mode, note[, km])
def old(i, drop=()):
    rows = []
    for r in D.DAYS[i - 1]["rows"]:
        if r["kind"] in drop: continue
        if r["frm"] and r["km"]:
            rows.append((r["start"], r["end"], "GO", r["frm"], r["to"], r["mode"], (r["detail"] or "")[:150], r["km"]))
        else:
            txt = NAME.get(r["to"], r["to"])
            det = r["detail"] or r["meal_by"] or ""
            rows.append((r["start"], r["end"], r["kind"], f"<b>{txt}</b>" + (f" — {det}" if det else "")))
    return rows

MORN = ("07:30", "08:00", "Morning programme", D.MORNING)
BRK = ("08:00", "09:00", "Breakfast", "Hotel breakfast")

DAYS = [
 dict(n=1, title="Arrive London Heathrow · Kamada Ekadasi", on="London (Wembley)", rows=old(1), same=1),
 dict(n=2, title="Akshaya Patra · Bhaktivedanta Manor Sunday programme · Madame Tussauds · ISKCON Soho · Covent Garden",
      on="London (Wembley)", rows=old(2), same=2),
 dict(n=3, title="Royal London: Changing of the Guard · King's Gallery · Tower of London · Tower Bridge · Thames boat · London Eye · Westminster",
      on="London (Wembley)", rows=old(3)[:-1] + [("21:30", "22:00", "Packing", "<b>Hotel</b> — Pack tonight; luggage in the lobby at 06:45. Passports in hand luggage: UK exit and French/Schengen entry (EES fingerprints) happen at St Pancras, before boarding.")], same=3),
 dict(n=4, title="Eurostar through the Channel Tunnel to Paris · Arc de Triomphe · Champs-Élysées · Trocadéro · Eiffel Tower · Seine cruise", on="Paris", rows=[
    ("06:15", "06:50", "Breakfast", "<b>Hotel</b> — early breakfast (exception to the 08:00 start)"),
    ("06:50", "07:10", "Check-out", "Check-out, luggage loaded, headcount."),
    ("07:10", "07:50", "GO", "H_LON", "ST_PANCRAS", "Coach", "UK coach's last run; luggage goes with the group onto the train."),
    ("07:50", "08:45", "Border check", "<b>St Pancras International</b> — group check-in, security, UK exit and French entry (EU Entry/Exit System) before boarding."),
    ("09:01", "12:20", "GO", "ST_PANCRAS", "GARE_NORD", "Train", "Eurostar, 2 h 16 m (clocks go forward 1 h). 50 km of it under the sea in the Channel Tunnel — one of the 'Seven Wonders of the Modern World' (American Society of Civil Engineers).", 492),
    ("12:20", "12:40", "Meet coach", "<b>Paris Gare du Nord</b> — continental coach meets the group; luggage loaded."),
    ("12:40", "12:50", "GO", "GARE_NORD", "SARAVANAA_PAR", "Coach", "Saravanaa Bhavan is 600 m from the station."),
    ("12:50", "13:50", "Lunch", "<b>Saravanaa Bhavan Paris</b> — South Indian vegetarian meals."),
    ("13:50", "14:20", "GO", "SARAVANAA_PAR", "ARC", "Coach", "Past the Opéra and Place de la Concorde."),
    ("14:20", "15:05", "Sightseeing", "<b>Arc de Triomphe</b> photo stop and a stroll on the <b>Champs-Élysées</b>."),
    ("15:05", "15:15", "GO", "ARC", "TROCADERO", "Coach", ""),
    ("15:15", "15:40", "Photo stop", "<b>Trocadéro</b> — the classic Eiffel Tower group photo."),
    ("15:40", "15:50", "GO", "TROCADERO", "EIFFEL", "Coach", "Across the Pont d'Iéna."),
    ("16:00", "18:00", "Sightseeing", "<b>Eiffel Tower</b> — lift to the 2nd floor (timed group ticket)."),
    ("18:00", "18:30", "GO", "EIFFEL", "H_PAR", "Coach", ""),
    ("18:30", "19:00", "Hotel", "<b>Hotel, Paris</b> — check-in."),
    ("19:15", "20:15", "Dinner", "<b>Hotel / Indian restaurant</b> — Satvik dinner."),
    ("20:25", "20:55", "GO", "H_PAR", "SEINE", "Coach", ""),
    ("21:00", "22:00", "Boat", "<b>Seine river cruise</b> (1 h): Notre-Dame, Louvre, Musée d'Orsay, the Eiffel Tower sparkling on the hour."),
    ("22:05", "22:35", "GO", "SEINE", "H_PAR", "Coach", ""),
 ]),
 dict(n=5, title="Louvre & Mona Lisa · Notre-Dame · ISKCON Paris (on the way) · Brussels Grand Place by evening", on="Brussels", rows=[
    MORN, BRK, ("08:30", "09:00", "Check-out", "Check-out, luggage loaded."),
    ("09:00", "09:20", "GO", "H_PAR", "LOUVRE", "Coach", ""),
    ("09:30", "11:30", "Sightseeing", "<b>Louvre</b> with a licensed guide: Mona Lisa, Venus de Milo, Winged Victory. (Louvre is closed on Tuesdays, so it is on Wednesday.)"),
    ("11:30", "11:40", "GO", "LOUVRE", "NOTREDAME", "Coach", "Along the Seine."),
    ("11:40", "12:20", "Sightseeing", "<b>Notre-Dame Cathedral</b> (reopened Dec 2024) and the <b>Île de la Cité</b>."),
    ("12:20", "12:40", "GO", "NOTREDAME", "KRISHNABHAVAN_PAR", "Coach", ""),
    ("12:40", "13:30", "Lunch", "<b>Krishna Bhavan, Rue Cail</b> — South Indian vegetarian lunch."),
    ("13:30", "14:10", "GO", "KRISHNABHAVAN_PAR", "ISKCON_PAR", "Coach", "Sevran lies on the way out of Paris towards Brussels."),
    ("14:10", "15:00", "Temple", "<b>ISKCON Paris</b> — darshan and kirtan."),
    ("15:00", "19:10", "GO", "ISKCON_PAR", "GRANDPLACE", "Coach", "A1 / E19 to Brussels, one 20-minute break."),
    ("19:10", "20:10", "Sightseeing", "<b>Grand Place</b> (UNESCO) lit up in the evening, <b>Galeries Royales Saint-Hubert</b>, <b>Manneken Pis</b>."),
    ("20:10", "20:20", "GO", "GRANDPLACE", "H_BRU", "Coach", ""),
    ("20:20", "20:40", "Hotel", "<b>Hotel, Brussels</b> — check-in."),
    ("20:40", "21:40", "Dinner", "<b>Hotel / Indian restaurant</b>"),
 ]),
 dict(n=6, title="Atomium · Keukenhof tulip gardens · Amsterdam canal cruise", on="Amsterdam", rows=[
    MORN, BRK, ("08:30", "09:00", "Check-out", "Check-out, luggage loaded."),
    ("09:00", "09:20", "GO", "H_BRU", "ATOMIUM", "Coach", ""),
    ("09:20", "09:50", "Photo stop", "<b>Atomium</b> — the giant iron-crystal model from Expo 58."),
    ("09:50", "13:05", "GO", "ATOMIUM", "KEUKENHOF", "Coach", "Antwerp ring, Rotterdam, through the Dutch bulb fields."),
    ("13:05", "16:00", "Sightseeing", "<b>Keukenhof</b> — 7 million tulips at peak bloom (open 18 Mar – 9 May 2027); packed Satvik lunch inside, 13:15–14:00 (snacks on the coach before)."),
    ("16:00", "16:45", "GO", "KEUKENHOF", "H_AMS", "Coach", ""),
    ("16:45", "17:15", "Hotel", "<b>Hotel, Amsterdam</b> — check-in."),
    ("17:20", "17:40", "GO", "H_AMS", "CANAL", "Coach", ""),
    ("17:45", "19:00", "Boat", "<b>Amsterdam canal cruise</b> (75 min, glass-roofed boat) through the UNESCO canal ring in daylight."),
    ("19:00", "19:20", "GO", "CANAL", "H_AMS", "Coach", ""),
    ("19:30", "20:30", "Dinner", "<b>Hotel / Indian restaurant</b>. Free evening."),
 ]),
 dict(n=7, title="Zaanse Schans windmills · Cologne Cathedral · Hohenzollern Bridge · ISKCON Cologne", on="Cologne", rows=[
    MORN, BRK, ("08:30", "09:00", "Check-out", "Check-out, luggage loaded."),
    ("09:00", "09:30", "GO", "H_AMS", "ZAANSE", "Coach", ""),
    ("09:30", "11:00", "Sightseeing", "<b>Zaanse Schans</b> — working windmills, <b>clog-making and cheese workshops</b>."),
    ("11:00", "14:55", "GO", "ZAANSE", "H_CGN", "Coach", "A2/A12 via Utrecht and Arnhem; one 20-minute break."),
    ("15:00", "15:45", "Lunch", "<b>Hotel, Cologne</b> — check-in and late lunch (Indian restaurant, TBC)."),
    ("15:45", "15:55", "GO", "H_CGN", "DOM", "Coach", ""),
    ("15:55", "17:15", "Sightseeing", "<b>Cologne Cathedral</b> (UNESCO) inside and out, then a walk over the <b>Hohenzollern Bridge</b> (love locks, best view of the cathedral)."),
    ("17:15", "17:40", "GO", "DOM", "ISKCON_CGN", "Coach", ""),
    ("17:40", "19:00", "Temple", "<b>ISKCON Cologne</b> — darshan, evening arati, kirtan with local devotees."),
    ("19:00", "19:20", "GO", "ISKCON_CGN", "H_CGN", "Coach", ""),
    ("19:30", "20:30", "Dinner", "<b>Hotel / Indian restaurant</b>"),
 ]),
 dict(n=8, title="Goloka Dham · Black Forest drive to Lake Titisee", on="Titisee (Black Forest)", rows=[
    MORN, BRK, ("08:30", "09:00", "Check-out", "Check-out."),
    ("09:00", "11:45", "GO", "H_CGN", "GOLOKA", "Coach", "Along the Rhine and over the Hunsrück hills."),
    ("11:45", "12:45", "Temple", "<b>Goloka Dham</b>, ISKCON's rural centre in Germany — darshan and kirtan."),
    ("12:45", "13:30", "Lunch", "<b>Goloka Dham</b> — prasadam lunch."),
    ("13:30", "18:15", "GO", "GOLOKA", "H_TIT", "Coach", "Last 90 minutes on the <b>Black Forest</b> scenic road (B500 / B31) through pine forest and valleys; one break."),
    ("18:15", "18:45", "Hotel", "<b>Hotel, Titisee</b> — check-in. Black Forest nights can be near 0 °C."),
    ("19:00", "20:00", "Dinner", "<b>Hotel</b>"),
 ]),
 dict(n=9, title="Lake Titisee & cuckoo clocks · Rhine Falls · Zurich · ISKCON Zurich", on="Zurich", rows=old(10), same=10),
 dict(n=10, title="Mount Titlis snow & Rotair · Lucerne · Lake Lucerne cruise · Luzern–Interlaken Express", on="Interlaken", rows=old(11), same=11),
 dict(n=11, title="Jungfrau view · Lake Como boat ride · Milan Duomo, Galleria & La Scala by evening", on="Milan", rows=[
    MORN, BRK, ("08:30", "09:00", "Check-out", "Check-out."),
    ("09:00", "09:20", "Sightseeing", "<b>Höhematte park</b> — morning view of the snow-covered <b>Jungfrau</b>."),
    ("09:20", "13:30", "GO", "H_INT", "COMO", "Coach", "Over the Alps by the Simplon or Gotthard road; one break."),
    ("13:30", "14:30", "Lunch", "<b>Como</b> — Indian restaurant (TBC)."),
    ("14:30", "16:00", "Boat", "<b>Lake Como boat ride</b> and the <b>Como Cathedral</b>."),
    ("16:00", "17:15", "GO", "COMO", "DUOMO_MIL", "Coach", ""),
    ("17:15", "18:45", "Sightseeing", "<b>Milan Duomo</b> (rooftop optional), <b>Galleria Vittorio Emanuele II</b> and <b>La Scala</b> in the evening lights."),
    ("18:45", "19:05", "GO", "DUOMO_MIL", "H_MIL", "Coach", ""),
    ("19:05", "19:30", "Hotel", "<b>Hotel, Milan</b> — check-in."),
    ("19:45", "20:45", "Dinner", "<b>Hotel / Indian restaurant</b>"),
 ]),
 dict(n=12, title="Villaggio Hare Krishna · Prabhupada Desh · Padova · Venice", on="Venice-Mestre", rows=[
    ("06:30", "07:00", "Morning programme", D.MORNING), ("07:00", "07:45", "Breakfast", "Hotel breakfast (early)"), ("07:45", "08:00", "Check-out", "Check-out."),
    ("08:00", "09:00", "GO", "H_MIL", "VILLAGGIO", "Coach", "A4 east towards Venice."),
    ("09:00", "10:00", "Temple", "<b>Villaggio Hare Krishna</b>, Italy's oldest ISKCON farm community — morning darshan."),
    ("10:00", "12:50", "GO", "VILLAGGIO", "PRABHUPADADESH", "Coach", "Still on the A4."),
    ("12:50", "14:30", "Temple", "<b>Prabhupada Desh</b> — darshan, kirtan and prasadam lunch."),
    ("14:30", "15:15", "GO", "PRABHUPADADESH", "PADOVA", "Coach", ""),
    ("15:15", "16:00", "Sightseeing", "<b>Padova</b> — <b>Basilica of St Anthony</b> and <b>Prato della Valle</b>."),
    ("16:00", "16:45", "GO", "PADOVA", "TRONCHETTO", "Coach", ""),
    ("16:55", "20:00", "Sightseeing", "<b>Venice</b> by vaporetto: <b>St Mark's Square & Basilica</b>, <b>Doge's Palace & Bridge of Sighs</b>, <b>Rialto Bridge</b>, <b>gondola ride</b>."),
    ("20:05", "20:30", "GO", "TRONCHETTO", "H_MES", "Coach", ""),
    ("20:30", "20:45", "Hotel", "<b>Hotel, Venice-Mestre</b> — check-in."),
    ("20:45", "21:45", "Dinner", "<b>Hotel</b>"),
 ]),
 dict(n=13, title="Frecciarossa Venice → Rome · Vatican Museums & Sistine Chapel · St Peter's · Colosseum & Roman Forum", on="Rome", rows=[
    ("06:15", "06:45", "Breakfast", "Hotel breakfast (early)"),
    ("06:45", "07:00", "Check-out", "Check-out with a small overnight bag; big luggage stays on the coach, which drives to Florence (260 km, no passengers) to meet us tomorrow."),
    ("07:00", "07:10", "GO", "H_MES", "VE_MESTRE", "Coach", ""),
    ("07:30", "11:15", "GO", "VE_MESTRE", "ROMA_TERMINI", "Train", "<b>Frecciarossa</b> high-speed train, about 3 h 45 m.", 530),
    ("11:15", "11:45", "GO", "ROMA_TERMINI", "VATICAN", "Local coach", ""),
    ("11:45", "14:00", "Sightseeing", "<b>Vatican Museums</b> and the <b>Sistine Chapel</b> with licensed guides (timed group entry)."),
    ("14:00", "14:50", "Lunch", "<b>Indian restaurant near the Vatican</b> (TBC)."),
    ("15:00", "15:45", "Sightseeing", "<b>St Peter's Basilica</b> (Michelangelo's Pietà) and <b>St Peter's Square</b>."),
    ("15:45", "16:15", "GO", "VAT_LUNCH", "COLOSSEUM", "Local coach", ""),
    ("16:15", "18:30", "Sightseeing", "<b>Colosseum (inside)</b> and the <b>Roman Forum</b> with a guide (timed group ticket; summer hours, last entry 18:15)."),
    ("18:30", "18:50", "GO", "COLOSSEUM", "H_ROM", "Local coach", ""),
    ("18:50", "19:20", "Hotel", "<b>Hotel, Rome</b> — check-in."),
    ("19:45", "20:45", "Dinner", "<b>Indian restaurant near Termini</b> (TBC)."),
 ]),
 dict(n=14, title="Trevi Fountain · Pantheon · Piazza Navona · Spanish Steps · Frecciarossa to Florence · Duomo · Ponte Vecchio · Piazzale Michelangelo · Villa Vrindavan", on="Florence", rows=[
    MORN, ("07:30", "08:15", "Breakfast", "Hotel breakfast"), ("08:15", "08:30", "Check-out", "Check-out; bags kept on the local coach."),
    ("08:30", "08:45", "GO", "H_ROM", "TREVI", "Local coach", ""),
    ("08:45", "09:30", "Sightseeing", "<b>Trevi Fountain</b> before the crowds (coin toss)."),
    ("09:30", "09:40", "GO", "TREVI", "PANTHEON", "Walk", ""),
    ("09:40", "10:20", "Sightseeing", "<b>Pantheon</b>."),
    ("10:20", "10:30", "GO", "PANTHEON", "NAVONA", "Walk", ""),
    ("10:30", "11:00", "Sightseeing", "<b>Piazza Navona</b> — Bernini's Fountain of the Four Rivers."),
    ("11:00", "11:20", "GO", "NAVONA", "SPANISH", "Local coach", ""),
    ("11:20", "11:50", "Sightseeing", "<b>Spanish Steps</b> and Via Condotti."),
    ("11:50", "12:10", "GO", "SPANISH", "ROMA_TERMINI", "Local coach", ""),
    ("12:10", "13:00", "Lunch", "<b>Near Termini</b> — Indian restaurant (TBC)."),
    ("13:20", "14:55", "GO", "ROMA_TERMINI", "FI_SMN", "Train", "<b>Frecciarossa</b> Rome → Florence, 1 h 35 m. Our coach (with the big luggage) meets us at Santa Maria Novella.", 275),
    ("14:55", "15:10", "GO", "FI_SMN", "FLORENCE", "Coach", ""),
    ("15:10", "17:00", "Sightseeing", "<b>Florence</b> (UNESCO): <b>Duomo</b> with Brunelleschi's dome, <b>Piazza della Signoria</b>, <b>Ponte Vecchio</b>."),
    ("17:00", "17:20", "GO", "FLORENCE", "MICHELANGELO", "Coach", ""),
    ("17:20", "17:50", "Viewpoint", "<b>Piazzale Michelangelo</b> — panorama of Florence; group photo."),
    ("17:50", "18:25", "GO", "MICHELANGELO", "VILLAVRINDAVAN", "Coach", ""),
    ("18:25", "19:40", "Temple", "<b>Villa Vrindavan</b> (ISKCON Florence) — evening arati and prasadam dinner."),
    ("19:40", "20:15", "GO", "VILLAVRINDAVAN", "H_FLR", "Coach", ""),
    ("20:15", "20:40", "Hotel", "<b>Hotel, Florence</b> — check-in."),
 ]),
 dict(n=15, title="Leaning Tower of Pisa · drive to Milan Malpensa · relaxed last evening", on="Near Milan Malpensa airport", rows=[
    MORN, BRK, ("08:30", "09:00", "Check-out", "Check-out, luggage loaded."),
    ("09:00", "10:35", "GO", "H_FLR", "PISA", "Coach", ""),
    ("10:35", "12:00", "Sightseeing", "<b>Square of Miracles</b> (UNESCO): <b>Leaning Tower, Cathedral & Baptistery of Pisa</b> (tower climb optional, own expense). 1 May is an Italian holiday: expect crowds, the square stays open."),
    ("12:00", "13:00", "Lunch", "<b>Pisa</b> — Indian restaurant (TBC)."),
    ("13:00", "17:30", "GO", "PISA", "H_MXP", "Coach", "Along the coast past La Spezia and Genoa, then north to Malpensa; one break."),
    ("17:30", "18:00", "Hotel", "<b>Hotel near Malpensa</b> — check-in and rest."),
    ("19:30", "20:30", "Dinner", "<b>Hotel</b> — farewell dinner."),
    ("20:30", "21:15", "Packing", "Final packing: 30 kg check-in + 7 kg cabin; weigh bags in the lobby."),
 ]),
 dict(n=16, title="Fly home from Milan Malpensa", on="On flight (land 3 May)", rows=old(16), same=16),
]

# ---------- measurement ----------
def mins(a, b):
    h1, m1 = map(int, a.split(":")); h2, m2 = map(int, b.split(":"))
    d = (h2 * 60 + m2) - (h1 * 60 + m1)
    return d if d >= 0 else d + 1440

GROUP_SKIP = ("empty", "drives empty", "luggage only")
def legs(day):
    out = []
    for r in day["rows"]:
        if r[2] != "GO": continue
        s, e, _, a, b, mode, note = r[:7]
        if mode == "Flight": continue
        km = r[7] if len(r) > 7 else None
        if km is None:
            km = osrm(a, b)[0] if mode in ("Coach", "Local coach") else hav(a, b) * 1.3
        m = mins(s, e) - (60 if a == "ST_PANCRAS" else 0)   # Eurostar timetable crosses into CET
        out.append(dict(s=s, e=e, a=a, b=b, mode=mode, note=note, km=round(km, 1), m=m))
    return out

def old_legs(i):
    out = []
    for r in D.DAYS[i - 1]["rows"]:
        if r["frm"] and r["km"] and r["mode"] != "Flight":
            out.append(dict(mode=r["mode"], km=r["km"], m=mins(r["start"], r["end"]),
                            empty=("empty" in (r["detail"] + r["note"]).lower() and r["mode"] in ("Coach",)) or
                                  (i == 11 and r["mode"] == "Coach" and r["to"] == "H_INT") or (i == 1)))
    return out

if __name__ == "__main__":
    for d in DAYS:
        for l in legs(d):
            if l["mode"] in ("Coach", "Local coach"):
                dkm, dmin = osrm(l["a"], l["b"])
                need = dmin * 1.15 + (20 if dmin > 150 else 0)
                flag = "  <-- tight" if l["m"] < need - 10 else ""
                print(f'D{d["n"]:2} {l["a"]:>16}->{l["b"]:<16} {dkm:6.0f} km  osrm {dmin:4.0f} min  plan {l["m"]:4} min{flag}')
