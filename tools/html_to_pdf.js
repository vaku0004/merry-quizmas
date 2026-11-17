// node tools/html_to_pdf.js <page.html> <out.pdf> [footer html]
// Renders a local HTML file to a US Letter PDF with Playwright (Chromium). Used by tools/make_pdf.py.
const {chromium} = require('playwright');
const {pathToFileURL} = require('url');
const path = require('path');
const [, , src, out, footer] = process.argv;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto(pathToFileURL(path.resolve(src)).href, {waitUntil: 'load'});
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({path: out, format: 'Letter', printBackground: true, preferCSSPageSize: true,
               displayHeaderFooter: !!footer, headerTemplate: '<div></div>', footerTemplate: footer || '<div></div>',
               margin: {top: '0.55in', bottom: '0.7in', left: '0.6in', right: '0.6in'}});
  await b.close();
})();
