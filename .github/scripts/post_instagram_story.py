#!/usr/bin/env python3
"""Publica story no Instagram — Campanha Noite a Dois (Junho 2026)."""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

ACCESS_TOKEN = os.environ["INSTAGRAM_PAGE_TOKEN"]
ACCOUNT_ID   = os.environ["INSTAGRAM_ACCOUNT_ID"]
BASE_URL     = "https://graph.facebook.com/v25.0"
RAW          = "https://raw.githubusercontent.com/luizglopesx/senhorcolchao/main/.github/assets/stories"

STORIES = {
    "01/06": {"image": f"{RAW}/story-01-lancamento.png"},
    "03/06": {"image": f"{RAW}/story-02-produto.png"},
    "05/06": {"image": f"{RAW}/story-03-educativo.png"},
    "07/06": {"image": f"{RAW}/story-04-lifestyle.png"},
    "09/06": {"image": f"{RAW}/story-05-urgencia.png"},
    "11/06": {"image": f"{RAW}/story-06-vespera.png"},
    "12/06": {"image": f"{RAW}/story-07-dia-dos-namorados.png"},
    "13/06": {"image": f"{RAW}/story-08-dia-encerramento.png"},
}


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


def publish_story(image_url: str) -> str:
    container = api_post(f"{ACCOUNT_ID}/media", {
        "image_url": image_url,
        "media_type": "STORIES",
        "access_token": ACCESS_TOKEN,
    })
    creation_id = container.get("id")
    if not creation_id:
        print(f"Erro ao criar container: {container}")
        sys.exit(1)
    print(f"Container criado: {creation_id}")

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

    story = STORIES.get(today)
    if not story:
        print(f"Nenhum story agendado para hoje ({today}). Nada a fazer.")
        sys.exit(0)

    print(f"Publicando story de {today}...")
    post_id = publish_story(story["image"])
    print(f"✅ Story publicado com sucesso! ID: {post_id}")


if __name__ == "__main__":
    main()
