#!/usr/bin/env python3
"""Meta Ads API Client — create and manage paid campaigns via Marketing API v25.0."""

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

VALID_OBJECTIVES = {
    "OUTCOME_TRAFFIC",
    "OUTCOME_ENGAGEMENT",
    "OUTCOME_LEADS",
    "OUTCOME_SALES",
}


def _get_ads_accounts() -> list[dict]:
    accounts = []
    pattern = re.compile(r"^SOCIAL_META_ADS_(\d+)_LABEL$")
    for key, value in sorted(os.environ.items()):
        m = pattern.match(key)
        if m:
            idx = m.group(1)
            accounts.append({
                "index": idx,
                "label": value,
                "account_id": os.environ.get(f"SOCIAL_META_ADS_{idx}_ACCOUNT_ID", ""),
            })
    return accounts


def _get_ads_account(label_or_index: str = None) -> dict:
    accounts = _get_ads_accounts()
    if not accounts:
        return {}
    if not label_or_index:
        return accounts[0]
    for a in accounts:
        if a["index"] == label_or_index or a["label"].lower() == label_or_index.lower():
            return a
    return accounts[0]


def _get_token() -> str:
    """Use first available Facebook page token — page token has ads_management permission."""
    pattern = re.compile(r"^SOCIAL_FACEBOOK_(\d+)_PAGE_TOKEN$")
    for key, value in sorted(os.environ.items()):
        if pattern.match(key) and value:
            return value
    return os.environ.get("META_ADS_TOKEN", "")


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


def get_campaigns(ads_account: dict) -> dict:
    account_id = ads_account.get("account_id", "")
    token = _get_token()
    if not account_id or not token:
        return {"error": "No account_id or token configured"}

    data = _api_get(f"act_{account_id}/campaigns", {
        "fields": "id,name,objective,status,daily_budget,start_time,stop_time",
        "effective_status": '["ACTIVE","PAUSED"]',
        "access_token": token,
    })
    if "error" in data:
        return data

    return {
        "ads_account": ads_account.get("label", ""),
        "account_id": account_id,
        "campaigns": data.get("data", []),
        "total": len(data.get("data", [])),
    }


def create_campaign(
    ads_account: dict,
    name: str,
    objective: str,
    daily_budget_cents: int,
    start_time: str,
    end_time: str,
) -> dict:
    account_id = ads_account.get("account_id", "")
    token = _get_token()
    if not account_id or not token:
        return {"error": "No account_id or token configured"}
    if objective not in VALID_OBJECTIVES:
        return {"error": f"Invalid objective. Valid: {', '.join(sorted(VALID_OBJECTIVES))}"}

    result = _api_post(f"act_{account_id}/campaigns", {
        "name": name,
        "objective": objective,
        "daily_budget": str(daily_budget_cents),
        "start_time": start_time,
        "stop_time": end_time,
        "status": "PAUSED",
        "special_ad_categories": "[]",
        "access_token": token,
    })
    if "error" in result:
        return result

    return {
        "ads_account": ads_account.get("label", ""),
        "campaign_id": result.get("id", ""),
        "name": name,
        "objective": objective,
        "daily_budget_cents": daily_budget_cents,
        "status": "PAUSED",
    }


def create_ad_set(
    ads_account: dict,
    campaign_id: str,
    name: str,
    daily_budget_cents: int,
    targeting: dict,
    start_time: str,
    end_time: str,
) -> dict:
    account_id = ads_account.get("account_id", "")
    token = _get_token()
    if not account_id or not token:
        return {"error": "No account_id or token configured"}

    targeting_spec = {
        "geo_locations": targeting.get("geo_locations", {"countries": ["BR"]}),
        "age_min": targeting.get("age_min", 18),
        "age_max": targeting.get("age_max", 65),
    }

    result = _api_post(f"act_{account_id}/adsets", {
        "name": name,
        "campaign_id": campaign_id,
        "daily_budget": str(daily_budget_cents),
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "REACH",
        "targeting": json.dumps(targeting_spec),
        "start_time": start_time,
        "end_time": end_time,
        "status": "PAUSED",
        "access_token": token,
    })
    if "error" in result:
        return result

    return {
        "ads_account": ads_account.get("label", ""),
        "ad_set_id": result.get("id", ""),
        "campaign_id": campaign_id,
        "name": name,
        "daily_budget_cents": daily_budget_cents,
        "targeting": targeting_spec,
        "status": "PAUSED",
    }


def create_ad_creative(
    ads_account: dict,
    page_id: str,
    name: str,
    message: str,
    image_url: str,
    link_url: str,
) -> dict:
    account_id = ads_account.get("account_id", "")
    token = _get_token()
    if not account_id or not token:
        return {"error": "No account_id or token configured"}

    object_story_spec = {
        "page_id": page_id,
        "link_data": {
            "message": message,
            "link": link_url,
            "picture": image_url,
        },
    }

    result = _api_post(f"act_{account_id}/adcreatives", {
        "name": name,
        "object_story_spec": json.dumps(object_story_spec),
        "access_token": token,
    })
    if "error" in result:
        return result

    return {
        "ads_account": ads_account.get("label", ""),
        "creative_id": result.get("id", ""),
        "name": name,
        "page_id": page_id,
    }


