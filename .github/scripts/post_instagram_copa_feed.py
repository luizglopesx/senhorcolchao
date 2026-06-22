#!/usr/bin/env python3
"""Publica feed no Instagram — Campanha Aqui Dá Jogo! (Copa 2026)."""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

ACCESS_TOKEN = os.environ["INSTAGRAM_PAGE_TOKEN"]
ACCOUNT_ID   = os.environ["INSTAGRAM_ACCOUNT_ID"]
BASE_URL     = "https://graph.facebook.com/v25.0"
RAW          = "https://raw.githubusercontent.com/luizglopesx/senhorcolchao/main/.github/assets/copa-2026/feed"

POSTS = {
    "17/06": {
        "image": f"{RAW}/arte-04a-produto-molas.png",
        "caption": (
            "Esse aqui é o artilheiro do descanso. ⚽🏆\n\n"
            "Cama Box Molas Ensacadas 138x188 — tecnologia de molas independentes que se adaptam ao seu corpo "
            "em cada movimento. Mais conforto, menos pressão, sono de qualidade real.\n\n"
            "E enquanto o Brasil tá em campo, você pode estar garantindo o seu aqui na Sr. Colchão.\n\n"
            "🛏️ R$ 1.790 em até 12x R$ 149,17 sem juros\n"
            "🚚 Entrega e montagem grátis*\n\n"
            "Aqui dá jogo. 🇧🇷\n"
            "Chama no WhatsApp 📲\n\n"
            "📍 Rua 20, Entre 13x15, 1050\n"
            "📍 Rua 22, Esq. Av. 9, 1274\n\n"
            "*Consulte condições para sua região.\n\n"
            "#AquiDaJogo #SenhorColchao #SrColchao #CamaBox #CamaBoxCasal #MolasEnsacadas "
            "#ColchaoMolas #12xSemJuros #EntregaGratis #BarretosSP #Barretos "
            "#BomDescanso #SonoDeQualidade #CopaDoMundo2026 #VaiBrasil"
        ),
    },
    "18/06": {
        "image": f"{RAW}/arte-05-educativo.png",
        "caption": (
            "Sabe o que o jogador mais precisa antes de entrar em campo? ⚽\n\n"
            "Dormir bem.\n\n"
            "O sono é onde o corpo se recupera, a mente descansa e a energia se renova. "
            "É lá que a performance começa — mesmo pra quem vai torcer do sofá.\n\n"
            "Na Sr. Colchão a gente leva isso a sério.\n\n"
            "🛏️ Cama Box Molas Ensacadas — R$ 1.790 em 12x sem juros\n"
            "🛏️ Cama Box D33 Ícaro Preto — R$ 1.590 em 12x sem juros\n"
            "🚚 Entrega e montagem grátis*\n\n"
            "Aqui dá jogo. 🇧🇷\n\n"
            "📍 Rua 20, Entre 13x15, 1050\n"
            "📍 Rua 22, Esq. Av. 9, 1274\n\n"
            "#BomDescanso #SonoDeQualidade #SonoReparador #AquiDaJogo #SenhorColchao #SrColchao "
            "#CamaBox #MolasEnsacadas #12xSemJuros #BarretosSP #Barretos "
            "#Saude #QualidadeDeVida #VaiBrasil #CopaDoMundo2026"
        ),
    },
    "19/06": {
        "image": f"{RAW}/arte-02-pregame.png",
        "caption": (
            "Hoje tem Brasil! 🇧🇷⚽\n\n"
            "E pra torcer do jeito certo, começa com uma boa noite de sono.\n"
            "Quem dorme bem, acorda pronto pro jogo — mesmo que seja só no sofá.\n\n"
            "🛏️ Cama Box Molas Ensacadas — 12x R$ 149,17 sem juros\n"
            "🛏️ Cama Box D33 Ícaro Preto — 12x R$ 132,50 sem juros\n"
            "🚚 Entrega e montagem grátis*\n\n"
            "Vai Brasil! 💪🏾\n"
            "Chama no WhatsApp e garante o seu antes do próximo apito.\n\n"
            "📍 Rua 20, Entre 13x15, 1050\n"
            "📍 Rua 22, Esq. Av. 9, 1274\n\n"
            "*Consulte condições para sua região.\n\n"
            "#VaiBrasil #HojeTémBrasil #BrasilNaCopa #CopaDoMundo2026 #Copa2026 "
            "#AquiDaJogo #SenhorColchao #SrColchao #CamaBox #CamaBoxCasal "
            "#MolasEnsacadas #12xSemJuros #BarretosSP #BomDescanso #SonoDeQualidade"
        ),
    },
    "21/06": {
        "image": f"{RAW}/arte-04b-produto-d33.png",
        "caption": (
            "Elegância que entra em campo. ⚽🖤\n\n"
            "Cama Box D33 Ícaro Preto 138x188 — espuma D33 de alta densidade com design premium. "
            "Firmeza na medida certa pra quem leva o descanso a sério.\n\n"
            "Porque torcedor bom dorme bem antes do jogo. 🇧🇷\n\n"
            "🛏️ R$ 1.590 em até 12x R$ 132,50 sem juros\n"
            "🚚 Entrega e montagem grátis*\n\n"
            "Aqui dá jogo. ⚽\n"
            "Chama no WhatsApp 📲\n\n"
            "📍 Rua 20, Entre 13x15, 1050\n"
            "📍 Rua 22, Esq. Av. 9, 1274\n\n"
            "*Consulte condições para sua região.\n\n"
            "#AquiDaJogo #SenhorColchao #SrColchao #CamaBox #CamaBoxCasal "
            "#D33 #IcaroPreto #ColchaoD33 #12xSemJuros #EntregaGratis "
            "#BarretosSP #Barretos #BomDescanso #SonoDeQualidade #CopaDoMundo2026 #VaiBrasil"
        ),
    },
    "23/06": {
        "image": f"{RAW}/arte-05-educativo.png",
        "caption": (
            "Sabe o que o jogador mais precisa antes de entrar em campo? ⚽\n\n"
            "Dormir bem.\n\n"
            "O sono é onde o corpo se recupera, a mente descansa e a energia se renova. "
            "É lá que a performance começa — mesmo pra quem vai torcer do sofá.\n\n"
            "Na Sr. Colchão a gente leva isso a sério.\n\n"
            "🛏️ Cama Box Molas Ensacadas — R$ 1.790 em 12x sem juros\n"
            "🛏️ Cama Box D33 Ícaro Preto — R$ 1.590 em 12x sem juros\n"
            "🚚 Entrega e montagem grátis*\n\n"
            "Aqui dá jogo. 🇧🇷\n\n"
            "📍 Rua 20, Entre 13x15, 1050\n"
            "📍 Rua 22, Esq. Av. 9, 1274\n\n"
            "#BomDescanso #SonoDeQualidade #SonoReparador #AquiDaJogo #SenhorColchao #SrColchao "
            "#CamaBox #MolasEnsacadas #12xSemJuros #BarretosSP #Barretos "
            "#Saude #QualidadeDeVida #VaiBrasil #CopaDoMundo2026"
        ),
    },
    "24/06": {
        "image": f"{RAW}/arte-02-pregame.png",
        "caption": (
            "Hoje tem Brasil! 🇧🇷⚽\n\n"
            "E pra torcer do jeito certo, começa com uma boa noite de sono.\n"
            "Quem dorme bem, acorda pronto pro jogo — mesmo que seja só no sofá.\n\n"
            "🛏️ Cama Box Molas Ensacadas — 12x R$ 149,17 sem juros\n"
            "🛏️ Cama Box D33 Ícaro Preto — 12x R$ 132,50 sem juros\n"
            "🚚 Entrega e montagem grátis*\n\n"
            "Vai Brasil! 💪🏾\n"
            "Chama no WhatsApp e garante o seu antes do próximo apito.\n\n"
            "📍 Rua 20, Entre 13x15, 1050\n"
            "📍 Rua 22, Esq. Av. 9, 1274\n\n"
            "*Consulte condições para sua região.\n\n"
            "#VaiBrasil #HojeTémBrasil #BrasilNaCopa #CopaDoMundo2026 #Copa2026 "
            "#AquiDaJogo #SenhorColchao #SrColchao #CamaBox #CamaBoxCasal "
            "#MolasEnsacadas #12xSemJuros #BarretosSP #BomDescanso #SonoDeQualidade"
        ),
    },
}


