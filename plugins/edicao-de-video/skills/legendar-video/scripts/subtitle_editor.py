"""Editor local de legendas sincronizado com o vídeo.

Uso: python subtitle_editor.py <video.mp4> <legendas.srt> [--port 8765] [--flag 62,67]
Abre http://localhost:8765 — cada alteração é salva direto no .srt (backup em .srt.bak na 1ª gravação).
"""
import argparse
import json
import os
import re
import shutil
import webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))


def ts_to_s(t):
    h, m, rest = t.strip().replace(".", ",").split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def s_to_ts(x):
    ms = int(round(max(x, 0) * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def parse_srt(text):
    cues = []
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n").strip()):
        lines = block.split("\n")
        i = next((k for k, l in enumerate(lines) if "-->" in l), None)
        if i is None:
            continue
        a, b = lines[i].split("-->")
        cues.append({"start": ts_to_s(a), "end": ts_to_s(b), "text": "\n".join(lines[i + 1:]).strip()})
    return cues


def write_srt(cues):
    cues = sorted(cues, key=lambda c: c["start"])
    return "\n".join(f"{n}\n{s_to_ts(c['start'])} --> {s_to_ts(c['end'])}\n{c['text'].strip()}\n"
                     for n, c in enumerate(cues, 1))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            return self._send(200, open(os.path.join(HERE, "subtitle_editor.html"), encoding="utf-8").read(),
                              "text/html; charset=utf-8")
        if self.path == "/api/srt":
            cues = parse_srt(open(self.server.srt, encoding="utf-8").read())
            return self._send(200, json.dumps({"cues": cues, "flags": self.server.flags,
                                               "name": os.path.basename(self.server.srt)}, ensure_ascii=False))
        if self.path.startswith("/video"):
            return self._video()
        self._send(404, "{}")

    def do_PUT(self):
        if self.path != "/api/srt":
            return self._send(404, "{}")
        cues = json.loads(self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8"))["cues"]
        if not self.server.backed_up:
            shutil.copyfile(self.server.srt, self.server.srt + ".bak")
            self.server.backed_up = True
        tmp = self.server.srt + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(write_srt(cues))
        os.replace(tmp, self.server.srt)
        self._send(200, json.dumps({"ok": True, "count": len(cues)}))

    def _video(self):
        path, size = self.server.video, os.path.getsize(self.server.video)
        rng = self.headers.get("Range")
        start, end = 0, size - 1
        if rng:
            m = re.match(r"bytes=(\d*)-(\d*)", rng)
            if m.group(1):
                start = int(m.group(1))
                end = int(m.group(2)) if m.group(2) else min(start + 8 * 1024 * 1024, size) - 1
            else:
                start = size - int(m.group(2))
        self.send_response(206 if rng else 200)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        if rng:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        try:
            with open(path, "rb") as f:
                f.seek(start)
                left = end - start + 1
                while left > 0:
                    chunk = f.read(min(1024 * 1024, left))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    left -= len(chunk)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("srt")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--flag", default="", help="números de legendas duvidosas, ex.: 62,67")
    ap.add_argument("--no-browser", action="store_true")
    a = ap.parse_args()

    srv = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    srv.video, srv.srt, srv.backed_up = os.path.abspath(a.video), os.path.abspath(a.srt), False
    srv.flags = [int(x) for x in a.flag.split(",") if x.strip()]
    url = f"http://localhost:{a.port}"
    print(f"Editor de legendas em {url}  (Ctrl+C para sair)", flush=True)
    if not a.no_browser:
        webbrowser.open(url)
    srv.serve_forever()


if __name__ == "__main__":
    main()
