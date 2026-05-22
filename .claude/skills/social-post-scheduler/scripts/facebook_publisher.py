#!/usr/bin/env python3
"""Facebook Graph API Publisher — publish and schedule posts on Facebook Pages."""

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def _load_dotenv():
    env_path = Path(__file__).resolve().parents[4] / ".env"
    if not env_path.exists():
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip()
            if key and key not in os.environ:
                os.environ[key] = value


_load_dotenv()

BASE_URL = "https://graph.facebook.com/v25.0"


def _get_accounts() -> list[dict]:
    accounts = []
    pattern = re.compile(r"^SOCIAL_FACEBOOK_(\d+)_LABEL$")
    for key, value in sorted(os.environ.items()):
        m = pattern.match(key)
        if m:
            idx = m.group(1)
            accounts.append({
                "index": idx,
                "label": value,
                "page_id": os.environ.get(f"SOCIAL_FACEBOOK_{idx}_PAGE_ID", ""),
                "page_token": os.environ.get(f"SOCIAL_FACEBOOK_{idx}_PAGE_TOKEN", ""),
            })
    return accounts


def _get_account(label_or_index: str = None) -> dict:
    accounts = _get_accounts()
    if not accounts:
        return {}
    if not label_or_index:
        return accounts[0]
    for a in accounts:
        if a["index"] == label_or_index or a["label"].lower() == label_or_index.lower():
            return a
    return accounts[0]


def _token(account: dict) -> str:
    return account.get("page_token", "")


def _api_post(path: str, data: dict) -> dict:
    url = f"{BASE_URL}/{path}"
    payload = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"error": f"HTTP {e.code}", "detail": body[:500]}
    except Exception as e:
        return {"error": str(e)}


def _api_get(path: str, params: dict = None) -> dict:
    params = params or {}
    query = urllib.parse.urlencode(params)
    url = f"{BASE_URL}/{path}"
    if query:
        url += f"?{query}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"error": f"HTTP {e.code}", "detail": body[:500]}
    except Exception as e:
        return {"error": str(e)}


def _api_delete(path: str, params: dict = None) -> dict:
    params = params or {}
    query = urllib.parse.urlencode(params)
    url = f"{BASE_URL}/{path}"
    if query:
        url += f"?{query}"
    req = urllib.request.Request(url, method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"error": f"HTTP {e.code}", "detail": body[:500]}
    except Exception as e:
        return {"error": str(e)}


def publish_post(account: dict, message: str, image_url: str = None) -> dict:
    page_id = account.get("page_id", "")
    token = _token(account)
    if not page_id or not token:
        return {"error": "No page_id or page_token configured"}

    if image_url:
        data = {
            "url": image_url,
            "message": message,
            "access_token": token,
        }
        result = _api_post(f"{page_id}/photos", data)
    else:
        data = {
            "message": message,
            "access_token": token,
        }
        result = _api_post(f"{page_id}/feed", data)

    if "error" in result:
        return result

    return {
        "account": account.get("label", ""),
        "post_id": result.get("id", result.get("post_id", "")),
        "status": "published",
    }


def schedule_post(account: dict, message: str, publish_time_unix: int, image_url: str = None) -> dict:
    page_id = account.get("page_id", "")
    token = _token(account)
    if not page_id or not token:
        return {"error": "No page_id or page_token configured"}

    if image_url:
        data = {
            "url": image_url,
            "message": message,
            "published": "false",
            "scheduled_publish_time": str(publish_time_unix),
            "access_token": token,
        }
        result = _api_post(f"{page_id}/photos", data)
    else:
        data = {
            "message": message,
            "published": "false",
            "scheduled_publish_time": str(publish_time_unix),
            "access_token": token,
        }
        result = _api_post(f"{page_id}/feed", data)

    if "error" in result:
        return result

    return {
        "account": account.get("label", ""),
        "post_id": result.get("id", result.get("post_id", "")),
        "scheduled_publish_time": publish_time_unix,
        "status": "scheduled",
    }


