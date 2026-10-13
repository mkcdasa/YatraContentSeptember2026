// Pre-renders diagrams/*.mmd to SVG and PNG with Mermaid in headless Chromium.
// Usage: node render_diagrams.mjs <path-to-mermaid.min.js>
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'diagrams');
const browser = await chromium.launch({ executablePath: process.env.CHROME || undefined });
const page = await browser.newPage({ viewport: { width: 1800, height: 1200 }, deviceScaleFactor: 2 });
await page.setContent('<html><body style="margin:0;background:#fff"><div id="o"></div></body></html>');
await page.addScriptTag({ path: process.argv[2] });
await page.evaluate(() => mermaid.initialize({ startOnLoad: false, theme: 'base', themeVariables: {
  primaryColor: '#FBEBD0', primaryBorderColor: '#7A1F2B', primaryTextColor: '#2B221E', lineColor: '#7A1F2B',
  secondaryColor: '#FFF8EC', tertiaryColor: '#FFFFFF', fontFamily: 'Liberation Sans, Arial, sans-serif', fontSize: '15px' } }));
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.mmd'))) {
  const slug = f.replace('.mmd', '');
  const code = fs.readFileSync(path.join(dir, f), 'utf8');
  const svg = await page.evaluate(async ([c, id]) => (await mermaid.render(id, c)).svg, [code, 'd_' + slug]);
  fs.writeFileSync(path.join(dir, slug + '.svg'), svg);
  await page.evaluate(s => { document.getElementById('o').innerHTML = s; }, svg);
  await (await page.$('#o svg')).screenshot({ path: path.join(dir, slug + '.png') });
  console.log('rendered', slug);
}
await browser.close();
