#!/usr/bin/env python3
"""Instagram Graph API Publisher — publish and schedule posts."""

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
    pattern = re.compile(r"^SOCIAL_INSTAGRAM_(\d+)_LABEL$")
    for key, value in sorted(os.environ.items()):
        m = pattern.match(key)
        if m:
            idx = m.group(1)
            accounts.append({
                "index": idx,
                "label": value,
                "access_token": os.environ.get(f"SOCIAL_INSTAGRAM_{idx}_ACCESS_TOKEN", ""),
                "account_id": os.environ.get(f"SOCIAL_INSTAGRAM_{idx}_ACCOUNT_ID", ""),
                "page_token": os.environ.get(f"SOCIAL_INSTAGRAM_{idx}_PAGE_TOKEN", ""),
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
    return account.get("page_token") or account.get("access_token", "")


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


def publish_photo(account: dict, image_url: str, caption: str) -> dict:
    ig_id = account.get("account_id", "")
    token = _token(account)
    if not ig_id or not token:
        return {"error": "No account_id or token configured"}

    create = _api_post(f"{ig_id}/media", {
        "image_url": image_url,
        "caption": caption,
        "access_token": token,
    })
    if "error" in create:
        return create

    creation_id = create.get("id", "")
    if not creation_id:
        return {"error": "No creation_id returned", "detail": str(create)}

    result = _api_post(f"{ig_id}/media_publish", {
        "creation_id": creation_id,
        "access_token": token,
    })
    return {"account": account.get("label", ""), "post_id": result.get("id", ""), "raw": result}


def publish_carousel(account: dict, image_urls: list[str], caption: str) -> dict:
    ig_id = account.get("account_id", "")
    token = _token(account)
    if not ig_id or not token:
        return {"error": "No account_id or token configured"}
    if not image_urls:
        return {"error": "image_urls must not be empty"}

    item_ids = []
    for url in image_urls:
        resp = _api_post(f"{ig_id}/media", {
            "image_url": url,
            "is_carousel_item": "true",
            "access_token": token,
        })
        if "error" in resp:
            return {"error": f"Failed to create carousel item: {resp}"}
        item_ids.append(resp.get("id", ""))

    container = _api_post(f"{ig_id}/media", {
        "media_type": "CAROUSEL",
        "children": ",".join(item_ids),
        "caption": caption,
        "access_token": token,
    })
    if "error" in container:
        return container

    creation_id = container.get("id", "")
    if not creation_id:
        return {"error": "No carousel creation_id returned", "detail": str(container)}

    result = _api_post(f"{ig_id}/media_publish", {
        "creation_id": creation_id,
        "access_token": token,
    })
    return {"account": account.get("label", ""), "post_id": result.get("id", ""), "items": len(item_ids), "raw": result}


def publish_story(account: dict, image_url: str) -> dict:
    ig_id = account.get("account_id", "")
    token = _token(account)
    if not ig_id or not token:
        return {"error": "No account_id or token configured"}

    create = _api_post(f"{ig_id}/media", {
        "image_url": image_url,
        "media_type": "STORIES",
        "access_token": token,
    })
    if "error" in create:
        return create

    creation_id = create.get("id", "")
    if not creation_id:
        return {"error": "No creation_id returned", "detail": str(create)}

    result = _api_post(f"{ig_id}/media_publish", {
        "creation_id": creation_id,
        "access_token": token,
    })
    return {"account": account.get("label", ""), "story_id": result.get("id", ""), "raw": result}


def schedule_photo(account: dict, image_url: str, caption: str, publish_time_unix: int) -> dict:
    ig_id = account.get("account_id", "")
    token = _token(account)
    if not ig_id or not token:
        return {"error": "No account_id or token configured"}

    result = _api_post(f"{ig_id}/media", {
        "image_url": image_url,
        "caption": caption,
        "published": "false",
        "scheduled_publish_time": str(publish_time_unix),
        "access_token": token,
    })
    if "error" in result:
        return result

    return {
        "account": account.get("label", ""),
        "creation_id": result.get("id", ""),
        "scheduled_publish_time": publish_time_unix,
        "status": "scheduled",
    }


def schedule_carousel(account: dict, image_urls: list[str], caption: str, publish_time_unix: int) -> dict:
    ig_id = account.get("account_id", "")
    token = _token(account)
    if not ig_id or not token:
        return {"error": "No account_id or token configured"}
    if not image_urls:
        return {"error": "image_urls must not be empty"}

    item_ids = []
    for url in image_urls:
        resp = _api_post(f"{ig_id}/media", {
            "image_url": url,
            "is_carousel_item": "true",
            "access_token": token,
        })
        if "error" in resp:
            return {"error": f"Failed to create carousel item: {resp}"}
        item_ids.append(resp.get("id", ""))

    result = _api_post(f"{ig_id}/media", {
        "media_type": "CAROUSEL",
        "children": ",".join(item_ids),
        "caption": caption,
        "published": "false",
        "scheduled_publish_time": str(publish_time_unix),
        "access_token": token,
    })
    if "error" in result:
        return result

    return {
        "account": account.get("label", ""),
        "creation_id": result.get("id", ""),
        "items": len(item_ids),
        "scheduled_publish_time": publish_time_unix,
        "status": "scheduled",
    }


def get_scheduled_posts(account: dict) -> dict:
    ig_id = account.get("account_id", "")
    token = _token(account)
    if not ig_id or not token:
        return {"error": "No account_id or token configured"}

    data = _api_get(f"{ig_id}/media", {
        "fields": "id,caption,media_type,scheduled_publish_time,status",
        "publishing_type": "SCHEDULED",
        "access_token": token,
    })
    if "error" in data:
        return data

    return {
        "account": account.get("label", ""),
        "scheduled_posts": data.get("data", []),
        "total": len(data.get("data", [])),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: instagram_publisher.py <command> [args]")
        print("\nCommands:")
        print("  accounts                                             # List configured accounts")
        print("  publish_photo <image_url> <caption> [account]       # Publish photo now")
        print("  publish_story <image_url> [account]                 # Publish story now")
        print("  publish_carousel <img1,img2,...> <caption> [account] # Publish carousel now")
        print("  schedule_photo <image_url> <caption> <unix_ts> [account]      # Schedule photo")
        print("  schedule_carousel <img1,img2,...> <caption> <unix_ts> [account] # Schedule carousel")
        print("  scheduled [account]                                  # List scheduled posts")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    try:
        if cmd == "accounts":
            result = {"accounts": [{"index": a["index"], "label": a["label"],
                                     "account_id": a["account_id"],
                                     "has_token": bool(a["access_token"]),
                                     "has_page_token": bool(a["page_token"])} for a in _get_accounts()]}
        elif cmd == "publish_photo":
            image_url = args[0] if args else ""
            caption = args[1] if len(args) > 1 else ""
            acc = _get_account(args[2] if len(args) > 2 else None)
            result = publish_photo(acc, image_url, caption)
        elif cmd == "publish_story":
            image_url = args[0] if args else ""
            acc = _get_account(args[1] if len(args) > 1 else None)
            result = publish_story(acc, image_url)
        elif cmd == "publish_carousel":
            image_urls = args[0].split(",") if args else []
            caption = args[1] if len(args) > 1 else ""
            acc = _get_account(args[2] if len(args) > 2 else None)
            result = publish_carousel(acc, image_urls, caption)
        elif cmd == "schedule_photo":
            image_url = args[0] if args else ""
            caption = args[1] if len(args) > 1 else ""
            unix_ts = int(args[2]) if len(args) > 2 else 0
            acc = _get_account(args[3] if len(args) > 3 else None)
            result = schedule_photo(acc, image_url, caption, unix_ts)
        elif cmd == "schedule_carousel":
            image_urls = args[0].split(",") if args else []
            caption = args[1] if len(args) > 1 else ""
            unix_ts = int(args[2]) if len(args) > 2 else 0
            acc = _get_account(args[3] if len(args) > 3 else None)
            result = schedule_carousel(acc, image_urls, caption, unix_ts)
        elif cmd == "scheduled":
            acc = _get_account(args[0] if args else None)
            result = get_scheduled_posts(acc)
        else:
            print(f"Unknown command: {cmd}")
            sys.exit(1)

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)
