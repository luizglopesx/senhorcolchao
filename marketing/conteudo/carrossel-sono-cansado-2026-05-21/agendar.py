import sys
import json
sys.path.insert(0, "/Users/luizgustavo/Projetos_Automacao/Senhor Colchao/senhor-colchao/.claude/skills/social-post-scheduler/scripts")

import instagram_publisher as ig
import facebook_publisher as fb

URLS = [
    "https://i.imgur.com/0R9W41A.png",  # slide-01
    "https://i.imgur.com/DcoaaDh.png",  # slide-02
    "https://i.imgur.com/KiuiWJK.png",  # slide-03
    "https://i.imgur.com/J0RXr5L.png",  # slide-04
    "https://i.imgur.com/0ACwzDy.png",  # slide-05
    "https://i.imgur.com/W90xOfo.png",  # slide-06
    "https://i.imgur.com/NuKdLX6.png",  # slide-07
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

# 22/05/2026 às 09:00 BRT
PUBLISH_TIME = 1779451200

print("=" * 50)
print("Agendando no Instagram...")
acc_ig = ig._get_account()
result_ig = ig.schedule_carousel(acc_ig, URLS, CAPTION, PUBLISH_TIME)
print(json.dumps(result_ig, indent=2, ensure_ascii=False))

print("\n" + "=" * 50)
print("Agendando no Facebook...")
acc_fb = fb._get_account()
result_fb = fb.schedule_carousel(acc_fb, URLS, CAPTION, PUBLISH_TIME)
print(json.dumps(result_fb, indent=2, ensure_ascii=False))
