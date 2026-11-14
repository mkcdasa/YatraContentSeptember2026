// Itinerary HTML -> A4 PDF with a page-number footer. Usage: node ryatri.js itinerary.html out.pdf
const { chromium } = require('./pw');
const path = require('path');
const fs = require('fs');
(async () => {
  const [,, html, pdf] = process.argv;
  let foot = 'Punya Kshetras by Hare Krishna Golden Temple';
  try { const c = JSON.parse(fs.readFileSync('brand.json', 'utf8')); foot += ' · Call ' + c.phone; } catch (e) {}
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(html), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: `<div style="width:100%;font-size:7px;color:#6E6077;padding:0 13mm;display:flex;justify-content:space-between;font-family:sans-serif"><span>${foot}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>` });
  await b.close();
})();
