#!/usr/bin/env python3
"""Upload local image to Imgur and return public URL."""

import base64
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

IMGUR_CLIENT_ID = "546c25a59c58ad7"  # public anonymous client ID


def upload(image_path: str) -> dict:
    path = Path(image_path)
    if not path.exists():
        return {"error": f"File not found: {image_path}"}

    with open(path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    data = urllib.parse.urlencode({"image": image_data, "type": "base64"}).encode()
    req = urllib.request.Request(
        "https://api.imgur.com/3/image",
        data=data,
        headers={"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            if result.get("success"):
                return {"url": result["data"]["link"], "delete_hash": result["data"]["deletehash"]}
            return {"error": "Upload failed", "detail": str(result)}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: upload_image.py <image_path>")
        sys.exit(1)
    result = upload(sys.argv[1])
    print(json.dumps(result, indent=2))
