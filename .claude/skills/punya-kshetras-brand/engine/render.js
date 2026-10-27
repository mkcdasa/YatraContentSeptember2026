// Brochure HTML -> A4 PDF (waits for the auto-fit script). Usage: node render.js page.html out.pdf [png-prefix]
const { chromium } = require('./pw');
const path = require('path');
(async () => {
  const [,, html, pdf, prev] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(html), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready); await p.evaluate(() => window.__fit); await p.waitForTimeout(300);
  if (pdf) await p.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true });
  if (prev) {
    const n = await p.$$eval('.page', e => e.length);
    for (let i = 0; i < n; i++) {
      const el = (await p.$$('.page'))[i];
      await el.screenshot({ path: `${prev}-${String(i + 1).padStart(2, '0')}.png` });
    }
  }
  await b.close();
})();
