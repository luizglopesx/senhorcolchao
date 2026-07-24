#!/usr/bin/env python3
"""
Gera o GOOGLE_ADS_REFRESH_TOKEN da Senhor Colchao.

Como rodar (no Terminal):
    cd "/Users/luizgustavo/Projetos/Senhor Colchao/senhor-colchao"
    python3 scripts/google-ads-refresh-token.py

O script abre o navegador, voce faz login com a conta que administra a MCC
(senhorcolchao@gmail.com), autoriza, e o refresh token e gravado direto no .env.
Sem instalar nada — usa so a biblioteca padrao do Python.
"""
import http.server
import socketserver
import urllib.parse
import urllib.request
import webbrowser
import threading
import json
import os
import sys
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
SCOPE = "https://www.googleapis.com/auth/adwords"
PORT = 8765
REDIRECT = f"http://localhost:{PORT}/"


def load_env(path):
    vals = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, v = s.split("=", 1)
            vals[k.strip()] = v.strip()
    return vals


def write_refresh_token(path, token):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if re.search(r"^GOOGLE_ADS_REFRESH_TOKEN=.*$", content, flags=re.M):
        content = re.sub(r"^GOOGLE_ADS_REFRESH_TOKEN=.*$",
                         f"GOOGLE_ADS_REFRESH_TOKEN={token}", content, flags=re.M)
    else:
        content += f"\nGOOGLE_ADS_REFRESH_TOKEN={token}\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


env = load_env(ENV_PATH)
CLIENT_ID = env.get("GOOGLE_ADS_CLIENT_ID", "")
CLIENT_SECRET = env.get("GOOGLE_ADS_CLIENT_SECRET", "")
if not CLIENT_ID or not CLIENT_SECRET:
    print("ERRO: faltam GOOGLE_ADS_CLIENT_ID / GOOGLE_ADS_CLIENT_SECRET no .env")
    sys.exit(1)

auth_code = {}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if "code" in params:
            auth_code["code"] = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                "<h2>Pronto! Pode fechar esta aba e voltar ao Terminal.</h2>".encode("utf-8"))
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, *args):
        pass


auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT,
    "response_type": "code",
    "scope": SCOPE,
    "access_type": "offline",
    "prompt": "consent",
})

print("\nAbrindo o navegador para login...")
print("Se nao abrir sozinho, copie e cole esta URL no navegador:\n")
print(auth_url + "\n")
threading.Thread(target=lambda: webbrowser.open(auth_url)).start()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Aguardando autorizacao em {REDIRECT} ...")
    while "code" not in auth_code:
        httpd.handle_request()

data = urllib.parse.urlencode({
    "code": auth_code["code"],
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT,
    "grant_type": "authorization_code",
}).encode()

try:
    resp = json.load(urllib.request.urlopen(
        urllib.request.Request("https://oauth2.googleapis.com/token", data=data)))
except urllib.error.HTTPError as e:
    print("ERRO ao trocar o codigo:", e.read().decode())
    sys.exit(1)

rt = resp.get("refresh_token")
if not rt:
    print("Nao veio refresh_token. Resposta:", resp)
    print("Dica: revogue o acesso em myaccount.google.com/permissions e rode de novo.")
    sys.exit(1)

write_refresh_token(ENV_PATH, rt)
print("\n==================================================")
print(" REFRESH TOKEN gerado e gravado no .env com sucesso!")
print(" (GOOGLE_ADS_REFRESH_TOKEN)")
print("==================================================\n")
