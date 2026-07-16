#!/usr/bin/env python3
"""Instagram publisher — GitHub Actions cron (Julho 2026 — Durma como Campeão).

Fluxo por post de vídeo:
  1. POST /{ig_account_id}/media  → container_id
  2. GET  /{container_id}?fields=status_code  (poll até FINISHED, max 5 min)
  3. POST /{ig_account_id}/media_publish  → post_id

Variáveis de ambiente (GitHub Secrets):
  INSTAGRAM_PAGE_TOKEN  — Page token com instagram_content_publish
  INSTAGRAM_ACCOUNT_ID  — Instagram Business Account ID
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

GRAPH_URL = "https://graph.facebook.com/v25.0"
REPO      = "luizglopesx/senhorcolchao"
BRANCH    = "main"
DEFAULT_ARTES_PATH = "marketing/campanhas/julho-2026-durma-como-campeao/artes"


def raw_base(post: dict) -> str:
    """Pasta de artes do post — cada post pode apontar pra uma campanha diferente."""
    artes_path = post.get("artes_path", DEFAULT_ARTES_PATH)
    return f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{artes_path}"

IG_ACCOUNT_ID  = os.environ.get("INSTAGRAM_ACCOUNT_ID", "")
IG_ACCESS_TOKEN = os.environ.get("INSTAGRAM_PAGE_TOKEN", "")

if not IG_ACCOUNT_ID or not IG_ACCESS_TOKEN:
    print("ERRO: INSTAGRAM_ACCOUNT_ID e INSTAGRAM_PAGE_TOKEN são obrigatórios.")
    sys.exit(1)


def api_post(path: str, params: dict) -> dict:
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(f"{GRAPH_URL}/{path}", data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"error": f"HTTP {e.code}", "detail": body[:500]}
    except Exception as e:
        return {"error": str(e)}


def api_get(path: str, params: dict) -> dict:
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{GRAPH_URL}/{path}?{query}")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"error": f"HTTP {e.code}", "detail": body[:500]}
    except Exception as e:
        return {"error": str(e)}


def create_container(post: dict) -> str | None:
    """Cria container de mídia (foto ou vídeo). Retorna container_id ou None em caso de erro."""
    is_video = "video_filename" in post
    filename = post["video_filename"] if is_video else post["image_filename"]
    media_url = f"{raw_base(post)}/{urllib.parse.quote(filename)}"

    params = {
        "access_token": IG_ACCESS_TOKEN,
        "video_url" if is_video else "image_url": media_url,
    }

    if post["media_type"] == "REELS":
        params["media_type"] = "REELS"
        params["caption"] = post.get("caption", "")
        params["share_to_feed"] = "true"
    elif post["media_type"] == "STORIES":
        params["media_type"] = "STORIES"
    elif post["media_type"] == "FEED":
        # Foto simples de feed: sem media_type — é o padrão da API pra image_url isolado
        params["caption"] = post.get("caption", "")

    print(f"  → Criando container | tipo={post['media_type']} | midia={'video' if is_video else 'imagem'}")
    print(f"    url={media_url}")
    result = api_post(f"{IG_ACCOUNT_ID}/media", params)

    if "id" in result:
        print(f"  ✓ Container: {result['id']}")
        return result["id"]

    print(f"  ✗ Erro ao criar container: {json.dumps(result)}")
    return None


def poll_container(container_id: str, max_attempts: int = 30, interval: int = 10) -> bool:
    """Poll até status_code=FINISHED. Default: 30 × 10s = 5 min máximo."""
    print(f"  → Aguardando processamento (até {max_attempts * interval}s) ...")
    for attempt in range(1, max_attempts + 1):
        result = api_get(container_id, {
            "fields": "status_code,status",
            "access_token": IG_ACCESS_TOKEN,
        })

        status_code = result.get("status_code", "UNKNOWN")
        print(f"  [{attempt:02d}/{max_attempts}] status_code={status_code}")

        if status_code == "FINISHED":
            return True
        if status_code == "ERROR":
            print(f"  ✗ Erro no container: {json.dumps(result)}")
            return False
        if "error" in result:
            print(f"  ✗ Erro na API: {json.dumps(result)}")
            return False

        if attempt < max_attempts:
            time.sleep(interval)

    print(f"  ✗ Timeout: container não ficou FINISHED em {max_attempts * interval}s")
    return False


def publish_container(container_id: str) -> str | None:
    """Publica container FINISHED. Retorna post_id ou None."""
    result = api_post(f"{IG_ACCOUNT_ID}/media_publish", {
        "creation_id": container_id,
        "access_token": IG_ACCESS_TOKEN,
    })

    if "id" in result:
        return result["id"]

    print(f"  ✗ Erro ao publicar: {json.dumps(result)}")
    return None


def main() -> int:
    schedule_path = Path(__file__).parent / "schedule.json"
    data = json.loads(schedule_path.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc)
    published = 0
    errors = 0
    changed = False

    print(f"\n=== Instagram Publisher — {now.strftime('%Y-%m-%d %H:%M UTC')} ===")
    print(f"    Conta: {IG_ACCOUNT_ID}\n")

    for post in data["posts"]:
        if post["status"] != "pending":
            print(f"Ignorando [{post['id']}] — status={post['status']}")
            continue

        scheduled_at = datetime.fromisoformat(post["scheduled_at"])
        if now < scheduled_at:
            delta_min = int((scheduled_at - now).total_seconds() / 60)
            print(f"Aguardando [{post['id']}] — faltam ~{delta_min} min")
            continue

        print(f"\n▶ Publicando: {post['label']}")

        # Step 1 — criar container
        container_id = create_container(post)
        if not container_id:
            post["status"] = "error"
            post["error"] = "Falha ao criar container"
            post["error_at"] = now.isoformat()
            errors += 1
            changed = True
            continue

        # Step 2 — aguardar processamento
        if not poll_container(container_id):
            post["status"] = "error"
            post["error"] = f"Container {container_id} não ficou FINISHED"
            post["error_at"] = now.isoformat()
            errors += 1
            changed = True
            continue

        # Step 3 — publicar
        post_id = publish_container(container_id)
        if post_id:
            post["status"] = "published"
            post["post_id"] = post_id
            post["container_id"] = container_id
            post["published_at"] = now.isoformat()
            print(f"  ✓ Publicado! post_id={post_id}")
            published += 1
        else:
            post["status"] = "error"
            post["error"] = f"Falha ao publicar container {container_id}"
            post["error_at"] = now.isoformat()
            errors += 1

        changed = True

    if changed:
        schedule_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print("\nschedule.json atualizado.")

    print(f"\n=== Resultado: {published} publicado(s), {errors} erro(s) ===")
    return 1 if errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
