// Renders lang/poster_<code>.html into JPG + PDF (marketing/out/lang/).
// Usage: node marketing/lang/render_lang.cjs
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const out = path.join(__dirname, '..', 'out', 'lang');
const LANGS = { te: 'Telugu', hi: 'Hindi', kn: 'Kannada', ta: 'Tamil' };

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  for (const [code, name] of Object.entries(LANGS)) {
    const page = await browser.newPage({ viewport: { width: 1131, height: 1600 }, deviceScaleFactor: 2 });
    await page.goto('file://' + path.join(__dirname, `poster_${code}.html`), { waitUntil: 'networkidle' });
    await page.waitForFunction(() => document.body.dataset.ready === '1');
    const base = path.join(out, `London_Europe_Yatra_2027_Poster_${name}`);
    await page.screenshot({ path: base + '.jpg', type: 'jpeg', quality: 92 });
    await page.pdf({ path: base + '.pdf', width: '1131px', height: '1600px', printBackground: true, pageRanges: '1' });
    await page.close();
  }
  await browser.close();
  console.log('rendered', Object.keys(LANGS).length, 'posters to', out);
})();
