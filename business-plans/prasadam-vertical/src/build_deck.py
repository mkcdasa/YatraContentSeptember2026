"""Builds 02_Presentation.pptx (16:9)."""
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

import content as C

OUT = Path(__file__).resolve().parent.parent / "02_Presentation.pptx"

MAROON = RGBColor(0x7A, 0x1F, 0x2B)
SAFFRON = RGBColor(0xE0, 0x7B, 0x00)
GOLD = RGBColor(0xC9, 0xA2, 0x27)
CREAM = RGBColor(0xFF, 0xF8, 0xEC)
INK = RGBColor(0x2B, 0x22, 0x1E)
MUTED = RGBColor(0x6B, 0x5E, 0x55)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PALE = RGBColor(0xFB, 0xEB, 0xD0)
GREEN = RGBColor(0x2E, 0x7D, 0x32)
BLUE = RGBColor(0x1F, 0x5F, 0x8B)
FONT = "Calibri"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
W, H = prs.slide_width, prs.slide_height


def box(slide, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE, radius=None):
    s = slide.shapes.add_shape(shape, x, y, w, h)
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(1)
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    s.shadow.inherit = False
    return s


def text(slide, x, y, w, h, t, size=14, color=INK, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, shape=None):
    tb = shape or slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right"):
        setattr(tf, m, Inches(0.08))
    tf.margin_top = tf.margin_bottom = Inches(0.04)
    lines = t if isinstance(t, list) else [t]
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = ln
        r.font.size, r.font.bold, r.font.color.rgb, r.font.name = Pt(size), bold, color, FONT
    return tb


def bullets(slide, x, y, w, h, items, size=14, color=INK, gap=4):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        r = p.add_run()
        r.text = "•  " + it
        r.font.size, r.font.color.rgb, r.font.name = Pt(size), color, FONT
    return tb


def base(title, kicker=None, num=[0]):
    num[0] += 1
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = CREAM
    box(s, 0, 0, Inches(0.18), H, fill=SAFFRON)
    if kicker:
        text(s, Inches(0.55), Inches(0.3), Inches(10), Inches(0.35), kicker.upper(), 11, SAFFRON, True)
    text(s, Inches(0.55), Inches(0.55), Inches(12.2), Inches(0.8), title, 28, MAROON, True)
    box(s, Inches(0.62), Inches(1.32), Inches(1.2), Inches(0.05), fill=GOLD)
    text(s, Inches(0.55), Inches(7.05), Inches(9), Inches(0.3), "Hare Krishna Golden Temple · Prasadam, Sweets & Savories Vertical", 9, MUTED)
    text(s, Inches(12.2), Inches(7.05), Inches(0.8), Inches(0.3), str(num[0] + 1), 9, MUTED, align=PP_ALIGN.RIGHT)
    return s