def create_ad(
    ads_account: dict,
    name: str,
    ad_set_id: str,
    creative_id: str,
) -> dict:
    account_id = ads_account.get("account_id", "")
    token = _get_token()
    if not account_id or not token:
        return {"error": "No account_id or token configured"}

    result = _api_post(f"act_{account_id}/ads", {
        "name": name,
        "adset_id": ad_set_id,
        "creative": json.dumps({"creative_id": creative_id}),
        "status": "PAUSED",
        "access_token": token,
    })
    if "error" in result:
        return result

    return {
        "ads_account": ads_account.get("label", ""),
        "ad_id": result.get("id", ""),
        "name": name,
        "ad_set_id": ad_set_id,
        "creative_id": creative_id,
        "status": "PAUSED",
    }


def get_ad_insights(ads_account: dict, campaign_id: str) -> dict:
    account_id = ads_account.get("account_id", "")
    token = _get_token()
    if not account_id or not token:
        return {"error": "No account_id or token configured"}

    data = _api_get(f"{campaign_id}/insights", {
        "fields": "campaign_id,campaign_name,impressions,reach,clicks,spend,cpc,cpm,ctr,actions",
        "date_preset": "last_30d",
        "access_token": token,
    })
    if "error" in data:
        return data

    insights = data.get("data", [])
    return {
        "ads_account": ads_account.get("label", ""),
        "campaign_id": campaign_id,
        "insights": insights,
        "total_records": len(insights),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: meta_ads_client.py <command> [args]")
        print("\nCommands:")
        print("  accounts                                                        # List configured ads accounts")
        print("  campaigns [account]                                             # List active campaigns")
        print("  create_campaign <name> <objective> <daily_budget_cents> <start_time> <end_time> [account]")
        print("    objectives: OUTCOME_TRAFFIC | OUTCOME_ENGAGEMENT | OUTCOME_LEADS | OUTCOME_SALES")
        print("    times: ISO 8601 e.g. 2026-06-01T00:00:00+0000")
        print("  create_ad_set <campaign_id> <name> <daily_budget_cents> <start_time> <end_time> [account]")
        print("  create_creative <page_id> <name> <message> <image_url> <link_url> [account]")
        print("  create_ad <name> <ad_set_id> <creative_id> [account]           # Create ad (starts PAUSED)")
        print("  insights <campaign_id> [account]                                # Campaign metrics (30d)")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    try:
        if cmd == "accounts":
            result = {"accounts": [{"index": a["index"], "label": a["label"],
                                     "account_id": a["account_id"]} for a in _get_ads_accounts()],
                      "token_available": bool(_get_token())}
        elif cmd == "campaigns":
            acc = _get_ads_account(args[0] if args else None)
            result = get_campaigns(acc)
        elif cmd == "create_campaign":
            name = args[0] if len(args) > 0 else ""
            objective = args[1] if len(args) > 1 else ""
            budget = int(args[2]) if len(args) > 2 else 0
            start = args[3] if len(args) > 3 else ""
            end = args[4] if len(args) > 4 else ""
            acc = _get_ads_account(args[5] if len(args) > 5 else None)
            result = create_campaign(acc, name, objective, budget, start, end)
        elif cmd == "create_ad_set":
            campaign_id = args[0] if len(args) > 0 else ""
            name = args[1] if len(args) > 1 else ""
            budget = int(args[2]) if len(args) > 2 else 0
            start = args[3] if len(args) > 3 else ""
            end = args[4] if len(args) > 4 else ""
            acc = _get_ads_account(args[5] if len(args) > 5 else None)
            result = create_ad_set(acc, campaign_id, name, budget, {}, start, end)
        elif cmd == "create_creative":
            page_id = args[0] if len(args) > 0 else ""
            name = args[1] if len(args) > 1 else ""
            message = args[2] if len(args) > 2 else ""
            image_url = args[3] if len(args) > 3 else ""
            link_url = args[4] if len(args) > 4 else ""
            acc = _get_ads_account(args[5] if len(args) > 5 else None)
            result = create_ad_creative(acc, page_id, name, message, image_url, link_url)
        elif cmd == "create_ad":
            name = args[0] if len(args) > 0 else ""
            ad_set_id = args[1] if len(args) > 1 else ""
            creative_id = args[2] if len(args) > 2 else ""
            acc = _get_ads_account(args[3] if len(args) > 3 else None)
            result = create_ad(acc, name, ad_set_id, creative_id)
        elif cmd == "insights":
            campaign_id = args[0] if args else ""
            acc = _get_ads_account(args[1] if len(args) > 1 else None)
            result = get_ad_insights(acc, campaign_id)
        else:
            print(f"Unknown command: {cmd}")
            sys.exit(1)

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)
