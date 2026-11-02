// Renders the HTML from build_marketing.py into JPG posters and PDFs (marketing/out/).
// Usage: node marketing/render.cjs   (YATRA_BRAND=bhakti for the Bhakti Yatra versions)
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const html = path.join(__dirname, 'html');
const BHAKTI = process.env.YATRA_BRAND === 'bhakti';
const out = path.join(__dirname, BHAKTI ? 'out/bhakti-yatra' : 'out');
const HP = BHAKTI ? 'bhakti_' : '';
const PRE = BHAKTI ? 'Bhakti_Yatra_London_Europe_Yatra_2027' : 'London_Europe_Yatra_2027';

const POSTERS = [
  ['poster_1_main', 1080, 1350],
  ['poster_2_itinerary', 1080, 1350],
  ['poster_3_price', 1080, 1350],
  ['poster_4_story', 1080, 1920],
];

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  for (const [name, w, h] of POSTERS) {
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    await page.goto('file://' + path.join(html, HP + name + '.html'), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(out, `${PRE}_${name}.jpg`), type: 'jpeg', quality: 92 });
    await page.pdf({ path: path.join(out, `${PRE}_${name}.pdf`), width: `${w}px`, height: `${h}px`, printBackground: true });
    await page.close();
  }
  const page = await browser.newPage();
  await page.goto('file://' + path.join(html, HP + 'brochure.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: path.join(out, `${PRE}_Brochure.pdf`), format: 'A4', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('rendered to', out);
})();