def card(s, x, y, w, h, head, body, head_fill=MAROON, size=12, body_items=None):
    box(s, x, y, w, h, fill=WHITE, line=PALE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    hd = box(s, x, y, w, Inches(0.5), fill=head_fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.25)
    text(s, 0, 0, 0, 0, head, 13, WHITE, True, anchor=MSO_ANCHOR.MIDDLE, shape=hd)
    if body_items:
        bullets(s, x + Inches(0.05), y + Inches(0.58), w - Inches(0.1), h - Inches(0.6), body_items, size, gap=2)
    elif body:
        text(s, x + Inches(0.05), y + Inches(0.58), w - Inches(0.1), h - Inches(0.6), body, size)


def notes(s, t):
    s.notes_slide.notes_text_frame.text = t


# 1 Title -------------------------------------------------------------------
s = prs.slides.add_slide(BLANK)
s.background.fill.solid()
s.background.fill.fore_color.rgb = MAROON
box(s, 0, Inches(5.9), W, Inches(0.08), fill=GOLD)
text(s, Inches(0.9), Inches(1.2), Inches(11), Inches(0.5), "HARE KRISHNA GOLDEN TEMPLE (ISKCON) · HYDERABAD", 14, GOLD, True)
text(s, Inches(0.9), Inches(1.9), Inches(11.5), Inches(1.8), ["Prasadam, Sweets & Savories", "A New Revenue Vertical"], 44, WHITE, True)
text(s, Inches(0.9), Inches(3.95), Inches(11), Inches(1.2), "Business plan · Target audiences · Revenue models · Roadmap · Project plan", 18, PALE)
text(s, Inches(0.9), Inches(6.2), Inches(11), Inches(0.8), ["From the house of Radha Krishna: satvik, pure, no preservatives", C.VERSION], 13, PALE)
notes(s, "Built from the 26 Sep 2026 Prasadam Revenue Generation Plan meeting plus desk research.")

# 2 Executive summary ---------------------------------------------------------
y1 = sum(r[1] for r in C.REVENUE_Y1)
y2 = sum(r[1] * r[2] for r in C.REVENUE_Y1)
y3 = sum(r[1] * r[2] * r[3] for r in C.REVENUE_Y1)
s = base("Demand is proven; we now have a production owner", "Executive summary")
stats = [("₹6 L", "Janmashtami 2026 counters\n(sold out)"), ("10×", "festival sales target"),
         ("14", "revenue streams across\n5 audience circles"), (f"₹{y1 / 100:.1f} Cr", "Year-1 revenue\ntarget [estimate]")]
for i, (big, small) in enumerate(stats):
    x = Inches(0.6 + i * 3.1)
    box(s, x, Inches(1.65), Inches(2.9), Inches(1.7), fill=WHITE, line=PALE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    text(s, x, Inches(1.75), Inches(2.9), Inches(0.8), big, 36, SAFFRON, True, PP_ALIGN.CENTER)
    text(s, x, Inches(2.55), Inches(2.9), Inches(0.8), small.split("\n"), 12, MUTED, align=PP_ALIGN.CENTER)
bullets(s, Inches(0.6), Inches(3.65), Inches(12.2), Inches(3.3), [
    "Trust is our moat: people believe in ISKCON; satvik, chemical-free prasadam commands loyalty and price.",
    "Warm network: company owners (10,000-staff firms), MNR's 42 institutions, chambers, BNI, Rotary, 100 gated communities, donors.",
    "The missing piece is solved: temple production owns the kitchen; Mukunda Dasa and DMTT own marketing, tech and sales.",
    "Two-tier pricing: a mass tier keeps the kitchen running, a premium tier adds margin.",
    "Start lean: internal supply, festival stalls, corporate and white-label gifting for Dasara/Diwali 2026. Build capacity only after demand is proven.",
    f"Grow to about ₹{y2 / 100:.1f} Cr in Year 2 and ₹{y3 / 100:.1f} Cr in Year 3; then QSRs, pan-India and exports.",
], 15)

# 3 Why now -------------------------------------------------------------------
s = base("Why now: the market is untapped and we are late", "The opportunity")
card(s, Inches(0.6), Inches(1.65), Inches(3.9), Inches(5.1), "What we heard", None, body_items=[
    "Janmashtami counters sold out (~₹6 L)",
    "3 companies asked for gift boxes and we could not supply",
    "Chinmaya Mission asked for 50,000 meals",
    "Big donors ask for 5 kg namkeen in monsoon",
    "A partner offers funds for 100 QSRs",
    "No temple in our group has done this at scale",
], size=15)
card(s, Inches(4.72), Inches(1.65), Inches(3.9), Inches(5.1), "What the market says", None, head_fill=SAFFRON, body_items=[
    "Packaged sweets: ₹8,431 Cr (2025) → ₹30,506 Cr by 2034, ~16% CAGR",
    "Namkeen: +USD 4.9 bn by 2030, ~10% CAGR",
    "Corporate gifting: > ₹27,000 Cr by 2030",
    "58% of Diwali gifts are corporate",
    "GST on packaged namkeen cut 12% → 5%",
], size=15)
card(s, Inches(8.84), Inches(1.65), Inches(3.9), Inches(5.1), "What we already have", None, head_fill=GREEN, body_items=[
    "ISKCON brand and top SEO ranking",
    "Donor databases, WhatsApp, ads skills",
    "Online donor prasadam dispatch system",
    "Shopify experience; ~15,000 Amazon parcels shipped",
    "Negotiated vendor rates, new kitchen",
    "AI engineers and data scientists",
], size=15)

# 4 Vision -------------------------------------------------------------------
s = base("Vision, mission and brand", "Direction")
text(s, Inches(0.6), Inches(1.6), Inches(12), Inches(1.0), C.VISION, 17, INK)
text(s, Inches(0.6), Inches(2.75), Inches(12), Inches(1.0), C.MISSION, 14, MUTED)
pillars = [("Purity", "Satvik, no preservatives, no artificial colours"), ("Devotion", "Prepared with care and offered to the Deity"),
           ("Trust", "Decades of ISKCON goodwill in Hyderabad"), ("Service", "Proceeds support temple seva"), ("Delight", "Packaging that makes gifting special")]
for i, (h, b) in enumerate(pillars):
    x = Inches(0.6 + i * 2.48)
    box(s, x, Inches(4.2), Inches(2.3), Inches(2.4), fill=WHITE, line=PALE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    circ = box(s, x + Inches(0.8), Inches(4.35), Inches(0.7), Inches(0.7), fill=SAFFRON, shape=MSO_SHAPE.OVAL)
    text(s, 0, 0, 0, 0, str(i + 1), 18, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=circ)
    text(s, x, Inches(5.15), Inches(2.3), Inches(0.4), h, 16, MAROON, True, PP_ALIGN.CENTER)
    text(s, x + Inches(0.1), Inches(5.6), Inches(2.1), Inches(0.9), b, 12, MUTED, align=PP_ALIGN.CENTER)

# 5 Mind map ------------------------------------------------------------------
s = base("The whole vertical on one page", "Mind map")
cx, cy = Inches(6.67), Inches(4.15)
branches = [
    ("Audiences", ["Visitors & festivals", "Donors", "Companies", "Institutions", "Communities", "Online / NRI"], MAROON),
    ("Revenue streams", ["Stalls & restaurant", "Corporate gifting", "White-label", "E-commerce", "Catering", "QSR & export"], SAFFRON),
    ("Products", ["Chikkis & laddus", "Kaja & khara", "Namkeen", "Puri unde", "Pickles & powders", "Gift boxes"], GOLD),
    ("Marketing", ["ISKCON brand", "Databases & AI", "WhatsApp / SMS", "Google & Meta ads", "Owner meetings", "SEO & PR"], BLUE),
    ("Operations", ["Kitchen + 1 hire", "Recipes & costing", "Shelf-life tests", "Packaging", "Dispatch", "FSSAI & GST"], GREEN),
    ("Governance", ["DMTT ROI", "Weekly review", "Risk register", "Budgets", "KPIs", "Roadmap phases"], MUTED),
]
import math
pos = [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]
for (name, leaves, col), (dx, dy) in zip(branches, pos):
    bx = cx + int(dx * Inches(3.1)) - Inches(1.05)
    by = cy + int(dy * Inches(1.75)) - Inches(0.28)
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, cx, cy, bx + Inches(1.05), by + Inches(0.28))
    c.line.color.rgb, c.line.width = col, Pt(2.5)
    nb = box(s, bx, by, Inches(2.1), Inches(0.56), fill=col, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.4)
    text(s, 0, 0, 0, 0, name, 13, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=nb)
    lx = bx + (Inches(2.2) if dx > 0 else -Inches(2.05))
    for j, lf in enumerate(leaves):
        ly = by + Inches(0.28) - Inches(0.78) + j * Inches(0.26)
        text(s, lx, ly, Inches(1.95), Inches(0.27), lf, 10, INK, align=PP_ALIGN.LEFT if dx > 0 else PP_ALIGN.RIGHT)
core = box(s, cx - Inches(1.3), cy - Inches(0.5), Inches(2.6), Inches(1.0), fill=MAROON, line=GOLD, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.3)
core.line.width = Pt(3)
text(s, 0, 0, 0, 0, ["Prasadam", "Vertical"], 17, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=core)
notes(s, "The full interactive mind map with every detail is in 03_Mind_Map.html.")

# 6 Audiences -----------------------------------------------------------------
s = base("Different circles, different products", "Target audiences")
circles = {}
for a in C.AUDIENCES:
    circles.setdefault(a["circle"], []).append(a["name"])
cols = [MAROON, SAFFRON, GOLD, BLUE, GREEN]
for i, (circ, names) in enumerate(circles.items()):
    x = Inches(0.6 + i * 2.48)
    card(s, x, Inches(1.65), Inches(2.32), Inches(3.6), circ.split(":")[0], None, head_fill=cols[i], body_items=[circ.split(": ")[1].capitalize()] + names, size=13)
bx_ = box(s, Inches(0.6), Inches(5.5), Inches(12.2), Inches(1.3), fill=PALE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
text(s, Inches(0.8), Inches(5.6), Inches(11.8), Inches(1.1), ["Start inside, then go out: Circle 1 (people already coming to us) funds the kitchen from day one;",
     "Circle 2 (our B2B network) brings the big festival orders; Circles 3–4 add year-round volume; Circle 5 is the long-term scale play."], 14, MAROON)

# 7 Audience detail table ------------------------------------------------------
s = base("What each audience needs and what we offer", "Target audiences")
rows = [("Audience", "Offer", "Channel", "Price")] + [(a["name"], a["offer"], a["channel"], a["price"]) for a in C.AUDIENCES]
tbl = s.shapes.add_table(len(rows), 4, Inches(0.6), Inches(1.5), Inches(12.2), Inches(5.2)).table
for ci, wv in enumerate([2.6, 4.6, 3.4, 1.6]):
    tbl.columns[ci].width = Inches(wv)
for ri, row in enumerate(rows):
    for ci, v in enumerate(row):
        cell = tbl.cell(ri, ci)
        cell.text = v
        cell.margin_top = cell.margin_bottom = Emu(20000)
        p = cell.text_frame.paragraphs[0]
        p.runs[0].font.size = Pt(8.5 if ri else 10)
        p.runs[0].font.name = FONT
        p.runs[0].font.bold = ri == 0 or ci == 0
        p.runs[0].font.color.rgb = WHITE if ri == 0 else INK
        cell.fill.solid()
        cell.fill.fore_color.rgb = MAROON if ri == 0 else (WHITE if ri % 2 else PALE)

# 8-9 Revenue streams -----------------------------------------------------------
for part, chunk in enumerate((C.STREAMS[:7], C.STREAMS[7:])):
    s = base(f"14 revenue streams ({part + 1}/2)", "Business models")
    for i, st in enumerate(chunk):
        col, row = i % 4, i // 4
        x, y = Inches(0.6 + col * 3.07), Inches(1.6 + row * 2.72)
        box(s, x, y, Inches(2.92), Inches(2.55), fill=WHITE, line=PALE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
        tag = box(s, x + Inches(0.12), y + Inches(0.12), Inches(0.62), Inches(0.36), fill=SAFFRON, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.4)
        text(s, 0, 0, 0, 0, st["id"], 11, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=tag)
        text(s, x + Inches(0.8), y + Inches(0.06), Inches(2.08), Inches(0.62), st["name"], 11.5, MAROON, True)
        text(s, x + Inches(0.08), y + Inches(0.74), Inches(2.78), Inches(1.3), st["what"], 10, INK)
        text(s, x + Inches(0.08), y + Inches(2.05), Inches(2.78), Inches(0.45), f"{st['phase']} · Capex {st['capex']} · Margin {st['margin']}", 9, MUTED)

# 10 Two-tier pricing --------------------------------------------------------
s = base("Two segments: volume + premium", "Pricing strategy")
card(s, Inches(0.6), Inches(1.65), Inches(5.9), Inches(2.4), "Mass / competitive tier", None, head_fill=SAFFRON, body_items=[
    "Local-shop price or slightly below; huge volumes",
    "Covers rent, power, salaries; keeps kitchen rotating",
    "Counters, communities, internal supply, students"], size=13)
card(s, Inches(6.85), Inches(1.65), Inches(5.9), Inches(2.4), "Premium tier", None, head_fill=MAROON, body_items=[
    "Pure ghee, dry fruits, jaggery, wooden boxes",
    "Limited volume, high margin",
    "VIP corporate boxes, donors, wellness range"], size=13)
rows = [("Gift box", "Price", "Contents", "Best for")] + list(C.GIFT_TIERS)
tbl = s.shapes.add_table(len(rows), 4, Inches(0.6), Inches(4.3), Inches(12.2), Inches(2.5)).table
for ci, wv in enumerate([2.2, 2.0, 5.2, 2.8]):
    tbl.columns[ci].width = Inches(wv)
for ri, row in enumerate(rows):
    for ci, v in enumerate(row):
        cell = tbl.cell(ri, ci)
        cell.text = v
        r = cell.text_frame.paragraphs[0].runs[0]
        r.font.size, r.font.name, r.font.bold = Pt(11), FONT, ri == 0 or ci == 0
        r.font.color.rgb = WHITE if ri == 0 else INK
        cell.fill.solid()
        cell.fill.fore_color.rgb = MAROON if ri == 0 else (WHITE if ri % 2 else PALE)

# 11 Products -------------------------------------------------------------------
s = base("Products: 15–20+ days shelf life first", "Product range")
groups = {}
for p in C.PRODUCTS:
    groups.setdefault(p[1].split(" –")[0], []).append(f"{p[0]}  ({p[2]} d)")
slots = [(0, 0, 5.2), (1, 0, 2.5), (2, 0, 2.5), (1, 1, 2.5), (2, 1, 2.5), (0, 1, 2.5)]
for i, (g, items) in enumerate(groups.items()):
    col, row, hh = slots[i]
    card(s, Inches(0.6 + col * 4.12), Inches(1.6 + row * 2.7), Inches(3.95), Inches(hh), g, None,
         head_fill=[SAFFRON, MAROON, GOLD, GREEN, BLUE, MUTED][i % 6], body_items=items, size=13 if hh > 3 else 12)

# 12 Packaging -------------------------------------------------------------
s = base("Attractive packaging wins the market", "Packaging")
bullets(s, Inches(0.6), Inches(1.6), Inches(7.4), Inches(5.3), C.PACKAGING, 14, gap=8)
card(s, Inches(8.3), Inches(1.6), Inches(4.45), Inches(5.2), "Every pack carries", None, body_items=[
    "Temple brand + story card", "FSSAI logo & number", "MFD, best-before, batch", "Ingredients & allergens",
    "Veg mark, net weight, MRP", "QR to store & donation page", "Client logo (white-label)"], size=13)

# 13 Marketing ----------------------------------------------------------------
s = base("Marketing: brand + network + technology", "Go-to-market")
for i, (lever, plan) in enumerate(C.MARKETING):
    col, row = i % 2, i // 2
    x, y = Inches(0.6 + col * 6.15), Inches(1.55 + row * 1.07)
    box(s, x, y, Inches(6.0), Inches(0.97), fill=WHITE, line=PALE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
    text(s, x + Inches(0.1), y + Inches(0.05), Inches(5.8), Inches(0.3), lever, 12, SAFFRON, True)
    text(s, x + Inches(0.1), y + Inches(0.33), Inches(5.8), Inches(0.62), plan, 10, INK)

# 14 Funnel + corporate process ----------------------------------------------
s = base("From first touch to repeat order", "Sales funnel")
for i, (stage, act) in enumerate(C.MARKETING_FUNNEL):
    wv = Inches(6.2 - i * 0.7)
    x = Inches(0.6) + (Inches(6.2) - wv) // 2
    b = box(s, x, Inches(1.65 + i * 0.85), wv, Inches(0.75), fill=[MAROON, SAFFRON, GOLD, GREEN, BLUE, MUTED][i], shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.2)
    text(s, 0, 0, 0, 0, stage, 13, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=b)
    text(s, Inches(7.1), Inches(1.7 + i * 0.85), Inches(5.7), Inches(0.7), act, 12, INK, anchor=MSO_ANCHOR.MIDDLE)

# 15 Festival stalls ----------------------------------------------------------
s = base("Festival stalls: 10× by going where the crowd is", "Temple campus")
spots = ["Main entrance", "Darshan exit queue", "Goshala walking path", "Staircases", "Garden / lawn", "Waterfall & benches", "Goshala entrance → Samskara", "Restaurant takes the lawn"]
for i, sp in enumerate(spots):
    col, row = i % 4, i // 4
    b = box(s, Inches(0.6 + col * 3.07), Inches(1.65 + row * 1.0), Inches(2.9), Inches(0.82), fill=WHITE, line=SAFFRON, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.25)
    text(s, 0, 0, 0, 0, sp, 13, MAROON, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=b)
bullets(s, Inches(0.6), Inches(3.85), Inches(12.2), Inches(3.0), [
    "One stall draws 10–50 people and the rest walk away. Put many counters in a row.",
    "Pre-packed combos (₹100/₹200/₹500), UPI at every counter, runners restock every hour.",
    "Permanent rain-proof pagodas: closed in rain, open otherwise.",
    "Passive selling: we are not pushing. People choose to approach, so this is not commercialising the temple.",
    "Shelf-stable stock is the hedge: leftovers go online / Instagram within 48 hours.",
], 14)

# 16 Operations ---------------------------------------------------------------
s = base("Operations: start with what we have", "Operations")
for i, (area, plan) in enumerate(C.OPERATIONS):
    col, row = i % 2, i // 2
    x, y = Inches(0.6 + col * 6.15), Inches(1.55 + row * 1.07)
    box(s, x, y, Inches(6.0), Inches(0.97), fill=WHITE, line=PALE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
    text(s, x + Inches(0.1), y + Inches(0.05), Inches(5.8), Inches(0.3), area, 12, MAROON, True)
    text(s, x + Inches(0.1), y + Inches(0.33), Inches(5.8), Inches(0.62), plan, 9.5, INK)

# 17 Order flow --------------------------------------------------------------
s = base("One order flow for every channel", "Process")
steps = ["Order in\n(internal / B2B / online / stall)", "Order system\n(tag stream & campaign)", "Production plan\n(weekly + festival calendar)",
         "Cook, QC,\npack & label", "Dispatch\n(own vehicle / courier / Amazon)", "Payment &\nfeedback", "DMTT ROI\ndashboard"]
for i, st in enumerate(steps):
    x = Inches(0.55 + i * 1.83)
    b = box(s, x, Inches(2.6), Inches(1.6), Inches(1.6), fill=[MAROON, SAFFRON, GOLD, GREEN, BLUE, SAFFRON, MAROON][i], shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.15)
    text(s, 0, 0, 0, 0, st.split("\n"), 11, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=b)
    if i < len(steps) - 1:
        a = box(s, x + Inches(1.62), Inches(3.25), Inches(0.2), Inches(0.3), fill=MUTED, shape=MSO_SHAPE.RIGHT_ARROW)
bullets(s, Inches(0.6), Inches(4.7), Inches(12.2), Inches(2.2), [
    "Internal departments: weekly minimum order, one fixed delivery day, festival top-ups entered in advance.",
    "B2B: 50% advance, sticker proof approval, locked production slot, dispatch buffer before festival.",
    "All prasadam orders go only to the in-house production lead; no outside vendors.",
], 14)

# 18 Roadmap ------------------------------------------------------------------
s = base("Roadmap: six phases from foundation to export", "Roadmap")
box(s, Inches(0.6), Inches(2.3), Inches(12.2), Inches(0.08), fill=GOLD)
for i, ph in enumerate(C.PHASES):
    x = Inches(0.6 + i * 2.05)
    dot = box(s, x + Inches(0.8), Inches(2.1), Inches(0.45), Inches(0.45), fill=[MAROON, SAFFRON, GOLD, GREEN, BLUE, MUTED][i], shape=MSO_SHAPE.OVAL)
    text(s, 0, 0, 0, 0, str(i), 13, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=dot)
    text(s, x, Inches(1.55), Inches(2.0), Inches(0.5), ph["window"].split(" (")[0], 10, MUTED, True, PP_ALIGN.CENTER)
    text(s, x, Inches(2.7), Inches(2.0), Inches(0.6), ph["name"].split("– ")[1], 13, MAROON, True, PP_ALIGN.CENTER)
    text(s, x, Inches(3.25), Inches(2.0), Inches(0.5), ph["goal"], 10, SAFFRON, True, PP_ALIGN.CENTER)
    bullets(s, x, Inches(3.85), Inches(2.0), Inches(3.1), ph["items"][:6], 9, gap=1)

# 19 First 60 days ------------------------------------------------------------
s = base("The next 60 days: Dasara and Diwali pilot", "Immediate plan")
wk = [("Week 1–2", "26 Sep – 10 Oct", ["Order data analysis", "Budgets per department", "Samples & costing", "Pricing & gift tiers", "Catalogue & stickers", "Hire 1 person", "Decision meeting 5 Oct"]),
      ("Week 3–4", "11 – 24 Oct", ["Owner meetings", "Serve 3 waiting companies", "Mahalaya & Dasara stalls", "Weekly internal orders live", "Seasonal staff"]),
      ("Week 5–6", "25 Oct – 8 Nov", ["Diwali production", "White-label dispatch", "Donor bahumana boxes", "Daily stand-ups"]),
      ("Week 7–9", "9 – 30 Nov", ["Leftovers online / Instagram", "Collect payments", "P&L + ROI", "Pilot review & go/no-go"])]
for i, (h, d, items) in enumerate(wk):
    x = Inches(0.6 + i * 3.07)
    card(s, x, Inches(1.65), Inches(2.92), Inches(5.15), f"{h} · {d}", None, head_fill=[MAROON, SAFFRON, GOLD, GREEN][i], body_items=items, size=15)

# 20 Financials chart --------------------------------------------------------
s = base("Financial outlook [estimate]", "Financials")
cd = CategoryChartData()
cd.categories = ["Year 1", "Year 2", "Year 3"]
top = sorted(C.REVENUE_Y1, key=lambda r: -r[1])
groups_fin = [("Gifting (R4, R5, R14)", ("R4", "R5", "R14")), ("Festival & restaurant (R2, R3)", ("R2", "R3")),
              ("Internal & retail (R1, R6)", ("R1", "R6")), ("Online, catering & others", ("R7", "R8", "R9", "R10", "R11", "R12"))]
for gname, ids in groups_fin:
    vals = [0, 0, 0]
    for n, v1, m2, m3, gm, _ in C.REVENUE_Y1:
        if any(f"({i})" in n for i in ids):
            vals[0] += v1
            vals[1] += v1 * m2
            vals[2] += v1 * m2 * m3
    cd.add_series(gname, [round(v) for v in vals])
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(0.6), Inches(1.55), Inches(7.4), Inches(5.3), cd)
ch = gf.chart
ch.has_legend = True
ch.legend.position = XL_LEGEND_POSITION.BOTTOM
ch.legend.include_in_layout = False
ch.legend.font.size = Pt(10)
ch.value_axis.has_major_gridlines = False
ch.value_axis.tick_labels.font.size = Pt(10)
ch.category_axis.tick_labels.font.size = Pt(11)
for ser, colr in zip(ch.series, [MAROON, SAFFRON, GOLD, BLUE]):
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = colr
ch.has_title = True
ch.chart_title.text_frame.text = "Revenue by stream group, ₹ lakh"
ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(12)
gp = sum(r[1] * r[4] / 100 for r in C.REVENUE_Y1)
ox = sum(o[1] for o in C.OPEX_Y1)
card(s, Inches(8.3), Inches(1.6), Inches(4.45), Inches(5.2), "Year 1 at a glance", None, body_items=[
    f"Revenue ≈ ₹{y1:.0f} L", f"Gross profit ≈ ₹{gp:.0f} L ({gp / y1 * 100:.0f}%)", f"Incremental opex ≈ ₹{ox} L",
    f"Net contribution ≈ ₹{gp - ox:.0f} L before capex", "Capex < ₹30 L (machines, pagodas, storage)",
    "B2B 50% advances fund the pilot", f"Year 2 ≈ ₹{y2:.0f} L · Year 3 ≈ ₹{y3:.0f} L",
    "Replace with real order data (task 2.2)"], size=12)

# 21 Org & RACI -------------------------------------------------------------
s = base("Who does what", "Team & governance")
rows = [("Role", "Person", "Responsibility")] + list(C.ORG_ROLES)
tbl = s.shapes.add_table(len(rows), 3, Inches(0.6), Inches(1.55), Inches(8.0), Inches(5.3)).table
for ci, wv in enumerate([2.9, 2.3, 2.8]):
    tbl.columns[ci].width = Inches(wv)
for ri, row in enumerate(rows):
    for ci, v in enumerate(row):
        cell = tbl.cell(ri, ci)
        cell.text = v
        r = cell.text_frame.paragraphs[0].runs[0]
        r.font.size, r.font.name, r.font.bold = Pt(9.5), FONT, ri == 0
        r.font.color.rgb = WHITE if ri == 0 else INK
        cell.fill.solid()
        cell.fill.fore_color.rgb = MAROON if ri == 0 else (WHITE if ri % 2 else PALE)
card(s, Inches(8.85), Inches(1.55), Inches(3.9), Inches(5.3), "Governance rhythm", None, head_fill=SAFFRON,
     body_items=[f"{a}: {b}" for a, b, _ in C.GOVERNANCE], size=11)

# 22 Risks ---------------------------------------------------------------------
s = base("Top risks and how we handle them", "Risk")
top_r = sorted(C.RISKS, key=lambda r: -(r[2] * r[3]))[:8]
for i, r in enumerate(top_r):
    col, row = i % 2, i // 2
    x, y = Inches(0.6 + col * 6.15), Inches(1.55 + row * 1.33)
    sc = r[2] * r[3]
    box(s, x, y, Inches(6.0), Inches(1.22), fill=WHITE, line=PALE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    badge = box(s, x + Inches(0.1), y + Inches(0.12), Inches(0.6), Inches(0.6), fill=MAROON if sc >= 15 else SAFFRON, shape=MSO_SHAPE.OVAL)
    text(s, 0, 0, 0, 0, str(sc), 13, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=badge)
    text(s, x + Inches(0.8), y + Inches(0.04), Inches(5.1), Inches(0.5), r[1], 11.5, MAROON, True)
    text(s, x + Inches(0.8), y + Inches(0.55), Inches(5.1), Inches(0.66), r[4], 10, INK)

# 23 KPIs ----------------------------------------------------------------------
s = base("'What did we get back?': one ROI dashboard", "KPIs & ROI")
for i, (k, d, u, f) in enumerate(C.KPIS):
    col, row = i % 5, i // 5
    x, y = Inches(0.6 + col * 2.46), Inches(1.6 + row * 2.1)
    box(s, x, y, Inches(2.32), Inches(1.95), fill=WHITE, line=PALE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    text(s, x + Inches(0.05), y + Inches(0.08), Inches(2.2), Inches(0.35), k, 13, SAFFRON, True)
    text(s, x + Inches(0.05), y + Inches(0.45), Inches(2.2), Inches(1.1), d, 10, INK)
    text(s, x + Inches(0.05), y + Inches(1.55), Inches(2.2), Inches(0.3), f, 9, MUTED)
text(s, Inches(0.6), Inches(5.9), Inches(12.2), Inches(0.9),
     "ROI % = (Revenue − ingredients − packaging − labour − marketing − overheads − value of hours invested) ÷ total cost × 100", 13, MAROON, True)

# 24 Ideas ----------------------------------------------------------------------
s = base("More ideas to test cheaply", "Innovation pipeline")
for i, (n, d) in enumerate(C.BUSINESS_IDEAS):
    col, row = i % 4, i // 4
    x, y = Inches(0.6 + col * 3.07), Inches(1.55 + row * 1.33)
    box(s, x, y, Inches(2.92), Inches(1.22), fill=WHITE, line=PALE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    text(s, x + Inches(0.05), y + Inches(0.03), Inches(2.8), Inches(0.3), n, 10.5, MAROON, True)
    text(s, x + Inches(0.05), y + Inches(0.47), Inches(2.8), Inches(0.75), d, 9, INK)

# 25 Asks ---------------------------------------------------------------------
s = base("Decisions needed at the 5 October meeting", "The ask")
bullets(s, Inches(0.6), Inches(1.6), Inches(6.2), Inches(5.2), C.OPEN_QUESTIONS, 14, gap=6)
card(s, Inches(7.2), Inches(1.6), Inches(5.55), Inches(5.2), "Action items this week", None, head_fill=SAFFRON,
     body_items=[f"{a[0]}: {a[1]} ({a[2]}, {a[3]})" for a in C.ACTION_ITEMS[:8]], size=11)

# 26 Close -----------------------------------------------------------------------
s = prs.slides.add_slide(BLANK)
s.background.fill.solid()
s.background.fill.fore_color.rgb = MAROON
text(s, Inches(0.9), Inches(2.3), Inches(11.5), Inches(1.2), "Somebody has to take the first bold step.", 36, WHITE, True)
text(s, Inches(0.9), Inches(3.9), Inches(11.5), Inches(1.2), "Depending on Srila Prabhupada and Krishna, let us start today: production by the temple kitchen, marketing and technology by DMTT, every result tracked.", 18, PALE)
text(s, Inches(0.9), Inches(5.6), Inches(11.5), Inches(0.5), "Hare Krishna", 20, GOLD, True)

prs.save(OUT)
print(OUT, len(prs.slides))
