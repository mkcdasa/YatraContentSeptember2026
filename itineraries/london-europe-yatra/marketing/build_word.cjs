// Builds the shareable Word document (detailed itinerary and all yatri information)
// from word_data.json. Usage: node marketing/build_word.cjs
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  HeadingLevel, AlignmentType, BorderStyle, ExternalHyperlink, Header, Footer, PageNumber,
  LevelFormat, PageBreak, VerticalAlign,
} = require('docx');

const D = JSON.parse(fs.readFileSync(path.join(__dirname, 'word_data.json'), 'utf8'));
const OUT = path.join(__dirname, 'out', 'London_Europe_Yatra_2027_Detailed_Itinerary.docx');

const MAROON = '6B1414', GOLD = 'B8860B', SAFFRON = 'E8891D', MUTED = '6E5A4B';
const W = 9866; // A4 width minus 2 × 1020 margins
const FONT = 'Calibri';
const border = { style: BorderStyle.SINGLE, size: 4, color: 'D9C7A6' };
const borders = { top: border, bottom: border, left: border, right: border };

const t = (text, o = {}) => new TextRun({ text, font: FONT, ...o });
const p = (children, o = {}) => new Paragraph({ children: typeof children === 'string' ? [t(children)] : children, spacing: { after: 100 }, ...o });
const h1 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [t(text)] });
const h2 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [t(text)] });
const h3 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [t(text)] });
const bullet = (children) => new Paragraph({ numbering: { reference: 'bul', level: 0 }, spacing: { after: 40 },
  children: typeof children === 'string' ? [t(children)] : children });
const link = (text, url, size) => new ExternalHyperlink({ link: url, children: [t(text, { style: 'Hyperlink', size })] });
const brk = () => new Paragraph({ children: [new PageBreak()] });

function cell(content, width, o = {}) {
  const paras = (Array.isArray(content) ? content : [content]).map((c) =>
    c instanceof Paragraph ? c : new Paragraph({ spacing: { after: 0 }, children: typeof c === 'string' ? [t(c, { size: o.size || 18, bold: o.bold, color: o.color })] : c }));
  return new TableCell({
    children: paras, width: { size: width, type: WidthType.DXA }, borders,
    margins: { top: 50, bottom: 50, left: 90, right: 90 }, verticalAlign: VerticalAlign.TOP,
    shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR, color: 'auto' } : undefined,
    columnSpan: o.span,
  });
}

function table(widths, header, rows, o = {}) {
  const head = new TableRow({ tableHeader: true, children: header.map((h, i) => cell(h, widths[i], { fill: MAROON, color: 'FFFFFF', bold: true, size: o.size || 18 })) });
  const body = rows.map((r, ri) => new TableRow({ cantSplit: true, children: r.map((c, i) => cell(c, widths[i], { size: o.size || 18, fill: (o.fills && o.fills[ri]) || (ri % 2 ? 'FBF6EC' : undefined) })) }));
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: widths, rows: [head, ...body] });
}

const kv = (rows) => new Table({
  width: { size: W, type: WidthType.DXA }, columnWidths: [2600, W - 2600],
  rows: rows.map(([k, v]) => new TableRow({ children: [cell(k, 2600, { bold: true, fill: 'F6EBD6', size: 20 }), cell(v, W - 2600, { size: 20 })] })),
});

const monthName = (d) => (d.slice(5, 7) === '04' ? 'April' : 'May');
const dayDate = (d) => `${d.dow} ${parseInt(d.date.slice(8), 10)} ${monthName(d.date)} 2027`;
const children = [];

