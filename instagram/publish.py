#!/usr/bin/env python3
"""Instagram publisher — GitHub Actions cron.

Flow por post:
  1. POST /{ig_account_id}/media  → container_id
  2. GET  /{container_id}?fields=status_code  (poll até FINISHED, max 5 min)
  3. POST /{ig_account_id}/media_publish  → post_id

Variáveis de ambiente (GitHub Secrets):
  IG_ACCOUNT_ID    — Instagram Business Account ID
  IG_ACCESS_TOKEN  — Page token com instagram_content_publish
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
REPO = "luizglopesx/senhorcolchao"
BRANCH = "main"
ARTES_PATH = "marketing/campanhas/julho-2026-durma-como-campeao/artes"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{ARTES_PATH}"

IG_ACCOUNT_ID = os.environ.get("IG_ACCOUNT_ID", "")
IG_ACCESS_TOKEN = os.environ.get("IG_ACCESS_TOKEN", "")

if not IG_ACCOUNT_ID or not IG_ACCESS_TOKEN:
    print("ERRO: IG_ACCOUNT_ID e IG_ACCESS_TOKEN são obrigatórios.")
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
    """Cria container de mídia no Instagram. Retorna container_id."""
    filename = post["video_filename"]
    video_url = f"{RAW_BASE}/{urllib.parse.quote(filename)}"

    params = {
        "access_token": IG_ACCESS_TOKEN,
        "video_url": video_url,
    }

    if post["media_type"] == "REELS":
        params["media_type"] = "REELS"
        params["caption"] = post.get("caption", "")
        params["share_to_feed"] = "true"
    elif post["media_type"] == "STORIES":
        params["media_type"] = "STORIES"

    print(f"  → Criando container | tipo={post['media_type']} | url={video_url}")
    result = api_post(f"{IG_ACCOUNT_ID}/media", params)

    if "id" in result:
        print(f"  ✓ Container: {result['id']}")
        return result["id"]

    print(f"  ✗ Erro ao criar container: {json.dumps(result)}")
    return None


def poll_container(container_id: str, max_attempts: int = 30, interval: int = 10) -> bool:
    """Poll até status_code=FINISHED. Timeout padrão 5 min (30 × 10s)."""
    print(f"  → Aguardando processamento ({max_attempts * interval}s max) ...")
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
    """Publica container FINISHED. Retorna post_id."""
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

    print(f"\n=== Instagram Publisher — {now.strftime('%Y-%m-%d %H:%M UTC')} ===\n")

    for post in data["posts"]:
        if post["status"] != "pending":
            continue

        scheduled_at = datetime.fromisoformat(post["scheduled_at"])
        if now < scheduled_at:
            delta = int((scheduled_at - now).total_seconds() / 60)
            print(f"Aguardando [{post['id']}] — faltam ~{delta} min")
            continue

        print(f"\n▶ Publicando: {post['label']}")

        container_id = create_container(post)
        if not container_id:
            post["status"] = "error"
            post["error"] = "Falha ao criar container"
            post["error_at"] = now.isoformat()
            errors += 1
            changed = True
            continue

        if not poll_container(container_id):
            post["status"] = "error"
            post["error"] = f"Container {container_id} não ficou FINISHED"
            post["error_at"] = now.isoformat()
            errors += 1
            changed = True
            continue

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
        print(f"\nschedule.json atualizado.")

    print(f"\n=== Resultado: {published} publicado(s), {errors} erro(s) ===")
    return 1 if errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
