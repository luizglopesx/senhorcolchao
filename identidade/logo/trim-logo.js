const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const logoPath = path.join(__dirname, 'logo-completa.png');
  const logoB64 = fs.readFileSync(logoPath).toString('base64');
  const dataUrl = `data:image/png;base64,${logoB64}`;

  await page.setContent(`
    <html>
    <body style="margin:0;padding:0;background:transparent;">
      <canvas id="c"></canvas>
      <script>
        const img = new Image();
        img.onload = function() {
          const c = document.getElementById('c');
          c.width = img.width;
          c.height = img.height;
          const ctx = c.getContext('2d');
          ctx.drawImage(img, 0, 0);
          const data = ctx.getImageData(0, 0, img.width, img.height).data;
          let minX = img.width, minY = img.height, maxX = 0, maxY = 0;
          for (let y = 0; y < img.height; y++) {
            for (let x = 0; x < img.width; x++) {
              const alpha = data[(y * img.width + x) * 4 + 3];
              if (alpha > 10) {
                if (x < minX) minX = x;
                if (y < minY) minY = y;
                if (x > maxX) maxX = x;
                if (y > maxY) maxY = y;
              }
            }
          }
          window._bounds = { minX, minY, maxX, maxY, w: img.width, h: img.height };
        };
        img.src = '${dataUrl}';
      </script>
    </body></html>
  `);

  await page.waitForFunction(() => window._bounds !== undefined, { timeout: 10000 });
  const bounds = await page.evaluate(() => window._bounds);
  console.log('Bounds encontrados:', bounds);

  const pad = 8;
  const cx = Math.max(0, bounds.minX - pad);
  const cy = Math.max(0, bounds.minY - pad);
  const cw = Math.min(bounds.w, bounds.maxX + pad + 1) - cx;
  const ch = Math.min(bounds.h, bounds.maxY + pad + 1) - cy;
  console.log(`Crop: x=${cx} y=${cy} w=${cw} h=${ch}`);

  // Renderiza a logo com fundo transparente e recortada
  await page.setViewportSize({ width: bounds.w, height: bounds.h });
  const out = path.join(__dirname, 'logo-completa-trim.png');
  await page.screenshot({
    path: out,
    clip: { x: cx, y: cy, width: cw, height: ch },
    omitBackground: true
  });

  console.log(`\nSalvo: logo-completa-trim.png  ${cw}x${ch}px`);
  await browser.close();
})();