// ---------------------------------------------------------------- cover
children.push(
  new Paragraph({ spacing: { before: 1800, after: 120 }, alignment: AlignmentType.CENTER, children: [t('HARE KRISHNA GOLDEN TEMPLE · HYDERABAD', { color: GOLD, bold: true, size: 22, characterSpacing: 40 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [t('London Europe Yatra 2027', { font: 'Georgia', bold: true, size: 64, color: MAROON })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 }, children: [t('Detailed itinerary and yatri information', { font: 'Georgia', italics: true, size: 30, color: MUTED })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 }, children: [t('17 April – 2 May 2027 · 15 nights / 16 days', { bold: true, size: 30, color: SAFFRON })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 }, children: [t(D.yatra.countries.join(' · '), { size: 22 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [t(`${D.price.base} per person, including international flights`, { bold: true, size: 32, color: MAROON })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 900 }, children: [t('+ 5% GST + 2% TCS (TCS refunded or credited through your income-tax return)', { size: 20, color: MUTED })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [t(D.yatra.organiser, { size: 20 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [t(D.yatra.contact, { size: 20, bold: true })] }),
  brk(),
);

// ---------------------------------------------------------------- contents
children.push(h1('Contents'),
  ...['1. The yatra at a glance', '2. Yatra amount, inclusions and exclusions', '3. Flights', '4. Day-by-day summary, hotels and a typical day',
    '5. Detailed itinerary – Day 1 to Day 16 (times, places, map links, distances)', '6. Meal plan', '7. Visa and documents',
    '8. Practical information and things to be aware of', "9. Do's and don'ts", '10. Entry tickets and booking', '11. Contact and booking']
    .map((x) => p([t(x, { size: 22 })], { spacing: { after: 120 } })),
  brk());

// ---------------------------------------------------------------- 1. at a glance
children.push(h1('1. The yatra at a glance'),
  p('A 16-day pilgrimage and sightseeing tour with Hare Krishna devotees through eight countries. The group takes darshan at ten ISKCON temples, visits the Akshaya Patra kitchen in Watford, and sees the great sights of London, Paris, the Netherlands, Switzerland and Italy. All meals are Satvik prasadam, and the group travels together in one private coach with a tour manager.'),
  kv([
    ['Dates', '17 April – 2 May 2027 (15 nights / 16 days)'],
    ['Countries', D.yatra.countries.join(', ')],
    ['Route', 'London (3 nights) → Paris (2) → Brussels → Amsterdam → Cologne → Black Forest (Titisee) → Zurich → Interlaken → Milan → Venice-Mestre → Florence → near Milan Malpensa. Rome and the Vatican are a high-speed-train day on 30 April.'],
    ['Departure cities', 'Hyderabad and Bangalore (flights into London Heathrow; home from Milan Malpensa)'],
    ['Temples', D.temples.join(', ')],
    ['Yatra amount', `${D.price.base} per person, including international flights, + 5% GST + 2% TCS`],
    ['Meals', 'Breakfast, lunch and dinner every day: Satvik prasadam, no onion or garlic. Ekadasi meals on 17 April and 2 May.'],
    ['Organiser', `${D.yatra.organiser}. ${D.yatra.contact}`],
  ]),
);

// ---------------------------------------------------------------- 2. price
children.push(h1('2. Yatra amount, inclusions and exclusions'),
  p([t(`${D.price.base} per person, including international flights`, { bold: true }), t(', plus 5% GST and 2% TCS.')]),
  table([6000, W - 6000], ['What you pay (per person)', 'Amount'], [
    ['Yatra amount', D.price.base], ['GST 5%', D.price.gst], ['Sub-total', D.price.subtotal],
    ['TCS 2% (refunded or credited through your income-tax return)', D.price.tcs],
    [[new Paragraph({ children: [t('Total paid', { bold: true, size: 18 })] })], [new Paragraph({ children: [t(D.price.total, { bold: true, size: 18 })] })]],
  ]),
  p([t('TCS (Tax Collected at Source) is deposited against your PAN. You get it back as a refund, or as credit against your tax, when you file your income-tax return. A PAN is needed for the booking.', { size: 18, color: MUTED })], { spacing: { before: 80, after: 160 } }),
  h2('Included'), ...D.inclusions.map(bullet),
  h2('Not included'), bullet('GST 5% and TCS 2%'), ...D.exclusions.map(bullet),
);

// ---------------------------------------------------------------- 3. flights
const flightRows = [];
for (const d of [D.days[0], D.days[15]]) for (const r of d.rows) if (r.what.startsWith('Flight') || /EY 82|EY 352|EY 232/.test(r.detail)) flightRows.push([dayDate(d), r.time, r.detail]);
children.push(h1('3. Flights'),
  p('Shortlisted 2027 schedules. Flight numbers and times may change before ticketing. Times are local.'),
  table([2000, 1500, W - 3500], ['Date', 'Time', 'Flight'], flightRows),
);

// ---------------------------------------------------------------- 4. summary
children.push(h1('4. Day-by-day summary'),
  table([700, 1500, 4766, 1900, 1000], ['Day', 'Date', 'Route and highlights', 'Overnight', 'Coach km'],
    D.days.map((d) => [String(d.day), `${d.dow} ${parseInt(d.date.slice(8), 10)} ${monthName(d.date).slice(0, 3)}`, d.title, d.overnight, d.coach_km ? String(d.coach_km) : '—'])),
  h2('Hotels'), ...D.hotels.map(([c, n]) => bullet(`${c}: ${n} night${n > 1 ? 's' : ''}`)),
  p([t('Hotel names are confirmed closer to departure.', { italics: true, size: 18, color: MUTED })]),
  h2('A typical day'),
  bullet('07:30–08:00 morning programme in the hotel: japa, short kirtan and Bhagavatam reading (optional)'),
  bullet('08:00–09:00 breakfast at the hotel'),
  bullet('09:00 coach leaves the hotel; sightseeing and temple darshan with narration in Telugu, Hindi and English'),
  bullet('Lunch at an Indian restaurant or a temple near the sightseeing'),
  bullet('Evening arati at a temple where possible; dinner at the hotel; next-day briefing'),
  p('Exceptions: Day 14 (Rome) starts at 05:00 for the 06:30 train, and Day 16 starts at 06:30 for the 11:40 flight.'),
  brk(),
);

// ---------------------------------------------------------------- 5. detailed
children.push(h1('5. Detailed itinerary'),
  p('Every movement and visit, with times, distances and a Google Maps link for each place or route. Shaded rows are meals; grey rows are transfers. Times are local.'));
const COLS = [1150, 1400, 2650, W - 5200];
D.days.forEach((d, i) => {
  if (i) children.push(brk());
  children.push(h2(`Day ${d.day} · ${dayDate(d)}`),
    p([t(d.short, { bold: true, color: MAROON })], { spacing: { after: 60 } }),
    p(d.summary),
    p([t(`Overnight: ${d.overnight}`, { bold: true, size: 18 }),
      t(d.coach_km ? `   ·   Coach: about ${d.coach_km} km` : '', { size: 18 }),
      t(d.walk_km ? `   ·   Walking between stops: about ${d.walk_km} km` : '', { size: 18 })]));
  const fills = d.rows.map((r) => (r.meal ? 'FFF1D6' : r.move ? 'F3EEE7' : 'FFFFFF'));
  const rows = d.rows.map((r) => [
    r.time, r.what,
    [new Paragraph({ children: [link(r.where, r.link, 17)] })],
    [new Paragraph({ children: [t(r.detail, { size: 17 })] }),
      ...(r.note ? [new Paragraph({ spacing: { before: 40 }, children: [t('Note: ', { bold: true, size: 16, color: MUTED }), t(r.note, { size: 16, color: MUTED, italics: true })] })] : [])],
  ]);
  children.push(table(COLS, ['Time', 'Activity', 'Place / route (map link)', 'Details'], rows, { size: 17, fills }));
});
children.push(brk());

// ---------------------------------------------------------------- 6. meals
children.push(h1('6. Meal plan'),
  p('All meals are Satvik: no onion, garlic, eggs, meat or fish. Breakfast is at the hotel; lunch is at a temple or an Indian restaurant near the sightseeing; dinner is at the hotel.'),
  table([700, 2900, 3133, W - 6733], ['Day', 'Breakfast', 'Lunch', 'Dinner'],
    D.days.map((d) => [String(d.day), d.meals.Breakfast, d.meals.Lunch, d.meals.Dinner]), { size: 16 }),
);

// ---------------------------------------------------------------- 7. visa
children.push(h1('7. Visa and documents'),
  p('Two visas are needed: the UK Standard Visitor visa and a Schengen visa (applied through Italy). Start collecting documents now.'),
  table([2600, W - 2600], ['Document', 'What is needed'], D.visa.map(([a, b]) => [a, b])),
);

// ---------------------------------------------------------------- 8. practical
children.push(h1('8. Practical information'),
  table([2600, W - 2600], ['Topic', 'Details'], D.practical.map(([a, b]) => [a, b])),
  h2('Things to be aware of'),
  table([2400, 3600, W - 6000], ['Topic', 'What to expect', 'How we handle it'], D.challenges.map((c) => [c[0], c[1], c[2]]), { size: 17 }),
);

// ---------------------------------------------------------------- 9. dos
children.push(h1("9. Do's and don'ts"), h2('Do'), ...D.dos.map(bullet), h2("Don't"), ...D.donts.map(bullet));

// ---------------------------------------------------------------- 10. booking
children.push(brk(), h1('10. Entry tickets and booking'),
  p('All entry tickets marked "Included" are part of the yatra amount and are booked by the organisers on the official sites below. Optional extras can be added on request.'),
  table([700, 3400, 1300, W - 5400], ['Day', 'Place', 'Status', 'Official site and group rules'],
    D.booking.map(([day, place, url, rules]) => {
      const status = /\(optional/i.test(place) ? 'Optional' : 'Included';
      return [String(day), place, status, [new Paragraph({ children: [link(url.replace(/^https?:\/\/(www\.)?/, '').replace(/\/$/, ''), url, 16)] }), new Paragraph({ children: [t(rules, { size: 16 })] })]];
    }), { size: 17 }),
);

// ---------------------------------------------------------------- contact
children.push(h1('11. Contact and booking'),
  p([t('To reserve a seat, call or WhatsApp ', {}), t('+91 95053 88886', { bold: true }), t('.')]),
  p(`${D.yatra.organiser}`), p(D.yatra.contact),
  p([t('Seats are limited to one coach. The itinerary may change slightly for operational reasons (weather, strikes, opening hours). Payment schedule and cancellation terms are on the booking form.', { italics: true, size: 18, color: MUTED })]),
);

const doc = new Document({
  creator: 'Hare Krishna Golden Temple, Hyderabad',
  title: 'London Europe Yatra 2027 – Detailed itinerary',
  styles: {
    default: { document: { run: { font: FONT, size: 20 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: 'Georgia', size: 34, bold: true, color: MAROON }, paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: 'Georgia', size: 26, bold: true, color: '8E1F1A' }, paragraph: { spacing: { before: 220, after: 100 }, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT, size: 22, bold: true, color: MAROON }, paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [{ reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 260 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1000, bottom: 1000, left: 1020, right: 1020 } }, titlePage: true },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [t('London Europe Yatra 2027 · 17 April – 2 May 2027', { size: 16, color: MUTED })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [t('Hare Krishna Golden Temple, Hyderabad · +91 95053 88886 · page ', { size: 16, color: MUTED }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: MUTED, font: FONT })] })] }) },
    children,
  }],
});

fs.mkdirSync(path.dirname(OUT), { recursive: true });
Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(OUT, buf); console.log('wrote', OUT); });
