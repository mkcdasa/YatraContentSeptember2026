// NODE_PATH=$(npm root -g) node itineraries/london-europe-yatra/route_optimised/render.cjs
const path = require('path'); const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.join(__dirname, 'route_optimised.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const out = path.join(__dirname, 'London_Europe_Grand_Tour_2027_Route_Optimised_Itinerary.pdf');
  await p.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#888">London &amp; Europe Grand Tour 2027 · Route-optimised itinerary · page <span class="pageNumber"></span> of <span class="totalPages"></span></div>',
    margin: { top: '12mm', bottom: '14mm', left: '12mm', right: '12mm' } });
  console.log(out); await b.close(); })();
