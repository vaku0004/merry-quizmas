// node tools/html_to_pdf.js <page.html> <out.pdf> [footer html] [preview prefix]
// Renders a local HTML file to a US Letter PDF with Playwright (Chromium). Used by tools/make_pdf.py.
// With a preview prefix it also screenshots two "pages" as PNG (<prefix>-1.png the cover page, <prefix>-2.png the
// answer key page) for the preview picture on the site; make_pdf.py composes them.
const {chromium} = require('playwright');
const {pathToFileURL} = require('url');
const path = require('path');
const [, , src, out, footer, preview] = process.argv;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  const url = pathToFileURL(path.resolve(src)).href;
  await p.goto(url, {waitUntil: 'load'});
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({path: out, format: 'Letter', printBackground: true, preferCSSPageSize: true,
               displayHeaderFooter: !!footer, headerTemplate: '<div></div>', footerTemplate: footer || '<div></div>',
               margin: {top: '0.55in', bottom: '0.7in', left: '0.6in', right: '0.6in'}});
  if (preview) {
    // US Letter at 96 dpi = 816 x 1056; the page margins become padding so the text wraps as in the PDF
    const v = await b.newPage({viewport: {width: 816, height: 1056}, deviceScaleFactor: 1.5});
    await v.emulateMedia({media: 'print'});
    await v.goto(url, {waitUntil: 'load'});
    await v.addStyleTag({content: 'html,body{background:#fff}body{width:816px;padding:0.55in 0.6in 0.7in;margin:0}.part{break-before:auto}'});
    await v.evaluate(() => document.fonts.ready);
    await v.screenshot({path: `${preview}-1.png`, clip: {x: 0, y: 0, width: 816, height: 1056}});
    await v.addStyleTag({content: 'body>:not(.part){display:none}'});   // page 2: the answer key alone, from its top
    await v.screenshot({path: `${preview}-2.png`, clip: {x: 0, y: 0, width: 816, height: 1056}});
  }
  await b.close();
})();
