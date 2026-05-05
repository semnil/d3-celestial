#!/usr/bin/env python3
"""sky.html 配信サーバー。.env から LAT/LON を読み込みプレースホルダを置換して返す。"""

import http.server
import os
import socketserver
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = int(os.environ.get("PORT", 8080))


def load_env(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


env = load_env(ROOT / ".env")
LAT = env.get("LAT")
LON = env.get("LON")

if not LAT or not LON:
    sys.stderr.write(
        "Error: LAT / LON not set. Copy .env.example to .env and edit values.\n"
    )
    sys.exit(1)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path in ("/", "/sky.html"):
            html = (ROOT / "sky.html").read_text(encoding="utf-8")
            html = html.replace("__LAT__", LAT).replace("__LON__", LON)
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, format: str, *args: object) -> None:
        sys.stderr.write("[serve] " + format % args + "\n")


if __name__ == "__main__":
    os.chdir(ROOT)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        sys.stderr.write(f"sky.html: http://localhost:{PORT}/sky.html\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            sys.stderr.write("\nstopped\n")
