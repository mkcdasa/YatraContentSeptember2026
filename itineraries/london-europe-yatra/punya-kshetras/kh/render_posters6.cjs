// Renders the headline-numbers poster (p6_*.html) to out/*.jpg (2x) and .pdf at fixed sizes.
// Usage (repo root): NODE_PATH=$(npm root -g) node itineraries/london-europe-yatra/punya-kshetras/kh/render_posters5.cjs
const path = require('path'), fs = require('fs');
const { chromium } = require('playwright');
const dir = __dirname, out = path.join(dir, 'out');
const set = (pre, tag, pals) => pals.flatMap(p => [[pre + '_countries_' + p, tag + '8-Countries-75-Attractions-' + p, 1350], [pre + '_unesco_' + p, tag + '11-UNESCO-Sites-' + p, 1350]]);
const items = [...set('p6', '', ['Brand', 'Teal-Amber']), ...set('p6b', 'Bhakti-Yatra-', ['Bhakti-Purple', 'Teal-Amber'])];
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  for (const [src, name, h] of items) {
    const p = await b.newPage({ viewport: { width: 1080, height: h }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.join(dir, src + '.html'), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    const f = name.startsWith('Bhakti-Yatra-') ? 'Bhakti-Yatra-London-Europe-Grand-Tour-2027-Poster-' + name.slice(13) : 'London-Europe-Grand-Tour-2027-Poster-' + name;
    await p.screenshot({ path: path.join(out, f + '.jpg'), type: 'jpeg', quality: 90 });
    await p.pdf({ path: path.join(out, f + '.pdf'), width: '1080px', height: h + 'px', printBackground: true, pageRanges: '1' });
    console.log(f); await p.close();
  }
  await b.close();
})();
