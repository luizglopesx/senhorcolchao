#!/usr/bin/env python3
"""Publica post no Instagram — Campanha Noite a Dois (Junho 2026)."""

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

POSTS = {
    "01/06": {
        "image": "https://i.imgur.com/9mfzP7m.png",
        "caption": (
            "O maior presente não vem em caixa.\n"
            "Vem em noite a dois. 🛏️❤️\n\n"
            "A campanha de Dia dos Namorados da Sr. Colchão começa hoje — com condições especiais para quem quer presentear do jeito certo.\n\n"
            "Cama Box Casal Molas Ensacadas em até 12x sem juros, entrega e montagem grátis*.\n\n"
            "Passa na loja ou chama no WhatsApp — a gente encontra o produto perfeito pra vocês dois.\n\n"
            "Chama no WhatsApp\n\n"
            "📍 Rua 20, Entre 13x15, 1050\n"
            "📍 Rua 22, Esq. Av. 9, 1274\n"
            "⏳ Promoção válida de 01 a 13 de junho.\n\n"
            "*Consulte condições para sua região.\n\n"
            "#DiaDoNamorados #DiaDoNamorados2026 #SenhorColchao #SrColchao #PresenteDeNamorados #CamaBox #CamaBoxCasal #ColchaoMolasEnsacadas #NoiteADois #BomDescanso #SonoDeQualidade #EntregaGratis #12xSemJuros #CasalFeliz"
        ),
    },
    "03/06": {
        "image": "https://i.imgur.com/8oWuF7q.png",
        "caption": (
            "Pra dormir junto sem atrapalhar o outro. 🛏️\n\n"
            "Cama Box Casal Molas Ensacadas — R$ 1.590,00 em até 12x sem juros.\n\n"
            "A tecnologia de molas ensacadas isola o movimento: cada um se mexe de um lado, o outro nem sente. Isso é dormir bem junto.\n\n"
            "Com entrega e montagem grátis*, é o presente de Dia dos Namorados que vai durar anos.\n\n"
            "Passa na loja pra sentir de perto ou chama no WhatsApp — a gente te explica tudo.\n\n"
            "Chama no WhatsApp\n\n"
            "📍 Rua 20, Entre 13x15, 1050\n"
            "📍 Rua 22, Esq. Av. 9, 1274\n"
            "⏳ Condições especiais até 13 de junho.\n\n"
            "*Consulte condições para sua região.\n\n"
            "#MolasEnsacadas #ColchaoMolasEnsacadas #CamaBoxCasal #CamaBox #SenhorColchao #SrColchao #PresenteDeNamorados #DiaDoNamorados #12xSemJuros #EntregaGratis #BomDescanso #SonoDeQualidade #TecnologiaDeSono #CasalFeliz"
        ),
    },
    "05/06": {
        "image": "https://i.imgur.com/1YKfiWY.png",
        "caption": (
            "Casal que dorme bem, briga menos. 😄🛏️\n\n"
            "Pode parecer exagero, mas a ciência confirma: a qualidade do sono impacta diretamente o humor, a paciência e a energia do dia seguinte.\n\n"
            "E o colchão tem tudo a ver com isso.\n\n"
            "👉 Você sabia que o colchão ideal pra casal:\n"
            "— Isola o movimento (um se mexe, o outro não sente)\n"
            "— Distribui o peso de forma independente\n"
            "— Mantém a temperatura regulada\n\n"
            "A Cama Box Casal Molas Ensacadas da Sr. Colchão foi feita exatamente pra isso. Dormir junto, dormir bem.\n\n"
            "Quer saber qual é o modelo certo pra vocês? Chama no WhatsApp — a gente indica sem compromisso.\n\n"
            "📍 Rua 20, Entre 13x15, 1050\n"
            "📍 Rua 22, Esq. Av. 9, 1274\n\n"
            "#DicasDeSono #SonoDeQualidade #SaudeDoSono #CasalFeliz #BomDescanso #MolasEnsacadas #CamaBoxCasal #SenhorColchao #SrColchao #DiaDoNamorados #ColchaoIdeal #TrocaDeColchao #ColchaoDeQualidade"
        ),
    },
    "07/06": {
        "image": "https://i.imgur.com/pAaySM6.png",
        "caption": (
            "Acordar ao lado de quem você ama.\n"
            "Esse é o plano. ☀️❤️\n\n"
            "A gente garante que a cama faça a parte dela.\n\n"
            "Cama Box Casal Molas Ensacadas — 12x sem juros, entrega e montagem grátis*.\n\n"
            "Chama no WhatsApp ou passa na loja antes do Dia dos Namorados.\n\n"
            "📍 Rua 20, Entre 13x15, 1050\n"
            "📍 Rua 22, Esq. Av. 9, 1274\n"
            "⏳ Condições especiais até 13/06.\n\n"
            "*Consulte condições para sua região.\n\n"
            "#NoiteADois #CasalFeliz #DiaDoNamorados #DiaDoNamorados2026 #PresenteDeNamorados #SenhorColchao #SrColchao #CamaBox #CamaBoxCasal #BomDescanso #AmorDeVerdade #EntregaGratis"
        ),
    },
    "09/06": {
        "image": "https://i.imgur.com/r4px0lj.png",
        "caption": (
            "Faltam 3 dias para o Dia dos Namorados. ⏳\n\n"
            "Ainda dá tempo de garantir o presente que vai fazer diferença toda noite.\n\n"
            "Cama Box Casal Molas Ensacadas — R$ 1.590,00 em até 12x sem juros.\n"
            "Entrega e montagem grátis*.\n\n"
            "Não deixa pra última hora — chama no WhatsApp agora ou passa na loja.\n\n"
            "Chama no WhatsApp\n\n"
            "📍 Rua 20, Entre 13x15, 1050\n"
            "📍 Rua 22, Esq. Av. 9, 1274\n\n"
            "*Consulte condições para sua região.\n\n"
            "#UltimaChance #DiaDoNamorados #DiaDoNamorados2026 #3Dias #PresenteDeNamorados #CamaBoxCasal #SenhorColchao #SrColchao #12xSemJuros #EntregaGratis #NaoPercaEssaChance #BomDescanso"
        ),
    },
    "11/06": {
        "image": "https://i.imgur.com/q5NJSi1.png",
        "caption": (
            "Amanhã é o Dia dos Namorados.\n"
            "Ainda dá tempo de surpreender. ❤️\n\n"
            "Cama Box Casal Molas Ensacadas — R$ 1.590,00 em até 12x sem juros.\n"
            "Entrega e montagem grátis*.\n\n"
            "Chama no WhatsApp agora — a gente resolve hoje.\n\n"
            "Chama no WhatsApp\n\n"
            "📍 Rua 20, Entre 13x15, 1050\n"
            "📍 Rua 22, Esq. Av. 9, 1274\n\n"
            "*Consulte condições para sua região.\n\n"
            "#VésperaDeNamorados #DiaDoNamorados #DiaDoNamorados2026 #AindaDáTempo #PresenteDeNamorados #CamaBoxCasal #SenhorColchao #SrColchao #12xSemJuros #EntregaGratis #UltimosDias #CasalFeliz"
        ),
    },
    "12/06": {
        "image": "https://i.imgur.com/OQR2Uzv.png",
        "caption": (
            "Feliz Dia dos Namorados! ❤️\n\n"
            "Que o amor de vocês seja grande — e as noites, ainda melhores.\n\n"
            "Hoje ainda tem condições especiais na Sr. Colchão: Cama Box Casal Molas Ensacadas em até 12x sem juros, entrega e montagem grátis*.\n\n"
            "Chama no WhatsApp ou passa na loja — vamos comemorar junto com vocês.\n\n"
            "Chama no WhatsApp\n\n"
            "📍 Rua 20, Entre 13x15, 1050\n"
            "📍 Rua 22, Esq. Av. 9, 1274\n\n"
            "*Consulte condições para sua região.\n\n"
            "#FelizDiaDoNamorados #DiaDoNamorados #DiaDoNamorados2026 #12Dejunho #NoiteADois #PresenteDeNamorados #SenhorColchao #SrColchao #CamaBoxCasal #12xSemJuros #EntregaGratis #CasalFeliz #AmorDeVerdade"
        ),
    },
    "13/06": {
        "image": "https://i.imgur.com/0itI33N.png",
        "caption": (
            "Hoje é o último dia das condições especiais de Namorados.\n\n"
            "Cama Box Casal Molas Ensacadas — R$ 1.590,00 em até 12x sem juros.\n"
            "Entrega e montagem grátis*.\n\n"
            "Se você ainda tá na dúvida, esse é o sinal.\n\n"
            "Chama no WhatsApp ou passa direto na loja — a gente fecha negócio hoje.\n\n"
            "Chama no WhatsApp\n\n"
            "📍 Rua 20, Entre 13x15, 1050\n"
            "📍 Rua 22, Esq. Av. 9, 1274\n\n"
            "*Consulte condições para sua região.\n\n"
            "#UltimoDia #UltimaChance #SenhorColchao #SrColchao #CamaBoxCasal #PresenteDeNamorados #DiaDoNamorados #12xSemJuros #EntregaGratis #NaoPercaEssaChance #TrocaDeColchao #BomDescanso"
        ),
    },
}


