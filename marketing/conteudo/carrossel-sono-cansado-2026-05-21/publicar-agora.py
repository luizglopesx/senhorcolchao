import sys
import json
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    filename=str(Path(__file__).parent / "publicar.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

sys.path.insert(0, "/Users/luizgustavo/Projetos_Automacao/Senhor Colchao/senhor-colchao/.claude/skills/social-post-scheduler/scripts")
import instagram_publisher as ig

URLS = [
    "https://i.imgur.com/0R9W41A.png",
    "https://i.imgur.com/DcoaaDh.png",
    "https://i.imgur.com/KiuiWJK.png",
    "https://i.imgur.com/J0RXr5L.png",
    "https://i.imgur.com/0ACwzDy.png",
    "https://i.imgur.com/W90xOfo.png",
    "https://i.imgur.com/NuKdLX6.png",
]

CAPTION = """Dormiu 8 horas e acordou destruído? A culpa pode ser do colchão. 😴

Arraste pro lado e descobre por que isso acontece — e o que você pode fazer pra mudar.

Colchão velho não descansa — ele trabalha contra você a noite toda. Desalinha a coluna, interrompe o sono e faz você acordar com aquela dor que some só de tarde.

Se você dorme mais de 8 anos no mesmo colchão, já passou da hora de trocar.

A gente tem opções pra todo tipo de sono e bolso — com entrega e montagem grátis em Barretos.

Chama no WhatsApp ou passa na loja. 👇

📞 (17) 3323-3694
📍 Rua 20, 1050 / Rua 22, 1274 — Barretos

#colchão #sonodesqualidade #descanso #dormirbem #colchãonovo #barretos #senhorcolchao #sleepstore #qualidadedevida #trocarocolchão #dormirbeméviver #saúde #bemestar #colabox #colchaobarretos #lojabarretos"""

logging.info("Iniciando publicação do carrossel...")
acc = ig._get_account()
result = ig.publish_carousel(acc, URLS, CAPTION)
logging.info("Resultado: %s", json.dumps(result, ensure_ascii=False))
print(json.dumps(result, indent=2, ensure_ascii=False))
