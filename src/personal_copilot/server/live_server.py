"""
Real-Time Live Web Server (`src/personal_copilot/server/live_server.py`)
Serves:
1. `GET /` -> React SPA Dashboard (from frontend/dist) or fallback Minimalist HTML
2. `GET /assets/...` -> Static JS/CSS assets compiled by Vite
3. `GET /api/data` -> Live JSON payload of all Graph Nodes, Chunks, and Activity Logs
4. `POST /api/sync` -> Triggers live database re-sync
"""

from __future__ import annotations

import argparse
import http.server
import json
import mimetypes
import socketserver
from pathlib import Path

from personal_copilot.lakehouse.data_extractor import extract_live_data

PORT = 8765
PROJECT_ROOT = Path(__file__).resolve().parents[3]
FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist"


class LiveDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def _send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Cache-Control")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self) -> None:
        # 1. API: Live JSON data
        if self.path == "/api/data":
            data = extract_live_data()
            payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(payload)
            return

        # 2. Static snapshot images
        if self.path.startswith("/data/snapshots/"):
            snap_file = PROJECT_ROOT / self.path.lstrip("/")
            if snap_file.exists() and snap_file.is_file():
                content = snap_file.read_bytes()
                mime = mimetypes.guess_type(str(snap_file))[0] or "image/png"
                self.send_response(200)
                self._send_cors_headers()
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return

        # 3. Static assets from compiled React frontend/dist/assets/
        if self.path.startswith("/assets/") and FRONTEND_DIST.exists():
            asset_file = FRONTEND_DIST / self.path.lstrip("/")
            if asset_file.exists() and asset_file.is_file():
                content = asset_file.read_bytes()
                mime = mimetypes.guess_type(str(asset_file))[0] or "application/octet-stream"
                self.send_response(200)
                self._send_cors_headers()
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "public, max-age=31536000, immutable")
                self.end_headers()
                self.wfile.write(content)
                return

        # 4. Root /: Serve React SPA index.html
        if self.path == "/" or self.path.startswith("/index"):
            react_index = FRONTEND_DIST / "index.html"
            if react_index.exists():
                encoded = react_index.read_bytes()
            else:
                encoded = b"<h1>React SPA not built yet.</h1><p>Run <code>cd frontend && npm run build</code> to compile the frontend.</p>"

            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(encoded)
            return

        super().do_GET()

    def do_POST(self) -> None:
        if self.path == "/api/sync":
            from personal_copilot.dag import run_daily_knowledge_dag

            res = run_daily_knowledge_dag()
            payload = json.dumps(res, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(payload)
            return

        self.send_response(404)
        self._send_cors_headers()
        self.end_headers()


def run_live_server(port: int = PORT) -> None:
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), LiveDashboardHandler) as httpd:
        has_react = (FRONTEND_DIST / "index.html").exists()
        mode_str = "React 19 SPA (Vite Production Build)" if has_react else "Minimalist Server HTML"
        print(f"Personal Copilot Live Server running at: http://localhost:{port}")
        print(f"Mode: {mode_str}")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Live Dashboard Web Server")
    parser.add_argument("--port", type=int, default=PORT, help=f"Server port (default: {PORT})")
    args = parser.parse_args()
    run_live_server(port=args.port)
