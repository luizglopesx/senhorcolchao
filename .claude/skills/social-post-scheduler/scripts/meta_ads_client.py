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


def _api_post_multipart(path: str, fields: dict, file_field: str, file_path: str) -> dict:
    """POST with a file (multipart/form-data) — used for video/image uploads."""
    url = f"{BASE_URL}/{path}"
    boundary = "----MazyOSBoundary7f3c9a2e"
    body = bytearray()

    for key, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode())
        body.extend(f"{value}\r\n".encode())

    filename = os.path.basename(file_path)
    content_type = "video/mp4" if filename.lower().endswith(".mp4") else "application/octet-stream"
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    body.extend(f"--{boundary}\r\n".encode())
    body.extend(f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'.encode())
    body.extend(f"Content-Type: {content_type}\r\n\r\n".encode())
    body.extend(file_bytes)
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode())

    req = urllib.request.Request(url, data=bytes(body), method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", errors="replace")
        return {"error": f"HTTP {e.code}", "detail": body_txt[:500]}
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


def create_campaign_ctwa(ads_account: dict, name: str, start_time: str, end_time: str) -> dict:
    """Campanha CTWA (Click-to-WhatsApp) — sem orçamento no nível da campanha
    (o orçamento vive no ad set, igual ao padrão já usado na conta). Objetivo
    fixo OUTCOME_ENGAGEMENT + bid_strategy LOWEST_COST_WITHOUT_CAP, confirmados
    via API na campanha ativa 'Durma como Campeão' em 17/07/2026."""
    account_id = ads_account.get("account_id", "")
    token = _get_token()
    if not account_id or not token:
        return {"error": "No account_id or token configured"}

    result = _api_post(f"act_{account_id}/campaigns", {
        "name": name,
        "objective": "OUTCOME_ENGAGEMENT",
        "is_adset_budget_sharing_enabled": "false",
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
        "objective": "OUTCOME_ENGAGEMENT",
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


# Constantes da conta senhor_colchao — vindas do ad set real e ativo
# "Fase 1 | Copa/Lançamento" (Durma como Campeão), confirmadas via API em 17/07/2026
DEFAULT_PAGE_ID = "142661446468130"
DEFAULT_IG_USER_ID = "17841406065994132"
DEFAULT_WHATSAPP_PHONE = "551733233694"


def create_ad_set_full(
    ads_account: dict,
    campaign_id: str,
    name: str,
    daily_budget_cents: int,
    targeting: dict,
    start_time: str,
    end_time: str,
    page_id: str = DEFAULT_PAGE_ID,
    whatsapp_phone_number: str = DEFAULT_WHATSAPP_PHONE,
) -> dict:
    """Cria ad set CTWA (Click-to-WhatsApp) — optimization_goal CONVERSATIONS,
    destination_type WHATSAPP. Espera 'targeting' já pronto (raio + interesses)."""
    account_id = ads_account.get("account_id", "")
    token = _get_token()
    if not account_id or not token:
        return {"error": "No account_id or token configured"}

    promoted_object = {"page_id": page_id, "whatsapp_phone_number": whatsapp_phone_number}

    result = _api_post(f"act_{account_id}/adsets", {
        "name": name,
        "campaign_id": campaign_id,
        "daily_budget": str(daily_budget_cents),
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "CONVERSATIONS",
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "destination_type": "WHATSAPP",
        "promoted_object": json.dumps(promoted_object),
        "targeting": json.dumps(targeting),
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
        "targeting": targeting,
        "status": "PAUSED",
    }


def upload_image(ads_account: dict, file_path: str) -> dict:
    account_id = ads_account.get("account_id", "")
    token = _get_token()
    if not account_id or not token:
        return {"error": "No account_id or token configured"}
    if not os.path.exists(file_path):
        return {"error": f"Arquivo não encontrado: {file_path}"}

    result = _api_post_multipart(
        f"act_{account_id}/adimages",
        {"access_token": token},
        "source",
        file_path,
    )
    if "error" in result:
        return result

    images = result.get("images", {})
    first = next(iter(images.values()), {})
    return {
        "ads_account": ads_account.get("label", ""),
        "image_hash": first.get("hash", ""),
        "file_path": file_path,
    }


def upload_video(ads_account: dict, file_path: str, name: str) -> dict:
    account_id = ads_account.get("account_id", "")
    token = _get_token()
    if not account_id or not token:
        return {"error": "No account_id or token configured"}
    if not os.path.exists(file_path):
        return {"error": f"Arquivo não encontrado: {file_path}"}

    result = _api_post_multipart(
        f"act_{account_id}/advideos",
        {"name": name, "access_token": token},
        "source",
        file_path,
    )
    if "error" in result:
        return result

    return {
        "ads_account": ads_account.get("label", ""),
        "video_id": result.get("id", ""),
        "name": name,
        "file_path": file_path,
    }


def _build_welcome_message(intro_text: str, autofill_message: str) -> str:
    """Monta o page_welcome_message no mesmo formato usado pela conta hoje
    (template VISUAL_EDITOR com autofill_message + quick reply)."""
    payload = {
        "type": "VISUAL_EDITOR",
        "version": 2,
        "landing_screen_type": "welcome_message",
        "media_type": "text",
        "text_format": {
            "customer_action_type": "autofill_message",
            "message": {
                "autofill_message": {"content": autofill_message},
                "text": intro_text,
            },
        },
        "ai_generated_icebreaker_toggle_enabled": True,
        "user_edit": True,
        "surface": "visual_editor_new",
        "welcome_message_edited": True,
        "autofill_message_edited": True,
    }
    return json.dumps(payload, ensure_ascii=False)


def create_video_creative(
    ads_account: dict,
    video_id: str,
    name: str,
    title: str,
    message: str,
    link_description: str,
    intro_text: str,
    autofill_message: str,
    image_hash: str,
    page_id: str = DEFAULT_PAGE_ID,
    ig_user_id: str = DEFAULT_IG_USER_ID,
) -> dict:
    """Cria o ad creative de vídeo com CTA WHATSAPP_MESSAGE — mesma estrutura
    do criativo ativo da Orthoplus (confirmada via API em 17/07/2026).
    image_hash é obrigatório — usado como thumbnail do vídeo no anúncio."""
    account_id = ads_account.get("account_id", "")
    token = _get_token()
    if not account_id or not token:
        return {"error": "No account_id or token configured"}

    video_data = {
        "video_id": video_id,
        "title": title,
        "message": message,
        "link_description": link_description,
        "image_hash": image_hash,
        "call_to_action": {
            "type": "WHATSAPP_MESSAGE",
            "value": {"app_destination": "WHATSAPP", "link": "https://api.whatsapp.com/send"},
        },
        "page_welcome_message": _build_welcome_message(intro_text, autofill_message),
    }
    object_story_spec = {
        "page_id": page_id,
        "instagram_user_id": ig_user_id,
        "video_data": video_data,
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
        "video_id": video_id,
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


def get_adsets(ads_account: dict, campaign_id: str, active_only: bool = True) -> dict:
    token = _get_token()
    if not campaign_id or not token:
        return {"error": "No campaign_id or token configured"}

    params = {
        "fields": "id,name,status,effective_status,daily_budget,lifetime_budget,start_time,end_time,optimization_goal,billing_event",
        "access_token": token,
    }
    if active_only:
        params["effective_status"] = '["ACTIVE"]'

    data = _api_get(f"{campaign_id}/adsets", params)
    if "error" in data:
        return data

    return {
        "ads_account": ads_account.get("label", ""),
        "campaign_id": campaign_id,
        "adsets": data.get("data", []),
        "total": len(data.get("data", [])),
    }


def get_adset_insights(ads_account: dict, adset_id: str, date_preset: str = "this_week_mon_today") -> dict:
    token = _get_token()
    if not adset_id or not token:
        return {"error": "No adset_id or token configured"}

    data = _api_get(f"{adset_id}/insights", {
        "fields": "adset_id,adset_name,impressions,reach,clicks,spend,cpc,cpm,ctr,actions",
        "date_preset": date_preset,
        "access_token": token,
    })
    if "error" in data:
        return data

    insights = data.get("data", [])
    return {
        "ads_account": ads_account.get("label", ""),
        "adset_id": adset_id,
        "date_preset": date_preset,
        "insights": insights,
        "total_records": len(insights),
    }


def update_adset_status(ads_account: dict, adset_id: str, status: str) -> dict:
    token = _get_token()
    status = status.upper()
    if not adset_id or not token:
        return {"error": "No adset_id or token configured"}
    if status not in {"ACTIVE", "PAUSED"}:
        return {"error": "Invalid status. Valid: ACTIVE | PAUSED"}

    result = _api_post(adset_id, {
        "status": status,
        "access_token": token,
    })
    if "error" in result:
        return result

    return {
        "ads_account": ads_account.get("label", ""),
        "adset_id": adset_id,
        "status": status,
        "success": result.get("success"),
    }


def get_campaign_adsets_weekly_performance(ads_account: dict, campaign_id: str) -> dict:
    adsets_result = get_adsets(ads_account, campaign_id, active_only=True)
    if "error" in adsets_result:
        return adsets_result

    rows = []
    for adset in adsets_result.get("adsets", []):
        insight_result = get_adset_insights(ads_account, adset.get("id", ""))
        insight_rows = insight_result.get("insights", [])
        insight = insight_rows[0] if insight_rows else {}
        rows.append({
            "adset": adset,
            "insight": insight,
        })

    return {
        "ads_account": ads_account.get("label", ""),
        "campaign_id": campaign_id,
        "date_preset": "this_week_mon_today",
        "adsets": rows,
        "total": len(rows),
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
        print("  create_campaign_ctwa <name> <start_time> <end_time> [account]")
        print("    Campanha CTWA sem orçamento no nível campanha (orçamento fica no ad set) — usar com create_ad_set_full")
        print("  create_ad_set <campaign_id> <name> <daily_budget_cents> <start_time> <end_time> [account]")
        print("  create_ad_set_full <campaign_id> <name> <daily_budget_cents> <start_time> <end_time> <targeting_json_file> [account]")
        print("    CTWA (WhatsApp) — CONVERSATIONS + destination WHATSAPP. targeting_json_file tem geo_locations/age/flexible_spec")
        print("  upload_video <file_path> <name> [account]                      # Sobe vídeo, retorna video_id")
        print("  upload_image <file_path> [account]                             # Sobe imagem, retorna image_hash (thumbnail)")
        print("  create_video_creative <video_id> <name> <title> <message> <link_description> <intro_text> <autofill_message> <image_hash> [account]")
        print("    Criativo CTWA de vídeo (mesma estrutura do criativo ativo da conta)")
        print("  create_creative <page_id> <name> <message> <image_url> <link_url> [account]")
        print("  create_ad <name> <ad_set_id> <creative_id> [account]           # Create ad (starts PAUSED)")
        print("  insights <campaign_id> [account]                                # Campaign metrics (30d)")
        print("  adsets <campaign_id> [active|all] [account]                     # List ad sets")
        print("  adset_insights <adset_id> [date_preset] [account]               # Ad set metrics")
        print("  pause_adset <adset_id> [account]                                # Pause an ad set")
        print("  activate_adset <adset_id> [account]                             # Activate an ad set")
        print("  campaign_adsets_week <campaign_id> [account]                    # Active ad sets + this week metrics")
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
        elif cmd == "create_campaign_ctwa":
            name = args[0] if len(args) > 0 else ""
            start = args[1] if len(args) > 1 else ""
            end = args[2] if len(args) > 2 else ""
            acc = _get_ads_account(args[3] if len(args) > 3 else None)
            result = create_campaign_ctwa(acc, name, start, end)
        elif cmd == "create_ad_set":
            campaign_id = args[0] if len(args) > 0 else ""
            name = args[1] if len(args) > 1 else ""
            budget = int(args[2]) if len(args) > 2 else 0
            start = args[3] if len(args) > 3 else ""
            end = args[4] if len(args) > 4 else ""
            acc = _get_ads_account(args[5] if len(args) > 5 else None)
            result = create_ad_set(acc, campaign_id, name, budget, {}, start, end)
        elif cmd == "create_ad_set_full":
            campaign_id = args[0] if len(args) > 0 else ""
            name = args[1] if len(args) > 1 else ""
            budget = int(args[2]) if len(args) > 2 else 0
            start = args[3] if len(args) > 3 else ""
            end = args[4] if len(args) > 4 else ""
            targeting_path = args[5] if len(args) > 5 else ""
            acc = _get_ads_account(args[6] if len(args) > 6 else None)
            with open(targeting_path, encoding="utf-8") as f:
                targeting = json.load(f)
            result = create_ad_set_full(acc, campaign_id, name, budget, targeting, start, end)
        elif cmd == "upload_video":
            file_path = args[0] if len(args) > 0 else ""
            name = args[1] if len(args) > 1 else ""
            acc = _get_ads_account(args[2] if len(args) > 2 else None)
            result = upload_video(acc, file_path, name)
        elif cmd == "upload_image":
            file_path = args[0] if len(args) > 0 else ""
            acc = _get_ads_account(args[1] if len(args) > 1 else None)
            result = upload_image(acc, file_path)
        elif cmd == "create_video_creative":
            video_id = args[0] if len(args) > 0 else ""
            name = args[1] if len(args) > 1 else ""
            title = args[2] if len(args) > 2 else ""
            message = args[3] if len(args) > 3 else ""
            link_description = args[4] if len(args) > 4 else ""
            intro_text = args[5] if len(args) > 5 else ""
            autofill_message = args[6] if len(args) > 6 else ""
            image_hash = args[7] if len(args) > 7 else ""
            acc = _get_ads_account(args[8] if len(args) > 8 else None)
            result = create_video_creative(
                acc, video_id, name, title, message, link_description, intro_text, autofill_message, image_hash
            )
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
        elif cmd == "adsets":
            campaign_id = args[0] if args else ""
            active_only = (args[1].lower() if len(args) > 1 else "active") != "all"
            account_arg_index = 2 if len(args) > 1 else 1
            acc = _get_ads_account(args[account_arg_index] if len(args) > account_arg_index else None)
            result = get_adsets(acc, campaign_id, active_only=active_only)
        elif cmd == "adset_insights":
            adset_id = args[0] if args else ""
            date_preset = args[1] if len(args) > 1 else "this_week_mon_today"
            acc = _get_ads_account(args[2] if len(args) > 2 else None)
            result = get_adset_insights(acc, adset_id, date_preset=date_preset)
        elif cmd == "pause_adset":
            adset_id = args[0] if args else ""
            acc = _get_ads_account(args[1] if len(args) > 1 else None)
            result = update_adset_status(acc, adset_id, "PAUSED")
        elif cmd == "activate_adset":
            adset_id = args[0] if args else ""
            acc = _get_ads_account(args[1] if len(args) > 1 else None)
            result = update_adset_status(acc, adset_id, "ACTIVE")
        elif cmd == "campaign_adsets_week":
            campaign_id = args[0] if args else ""
            acc = _get_ads_account(args[1] if len(args) > 1 else None)
            result = get_campaign_adsets_weekly_performance(acc, campaign_id)
        else:
            print(f"Unknown command: {cmd}")
            sys.exit(1)

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)
