"""Gera SRT (estilo filme: até 2 linhas, ~42 caracteres por linha) a partir do transcript.json.

Uso: python make_srt.py <transcript.json> <saida.srt> --start S --end E
Os tempos são deslocados para o vídeo cortado (t - S); palavras fora de [S, E] são descartadas.
"""
import argparse
import json

MAX_CHARS = 74      # por legenda (2 linhas)
LINE_CHARS = 42
MAX_DUR = 5.0
GAP_BREAK = 0.7     # pausa que força nova legenda
MIN_DUR = 0.8


def ts(t):
    t = max(t, 0)
    h, rem = divmod(int(round(t * 1000)), 3600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def balance(text):
    """Quebra em 2 linhas o mais parecidas possível em tamanho."""
    ws = text.split()
    best = min(range(1, len(ws)), key=lambda i: abs(len(" ".join(ws[:i])) - len(" ".join(ws[i:]))))
    return [" ".join(ws[:best]), " ".join(ws[best:])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript")
    ap.add_argument("out")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=1e9)
    a = ap.parse_args()

    d = json.load(open(a.transcript, encoding="utf-8"))
    words = [w for s in d["segments"] for w in s["words"]
             if w["start"] >= a.start and w["end"] <= a.end + 0.5]

    # Uma legenda nunca atravessa segmentos do Whisper (que seguem as frases);
    # segmentos longos são quebrados de preferência na última vírgula.
    cues = []
    for seg in d["segments"]:
        ws = [w for w in seg["words"] if w["start"] >= a.start and w["end"] <= a.end + 0.5]
        cur = []
        for w in ws:
            if cur:
                text = "".join(x["word"] for x in cur).strip()
                gap = w["start"] - cur[-1]["end"]
                if gap > GAP_BREAK or w["end"] - cur[0]["start"] > MAX_DUR:
                    cues.append(cur); cur = []
                elif len(text) + len(w["word"]) > MAX_CHARS:
                    cut = max((i for i, x in enumerate(cur) if x["word"].rstrip().endswith(",")
                               and i >= len(cur) // 2), default=len(cur) - 1)
                    cues.append(cur[:cut + 1]); cur = cur[cut + 1:]
            cur.append(w)
        if cur:
            cues.append(cur)

    # Fragmentos de 1-2 palavras isolados por pausa (ex.: "A ... minha placa")
    # vão para a legenda seguinte; legendas curtas coladas na próxima são unidas.
    txt = lambda c: "".join(x["word"] for x in c).strip()
    fixed = []
    for i, c in enumerate(cues):
        nxt = cues[i + 1] if i + 1 < len(cues) else None
        if (len(c) <= 2 and nxt and nxt[0]["start"] - c[-1]["end"] > GAP_BREAK
                and len(txt(c + nxt)) <= MAX_CHARS):
            moved = [dict(w, start=nxt[0]["start"] - 0.3, end=nxt[0]["start"] - 0.3) for w in c]
            cues[i + 1] = moved + nxt
            continue
        if (fixed and len(txt(fixed[-1])) < 16 and c[0]["start"] - fixed[-1][-1]["end"] < 0.3
                and len(txt(fixed[-1] + c)) <= MAX_CHARS and c[-1]["end"] - fixed[-1][0]["start"] <= MAX_DUR):
            fixed[-1] = fixed[-1] + c
            continue
        fixed.append(c)
    cues = fixed

    with open(a.out, "w", encoding="utf-8") as f:
        for i, c in enumerate(cues, 1):
            st = c[0]["start"] - a.start
            en = max(c[-1]["end"] - a.start + 0.25, st + MIN_DUR)
            en = min(en, st + MAX_DUR + 1)
            if i < len(cues):
                en = min(en, cues[i][0]["start"] - a.start - 0.05)
            text = "".join(x["word"] for x in c).strip()
            lines = [text] if len(text) <= LINE_CHARS else balance(text)
            f.write(f"{i}\n{ts(st)} --> {ts(en)}\n" + "\n".join(lines) + "\n\n")
    print(f"OK {len(cues)} legendas -> {a.out}")


if __name__ == "__main__":
    main()
