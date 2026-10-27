// Poster HTML -> PNG (2x) + PDF. Usage: node rposter.js poster.html out.png out.pdf
const { chromium } = require('./pw');
const path = require('path');
(async () => {
  const [,, html, png, pdf] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(html));
  await p.evaluate(() => document.fonts.ready); await p.evaluate(() => window.__fit); await p.waitForTimeout(300);
  await p.screenshot({ path: png });
  await p.pdf({ path: pdf, width: '1080px', height: '1350px', printBackground: true, pageRanges: '1' });
  await b.close();
})();
