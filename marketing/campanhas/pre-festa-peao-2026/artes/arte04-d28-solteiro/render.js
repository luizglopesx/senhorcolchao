const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto(`file://${path.join(dir, 'peca.html')}`, { waitUntil: 'networkidle' });

  const targets = [
    { id: '#feed',  file: 'feed.png' },
    { id: '#story', file: 'story.png' },
  ];

  for (const t of targets) {
    const el = await page.$(t.id);
    await el.screenshot({ path: path.join(dir, t.file) });
    console.log(`✓ ${t.file}`);
  }

  await browser.close();
  console.log('\nPronto!');
})();
