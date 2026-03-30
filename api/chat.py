"""
Vercel serverless function: POST /api/chat with body { "message": "..." } -> { "answer", "lang" }
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from bot_engine import answer_fallback, answer_with_openai, detect_language


def _read_body(handler: BaseHTTPRequestHandler) -> dict:
    content_length = int(handler.headers.get("Content-Length", 0))
    if content_length == 0:
        return {}
    raw = handler.rfile.read(content_length)
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return {}


def _send_json(handler: BaseHTTPRequestHandler, status: int, data: dict) -> None:
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        body = _read_body(self)
        message = (body.get("message") or body.get("query") or "").strip()
        if not message:
            _send_json(self, 400, {"error": "Missing message", "answer": ""})
            return
        try:
            use_ai = bool(os.environ.get("OPENAI_API_KEY"))
            if use_ai:
                answer = answer_with_openai(message)
            else:
                answer = answer_fallback(message)
            lang = detect_language(message)
            _send_json(self, 200, {"answer": answer, "lang": lang})
        except Exception as e:
            _send_json(
                self,
                500,
                {
                    "error": str(e),
                    "answer": "申し訳ありません。エラーが発生しました。 / An error occurred.",
                },
            )
