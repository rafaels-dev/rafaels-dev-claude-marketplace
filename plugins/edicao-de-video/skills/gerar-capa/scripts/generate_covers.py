"""Gera as 3 capas (A/B/C) em paralelo a partir de capas/prompts.md.

Uso: python generate_covers.py <pasta-do-video> [--only A,C] [--model ...] [--suffix _v2]
Formato do prompts.md (a linha "canal:" no topo é opcional):
    canal: Nome do Canal, vlog de viagens em Cidade (UF)
    ## A
    texto: TESTEI POR 30 DIAS | VALEU A PENA?    (linhas separadas por |; a IA renderiza o texto)
    ref: frames/f_220.jpg
    <descrição da cena e dos elementos gráficos>
--model troca o modelo (padrão do generate_cover.py: openai/gpt-5.4-image-2).
"""
import argparse
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generate_cover.py")


def channel_of(md):
    m = re.search(r"^canal:\s*(.+)$", md, re.M)
    return m.group(1).strip() if m else ""


def parse(md):
    out = []
    for key, body in re.findall(r"^## ([A-Z])\s*\n(.+?)(?=^## |\Z)", md, re.S | re.M):
        meta, prompt = {}, []
        for line in body.strip().splitlines():
            m = re.match(r"^(texto|posição|posicao|ref):\s*(.+)$", line.strip())
            if m:
                meta.setdefault(m.group(1).replace("posicao", "posição"), []).append(m.group(2).strip())
            elif line.strip():
                prompt.append(line.strip())
        out.append((key, meta, " ".join(prompt)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--only", default="")
    ap.add_argument("--model", default="")
    ap.add_argument("--suffix", default="", help="sufixo no nome do arquivo, ex.: _v2")
    a = ap.parse_args()
    os.chdir(a.folder)
    md = open("capas/prompts.md", encoding="utf-8").read()
    channel = channel_of(md)
    items = parse(md)
    if a.only:
        items = [i for i in items if i[0] in a.only.split(",")]

    def run(item):
        key, meta, prompt = item
        texto = meta.get("texto", [""])[0]
        if texto:
            lines = " / ".join(f'"{l.strip()}"' for l in texto.split("|"))
            prompt = f"Texto EXATO da capa, nesta ordem de linhas: {lines}.\n{prompt}"
        cmd = [sys.executable, "-I", SCRIPT, "--prompt", prompt, "--out", f"capas/capa_{key}{a.suffix}.png"]
        if a.model:
            cmd += ["--model", a.model]
        if channel:
            cmd += ["--channel", channel]
        for r in meta.get("ref", []):
            cmd += ["--ref", r]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        return key, r.returncode, (r.stdout + r.stderr).strip()[-600:]

    with ThreadPoolExecutor(len(items) or 1) as ex:
        for key, rc, out in ex.map(run, items):
            print(f"[{key}] {'OK' if rc == 0 else 'ERRO'}: {out}")


if __name__ == "__main__":
    main()