def publish_carousel(account: dict, image_urls: list[str], message: str) -> dict:
    page_id = account.get("page_id", "")
    token = _token(account)
    if not page_id or not token:
        return {"error": "No page_id or page_token configured"}
    if not image_urls:
        return {"error": "image_urls must not be empty"}

    # 1. Faz upload de cada foto individualmente (sem publicar)
    photo_ids = []
    for url in image_urls:
        resp = _api_post(f"{page_id}/photos", {
            "url": url,
            "published": "false",
            "access_token": token,
        })
        if "error" in resp:
            return {"error": f"Falha no upload da foto {url}: {resp}"}
        photo_ids.append(resp.get("id", ""))

    # 2. Cria o post multi-foto vinculando todos os IDs
    attached = [{"media_fbid": pid} for pid in photo_ids]
    result = _api_post(f"{page_id}/feed", {
        "message": message,
        "attached_media": json.dumps(attached),
        "access_token": token,
    })
    if "error" in result:
        return result

    return {
        "account": account.get("label", ""),
        "post_id": result.get("id", ""),
        "items": len(photo_ids),
        "status": "published",
    }


def schedule_carousel(account: dict, image_urls: list[str], message: str, publish_time_unix: int) -> dict:
    page_id = account.get("page_id", "")
    token = _token(account)
    if not page_id or not token:
        return {"error": "No page_id or page_token configured"}
    if not image_urls:
        return {"error": "image_urls must not be empty"}

    # 1. Faz upload de cada foto individualmente (sem publicar)
    photo_ids = []
    for url in image_urls:
        resp = _api_post(f"{page_id}/photos", {
            "url": url,
            "published": "false",
            "access_token": token,
        })
        if "error" in resp:
            return {"error": f"Falha no upload da foto {url}: {resp}"}
        photo_ids.append(resp.get("id", ""))

    # 2. Cria o post agendado multi-foto
    attached = [{"media_fbid": pid} for pid in photo_ids]
    result = _api_post(f"{page_id}/feed", {
        "message": message,
        "attached_media": json.dumps(attached),
        "published": "false",
        "scheduled_publish_time": str(publish_time_unix),
        "access_token": token,
    })
    if "error" in result:
        return result

    return {
        "account": account.get("label", ""),
        "post_id": result.get("id", ""),
        "items": len(photo_ids),
        "scheduled_publish_time": publish_time_unix,
        "status": "scheduled",
    }


def get_scheduled_posts(account: dict) -> dict:
    page_id = account.get("page_id", "")
    token = _token(account)
    if not page_id or not token:
        return {"error": "No page_id or page_token configured"}

    data = _api_get(f"{page_id}/scheduled_posts", {
        "fields": "id,message,scheduled_publish_time,story",
        "access_token": token,
    })
    if "error" in data:
        return data

    return {
        "account": account.get("label", ""),
        "scheduled_posts": data.get("data", []),
        "total": len(data.get("data", [])),
    }


def delete_post(account: dict, post_id: str) -> dict:
    token = _token(account)
    if not token:
        return {"error": "No page_token configured"}

    result = _api_delete(post_id, {"access_token": token})
    if "error" in result:
        return result

    return {
        "account": account.get("label", ""),
        "post_id": post_id,
        "deleted": result.get("success", False),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: facebook_publisher.py <command> [args]")
        print("\nCommands:")
        print("  accounts                                                   # List configured accounts")
        print("  publish_post <message> [image_url] [account]              # Publish post now")
        print("  schedule_post <message> <unix_ts> [image_url] [account]   # Schedule post")
        print("  scheduled [account]                                        # List scheduled posts")
        print("  delete_post <post_id> [account]                           # Delete post")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    try:
        if cmd == "accounts":
            result = {"accounts": [{"index": a["index"], "label": a["label"],
                                     "page_id": a["page_id"],
                                     "has_token": bool(a["page_token"])} for a in _get_accounts()]}
        elif cmd == "publish_post":
            message = args[0] if args else ""
            image_url = args[1] if len(args) > 1 and args[1].startswith("http") else None
            acc_arg = args[2] if len(args) > 2 else (args[1] if len(args) > 1 and not args[1].startswith("http") else None)
            acc = _get_account(acc_arg)
            result = publish_post(acc, message, image_url)
        elif cmd == "schedule_post":
            message = args[0] if args else ""
            unix_ts = int(args[1]) if len(args) > 1 else 0
            image_url = args[2] if len(args) > 2 and args[2].startswith("http") else None
            acc_arg = args[3] if len(args) > 3 else (args[2] if len(args) > 2 and not args[2].startswith("http") else None)
            acc = _get_account(acc_arg)
            result = schedule_post(acc, message, unix_ts, image_url)
        elif cmd == "scheduled":
            acc = _get_account(args[0] if args else None)
            result = get_scheduled_posts(acc)
        elif cmd == "delete_post":
            post_id = args[0] if args else ""
            acc = _get_account(args[1] if len(args) > 1 else None)
            result = delete_post(acc, post_id)
        else:
            print(f"Unknown command: {cmd}")
            sys.exit(1)

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)
