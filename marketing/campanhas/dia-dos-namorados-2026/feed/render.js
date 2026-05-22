const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const dir = __dirname;
  const outDir = path.join(dir, 'instagram');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir);

  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.setViewportSize({ width: 1080, height: 1350 });
  await page.goto(`file://${path.join(dir, 'posts.html')}`, { waitUntil: 'networkidle' });

  const slides = await page.$$('.slide');
  console.log(`Renderizando ${slides.length} posts...`);

  for (let i = 0; i < slides.length; i++) {
    const num = String(i + 1).padStart(2, '0');
    const file = path.join(outDir, `post-${num}.png`);
    await slides[i].screenshot({ path: file });
    console.log(`✓ post-${num}.png`);
  }

  await browser.close();
  console.log(`\nPronto! ${slides.length} posts em instagram/`);
})();
