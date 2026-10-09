"""Extrai frames candidatos do vídeo para servir de base às capas.

Uso: python extract_frames.py <video.mp4> <pasta-saida> [--count 24] [--keep 12] [--transcript transcript.json]
- Amostra --count instantes espalhados pelo vídeo (pula 3% do começo e do fim) e, se houver
  transcript, também os momentos de frases com palavras-chave do assunto (--keywords).
- Mede a nitidez de cada frame e mantém os --keep mais nítidos (câmera tremida/borrada fica de fora).
- Gera folha_de_contato.jpg com todos numerados (f_<segundos>.jpg) para escolher rápido.
"""
import argparse
import json
import os
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageStat


def duration(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                         capture_output=True, text=True).stdout
    return float(out.strip())


def grab(video, t, path):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", video,
                    "-frames:v", "1", "-vf", "scale=1280:-2", "-q:v", "2", path], check=True)


def sharpness(path):
    g = Image.open(path).convert("L").resize((640, 360))
    return ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES)).var[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("out")
    ap.add_argument("--count", type=int, default=24)
    ap.add_argument("--keep", type=int, default=12)
    ap.add_argument("--transcript")
    ap.add_argument("--keywords", default="", help="palavras do assunto, separadas por vírgula")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    dur = duration(a.video)
    times = [dur * (0.03 + 0.94 * i / max(a.count - 1, 1)) for i in range(a.count)]
    if a.transcript and a.keywords:
        kws = [k.strip().lower() for k in a.keywords.split(",") if k.strip()]
        for s in json.load(open(a.transcript, encoding="utf-8"))["segments"]:
            if any(k in s["text"].lower() for k in kws):
                times.append(s["start"] + 0.5)
    times = sorted({round(t) for t in times if 0 < t < dur})

    scored = []
    for t in times:
        path = os.path.join(a.out, f"f_{t}.jpg")
        grab(a.video, t, path)
        scored.append((sharpness(path), t, path))
    scored.sort(reverse=True)
    keep = sorted(scored[: a.keep], key=lambda x: x[1])
    for _, _, path in scored[a.keep:]:
        os.remove(path)

    # folha de contato 4 colunas
    tw, th, cols = 320, 180, 4
    rows = (len(keep) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), "black")
    d = ImageDraw.Draw(sheet)
    for i, (_, t, path) in enumerate(keep):
        im = Image.open(path).resize((tw, th))
        x, y = (i % cols) * tw, (i // cols) * th
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 90, y + 22], fill="black")
        d.text((x + 5, y + 5), f"f_{t}.jpg", fill="yellow")
    sheet_path = os.path.join(a.out, "folha_de_contato.jpg")
    sheet.save(sheet_path, quality=88)
    print(f"OK {len(keep)} frames em {a.out} (folha: {sheet_path})")
    for s, t, path in keep:
        print(f"  {os.path.basename(path)}  nitidez={s:.0f}")


if __name__ == "__main__":
    main()
