// Lists brochure pages whose content overflows. Usage: node chk.js page.html  -> prints "page.html [ ]" when clean
const { chromium } = require('./pw');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  for (const f of process.argv.slice(2)) {
    const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
    await p.goto('file://' + path.resolve(f));
    await p.evaluate(() => window.__fit); await p.waitForTimeout(300);
    const bad = await p.$$eval('.page', ps => ps.map((pg, i) => { const b = pg.querySelector('.body'); return b && b.scrollHeight > b.clientHeight + 1 ? i + 1 : 0 }).filter(x => x));
    console.log(f, JSON.stringify(bad));
    if (bad.length) process.exitCode = 3;
  }
  await b.close();
})();
