// Renders kh/brochure_kh.html to kh/out/<name>.pdf and page previews kh/build/page-NN.png; reports overflowing boxes.
// Usage (repo root): NODE_PATH=$(npm root -g) node itineraries/london-europe-yatra/punya-kshetras/kh/render_kh.cjs
const path = require('path'), fs = require('fs');
const { chromium } = require('playwright');
const dir = __dirname, out = path.join(dir, 'out'), prev = path.join(dir, 'build');
const name = 'London-Europe-Grand-Tour-17-April-2-May-2027-Brochure';
(async () => {
  fs.mkdirSync(out, { recursive: true }); fs.mkdirSync(prev, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1.4 });
  await p.goto('file://' + path.join(dir, 'brochure_kh.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const over = await p.evaluate(() => {
    const r = [];
    document.querySelectorAll('.page').forEach((pg, i) => {
      const pb = pg.getBoundingClientRect(); const foot = pg.querySelector('.foot').getBoundingClientRect().top;
      pg.querySelectorAll('.card,.dc,.dph,.iec,.cn,.tc,.cy,.tp,.wy,.mos,.scs,.cns,.tcs,.map,.mapnote,.unesco,.exs,.dd,.crs,.crn,.visa,.pmgrid').forEach(el => {
        const e = el.getBoundingClientRect();
        if (e.bottom > foot + 2 && !el.closest('.cover') && !el.closest('.back')) r.push(`page ${i + 1}: ${el.className} bottom ${Math.round(e.bottom - pb.top)} > footer ${Math.round(foot - pb.top)}`);
        if (el.scrollHeight > el.clientHeight + 2 && getComputedStyle(el).overflow === 'hidden') r.push(`page ${i + 1}: ${el.className} clipped`);
      });
    });
    return r;
  });
  over.forEach(x => console.log('OVERFLOW', x));
  await p.pdf({ path: path.join(out, name + '.pdf'), preferCSSPageSize: true, printBackground: true });
  const pages = await p.$$('.page');
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.join(prev, `page-${String(i + 1).padStart(2, '0')}.png`) });
  await b.close(); console.log('pages', pages.length, '→', path.join(out, name + '.pdf'));
})();
