// Renders html/photo_poster.html into a 2-page A4 PDF and one JPG per page (marketing/out/).
// Usage: node marketing/render_photo_poster.cjs   (YATRA_BRAND=bhakti for the Bhakti Yatra version)
const path = require('path');
const { chromium } = require('playwright');

const BHAKTI = process.env.YATRA_BRAND === 'bhakti';
const out = path.join(__dirname, BHAKTI ? 'out/bhakti-yatra' : 'out');
const PRE = BHAKTI ? 'Bhakti_Yatra_London_Europe_Yatra_2027' : 'London_Europe_Yatra_2027';
const W = 794, H = 1123; // A4 at 96 px per inch

(async () => {
  require('fs').mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 3 });
  await page.goto('file://' + path.join(__dirname, 'html', (BHAKTI ? 'bhakti_' : '') + 'photo_poster.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: path.join(out, `${PRE}_Poster_2_pages.pdf`), format: 'A4', printBackground: true, preferCSSPageSize: true });
  const pages = await page.$$('section.page');
  for (let i = 0; i < pages.length; i++) {
    await pages[i].screenshot({ path: path.join(out, `${PRE}_Poster_page_${i + 1}.jpg`), type: 'jpeg', quality: 90 });
  }
  await browser.close();
  console.log('rendered', pages.length, 'pages to', out);
})();
