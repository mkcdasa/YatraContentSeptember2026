// Prints pdf_build/cover.html and pdf_build/body.html to PDF with headless Chromium.
// Usage: node render_pdf.mjs   (PLAYWRIGHT_MODULE and CHROME env vars are optional)
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const mod = process.env.PLAYWRIGHT_MODULE || 'playwright';
const { chromium } = await import(mod.startsWith('/') ? pathToFileURL(mod).href : mod);
const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), 'pdf_build');
const browser = await chromium.launch({ executablePath: process.env.CHROME || undefined });
const page = await browser.newPage();

// --pages in.html=out.pdf ... : print arbitrary pages (used by build_pdfs.py)
const at = process.argv.indexOf('--pages');
if (at > -1) {
  for (const pair of process.argv.slice(at + 1)) {
    const [src, out] = pair.split('=');
    await page.goto(pathToFileURL(src).href, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.querySelectorAll('li').forEach(l => l.classList.add('open')));
    await page.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true,
      headerTemplate: '<span></span>',
      footerTemplate: `<div style="width:100%;font-family:'Noto Sans',sans-serif;font-size:7.5px;color:#6B5E55;padding:0 14mm;display:flex;justify-content:space-between"><span>Prasadam, Sweets &amp; Savories Vertical</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>` });
  }
  await browser.close();
  process.exit(0);
}

await page.goto(pathToFileURL(path.join(dir, 'cover.html')).href);
await page.pdf({ path: path.join(dir, 'cover.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });

await page.goto(pathToFileURL(path.join(dir, 'body.html')).href, { waitUntil: 'networkidle' });
const footer = `<div style="width:100%;font-family:'Noto Sans',sans-serif;font-size:7.5px;color:#6B5E55;padding:0 16mm;display:flex;justify-content:space-between">
  <span>Prasadam, Sweets &amp; Savories Vertical · Leadership business plan · Confidential</span>
  <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>`;
await page.pdf({ path: path.join(dir, 'body.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true,
  displayHeaderFooter: true, headerTemplate: '<span></span>', footerTemplate: footer });
await browser.close();
console.log('pdf pages rendered');
