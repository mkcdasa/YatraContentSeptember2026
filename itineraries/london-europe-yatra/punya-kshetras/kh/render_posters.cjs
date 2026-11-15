// Renders poster_single / poster_part1 / poster_part2 to out/*.jpg (2x) and .pdf; height fits the content.
// Usage (repo root): NODE_PATH=$(npm root -g) node itineraries/london-europe-yatra/punya-kshetras/kh/render_posters.cjs
const path = require('path'), fs = require('fs');
const { chromium } = require('playwright');
const dir = __dirname, out = path.join(dir, 'out');
const items = [['poster_single', 'London-Europe-Grand-Tour-2027-Poster-Single'],
               ['poster_part1', 'London-Europe-Grand-Tour-2027-Poster-Part-1-of-2'],
               ['poster_part2', 'London-Europe-Grand-Tour-2027-Poster-Part-2-of-2']];
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  for (const [src, name] of items) {
    const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.join(dir, src + '.html'), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    const h = await p.evaluate(() => {
      const po = document.querySelector('.po'); const top = po.getBoundingClientRect().top;
      let m = 0; for (const el of po.children) { if (el.classList.contains('cta') || el.classList.contains('pg')) continue; m = Math.max(m, el.getBoundingClientRect().bottom - top); }
      const H = Math.ceil(m + 160); po.style.height = H + 'px'; return H;
    });
    await p.setViewportSize({ width: 1080, height: h });
    await p.screenshot({ path: path.join(out, name + '.jpg'), type: 'jpeg', quality: 90, clip: { x: 0, y: 0, width: 1080, height: h } });
    await p.pdf({ path: path.join(out, name + '.pdf'), width: '1080px', height: h + 'px', printBackground: true, pageRanges: '1' });
    console.log(name, '1080 x', h); await p.close();
  }
  await b.close();
})();