def api_get(path: str, params: dict) -> dict:
    qs = urllib.parse.urlencode(params)
    url = f"{BASE_URL}/{path}?{qs}"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body[:500]}")
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


def wait_until_ready(creation_id: str, max_attempts: int = 10) -> bool:
    """Aguarda o Instagram processar a imagem antes de publicar."""
    for attempt in range(1, max_attempts + 1):
        status = api_get(creation_id, {
            "fields": "status_code",
            "access_token": ACCESS_TOKEN,
        })
        code = status.get("status_code", "")
        print(f"  Status ({attempt}/{max_attempts}): {code}")
        if code == "FINISHED":
            return True
        if code == "ERROR":
            print(f"Erro no processamento da mídia: {status}")
            return False
        time.sleep(5)
    return False


def publish(image_url: str, caption: str) -> str:
    # Step 1 — criar container
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

    # Step 2 — aguardar processamento
    print("Aguardando processamento da imagem...")
    if not wait_until_ready(creation_id):
        print("Timeout: imagem não ficou pronta a tempo.")
        sys.exit(1)

    # Step 3 — publicar
    result = api_post(f"{ACCOUNT_ID}/media_publish", {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN,
    })
    return result.get("id", "")


def main():
    brt = timezone(timedelta(hours=-3))
    today = datetime.now(brt).strftime("%d/%m")

    # Permite forçar uma data via argumento (para testes)
    if len(sys.argv) > 1:
        today = sys.argv[1]

    post = POSTS.get(today)
    if not post:
        print(f"Nenhum post agendado para hoje ({today}). Nada a fazer.")
        sys.exit(0)

    print(f"Publicando post de {today}...")
    post_id = publish(post["image"], post["caption"])
    print(f"✅ Publicado com sucesso! ID: {post_id}")


if __name__ == "__main__":
    main()