def api_get(path: str, params: dict) -> dict:
    query = urllib.parse.urlencode(params)
    url = f"{BASE_URL}/{path}?{query}"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body[:500]}")
        sys.exit(1)


def wait_for_container(creation_id: str, max_attempts: int = 15, interval: int = 5) -> None:
    """Aguarda o container ficar FINISHED antes de publicar."""
    for attempt in range(1, max_attempts + 1):
        result = api_get(creation_id, {
            "fields": "status_code,status",
            "access_token": ACCESS_TOKEN,
        })
        status_code = result.get("status_code", "")
        print(f"  [{attempt}/{max_attempts}] status_code: {status_code}")
        if status_code == "FINISHED":
            return
        if status_code == "ERROR":
            print(f"Erro no processamento do container: {result}")
            sys.exit(1)
        time.sleep(interval)
    print(f"Timeout: container não ficou pronto após {max_attempts * interval}s.")
    sys.exit(1)


def api_post(path: str, data: dict) -> dict:
    url = f"{BASE_URL}/{path}"
    payload = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body[:500]}")
        sys.exit(1)


def publish(image_url: str, caption: str) -> str:
    container = api_post(f"{ACCOUNT_ID}/media", {
        "image_url": image_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN,
    })
    creation_id = container.get("id")
    if not creation_id:
        print(f"Erro ao criar container: {container}")
        sys.exit(1)
    print(f"Container criado: {creation_id}")

    print("Aguardando container ficar pronto...")
    wait_for_container(creation_id)

    result = api_post(f"{ACCOUNT_ID}/media_publish", {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN,
    })
    return result.get("id", "")


def main():
    brt = timezone(timedelta(hours=-3))
    today = datetime.now(brt).strftime("%d/%m")

    if len(sys.argv) > 1:
        today = sys.argv[1]

    post = POSTS.get(today)
    if not post:
        print(f"Nenhum post agendado para hoje ({today}). Nada a fazer.")
        sys.exit(0)

    print(f"Publicando feed de {today}...")
    post_id = publish(post["image"], post["caption"])
    print(f"✅ Feed publicado com sucesso! ID: {post_id}")


if __name__ == "__main__":
    main()
