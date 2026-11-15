// Renders the two-part poster sets (p4_*.html) to out/*.jpg (2x) and .pdf at fixed sizes.
// Usage (repo root): NODE_PATH=$(npm root -g) node itineraries/london-europe-yatra/punya-kshetras/kh/render_posters4.cjs
const path = require('path'), fs = require('fs');
const { chromium } = require('playwright');
const dir = __dirname, out = path.join(dir, 'out');
const items = ['bollywood','unesco','top10','passport'].flatMap(n => [['p4_'+n+'_1', n+'-Part-1-of-2', 1350], ['p4_'+n+'_2', n+'-Part-2-of-2', 1350]]);
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  for (const [src, name, h] of items) {
    const p = await b.newPage({ viewport: { width: 1080, height: h }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.join(dir, src + '.html'), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    const f = 'London-Europe-Grand-Tour-2027-Poster-' + name;
    await p.screenshot({ path: path.join(out, f + '.jpg'), type: 'jpeg', quality: 90 });
    await p.pdf({ path: path.join(out, f + '.pdf'), width: '1080px', height: h + 'px', printBackground: true, pageRanges: '1' });
    console.log(f); await p.close();
  }
  await b.close();
})();
