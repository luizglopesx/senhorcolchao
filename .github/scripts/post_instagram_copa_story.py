#!/usr/bin/env python3
"""Publica story no Instagram — Campanha Aqui Dá Jogo! (Copa 2026)."""

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
RAW          = "https://raw.githubusercontent.com/luizglopesx/senhorcolchao/main/.github/assets/copa-2026/stories"

STORIES = {
    "17/06": {"image": f"{RAW}/story-04a-produto-molas.png"},
    "18/06": {"image": f"{RAW}/story-05-educativo.png"},
    "19/06": {"image": f"{RAW}/story-02-pregame.png"},
    "21/06": {"image": f"{RAW}/story-04b-produto-d33.png"},
    "23/06": {"image": f"{RAW}/story-05-educativo.png"},
    "24/06": {"image": f"{RAW}/story-02-pregame.png"},
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


def wait_for_container(creation_id: str, max_attempts: int = 15, interval: int = 5) -> None:
    """Aguarda o container ficar FINISHED antes de publicar."""
    import time
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

    story = STORIES.get(today)
    if not story:
        print(f"Nenhum story agendado para hoje ({today}). Nada a fazer.")
        sys.exit(0)

    print(f"Publicando story de {today}...")
    post_id = publish_story(story["image"])
    print(f"✅ Story publicado com sucesso! ID: {post_id}")


if __name__ == "__main__":
    main()
