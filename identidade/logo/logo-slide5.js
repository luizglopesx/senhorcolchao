const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// Gera versão da logo com "Sleep Store" em branco (para usar em fundo amarelo)
// Estratégia: pixels amarelos no lado direito da imagem (onde está o texto) → branco
// O círculo amarelo do mascote fica no lado esquerdo e é preservado

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const logoPath = path.join(__dirname, 'logo-completa-trim.png');
  const logoB64 = fs.readFileSync(logoPath).toString('base64');
  const dataUrl = `data:image/png;base64,${logoB64}`;

  await page.setContent(`
    <html><body style="margin:0;padding:0;background:transparent;">
      <canvas id="c"></canvas>
      <script>
        const img = new Image();
        img.onload = function() {
          const c = document.getElementById('c');
          c.width = img.width;
          c.height = img.height;
          const ctx = c.getContext('2d');
          ctx.drawImage(img, 0, 0);

          const imageData = ctx.getImageData(0, 0, img.width, img.height);
          const data = imageData.data;

          // Mascote (círculo amarelo) ocupa aprox. x=0 a x=265px
          // Texto "Sr. Colchão" e "Sleep Store" começa em x≈280px
          // Troca pixels amarelos no lado direito (x > 270) por branco
          const textStart = 270;

          for (let y = 0; y < img.height; y++) {
            for (let x = textStart; x < img.width; x++) {
              const i = (y * img.width + x) * 4;
              const r = data[i];
              const g = data[i + 1];
              const b = data[i + 2];
              const a = data[i + 3];

              if (a < 20) continue; // ignora transparente

              // Detecta amarelo/dourado: R alto, G médio-alto, B baixo
              if (r > 180 && g > 140 && b < 80 && r > b + 120) {
                data[i]     = 255; // R
                data[i + 1] = 255; // G
                data[i + 2] = 255; // B
                // mantém alpha original
              }
            }
          }

          ctx.putImageData(imageData, 0, 0);
          window._done = c.toDataURL('image/png');
        };
        img.src = '${dataUrl}';
      </script>
    </body></html>
  `);

  await page.waitForFunction(() => window._done !== undefined, { timeout: 15000 });
  const resultB64 = await page.evaluate(() => window._done.split(',')[1]);

  const out = path.join(__dirname, 'logo-slide5.png');
  fs.writeFileSync(out, Buffer.from(resultB64, 'base64'));
  console.log('Salvo: logo-slide5.png — Sleep Store em branco, mascote preservado');

  await browser.close();
})();
