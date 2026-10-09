"""Coleta dados públicos de um canal do YouTube (sem API key) para montar o canal.md.

Uso: python fetch_channel.py <url-do-canal> <pasta-do-canal> [--limit 20] [--thumbs 4]
                             [--cookies-from-browser chrome|edge|firefox]
Gera em <pasta-do-canal>:
  canal_dados.json      títulos, views, duração (+ descrições e tags quando o YouTube deixar)
  canal_resumo.md       resumo legível (ordenado por views) para escrever o canal.md
  estilo-capas/*.jpg    miniaturas dos vídeos mais vistos (referência de estilo para as capas)
Requer: pip install yt-dlp requests
Às vezes o YouTube pede "confirme que não é um robô" ao abrir cada vídeo: aí só a listagem
(títulos, views, duração, miniaturas) é coletada. Para pegar descrições e tags, use
--cookies-from-browser (navegador logado no YouTube; o Chrome precisa estar fechado no Windows)
ou leia algumas páginas de vídeo pelo navegador.
"""
import argparse
import json
import os
import re
from collections import Counter

import requests
import yt_dlp


def videos_url(url):
    url = url.rstrip("/")
    return url if re.search(r"/(videos|streams|shorts)$", url) else url + "/videos"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("folder")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--thumbs", type=int, default=4)
    ap.add_argument("--cookies-from-browser", dest="browser")
    a = ap.parse_args()
    os.makedirs(a.folder, exist_ok=True)

    # lang=pt evita títulos traduzidos automaticamente para inglês
    quiet = {"quiet": True, "no_warnings": True, "skip_download": True,
             "extractor_args": {"youtube": {"lang": ["pt"]}}}
    if a.browser:
        quiet["cookiesfrombrowser"] = (a.browser,)
    with yt_dlp.YoutubeDL({**quiet, "extract_flat": True, "playlistend": a.limit}) as ydl:
        listing = ydl.extract_info(videos_url(a.url), download=False)
    channel = {
        "nome": listing.get("channel") or listing.get("uploader") or listing.get("title"),
        "url": listing.get("channel_url") or a.url,
        "inscritos": listing.get("channel_follower_count"),
        "descricao": listing.get("description", ""),
    }

    videos, blocked = [], 0
    with yt_dlp.YoutubeDL(quiet) as ydl:
        for entry in (listing.get("entries") or [])[: a.limit]:
            # dados da listagem: sempre disponíveis
            v = {
                "titulo": entry.get("title"),
                "url": entry.get("url"),
                "data": None,
                "views": entry.get("view_count") or 0,
                "duracao_s": entry.get("duration"),
                "tags": [],
                "descricao": "",
                "thumbnail": f"https://i.ytimg.com/vi/{entry['id']}/maxresdefault.jpg",
            }
            if blocked < 2:  # depois de 2 bloqueios seguidos, nem tenta o resto
                try:
                    info = ydl.extract_info(entry["url"], download=False)
                    v.update(titulo=info.get("title") or v["titulo"], data=info.get("upload_date"),
                             tags=info.get("tags") or [], descricao=info.get("description") or "",
                             thumbnail=info.get("thumbnail") or v["thumbnail"])
                    blocked = 0
                except yt_dlp.utils.DownloadError as e:
                    blocked += 1
                    print(f"sem detalhes de {entry.get('url')}: {str(e).splitlines()[0][:120]}")
            videos.append(v)
            print(f"ok {v['titulo']}")
    if blocked:
        print("\nAVISO: o YouTube bloqueou os detalhes (descrição/tags). Só a listagem foi coletada.")

    json.dump({"canal": channel, "videos": videos},
              open(os.path.join(a.folder, "canal_dados.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    top = sorted(videos, key=lambda v: v["views"], reverse=True)
    style_dir = os.path.join(a.folder, "estilo-capas")
    os.makedirs(style_dir, exist_ok=True)
    saved = []
    for i, v in enumerate(top[: a.thumbs], 1):
        if not v["thumbnail"]:
            continue
        r = requests.get(v["thumbnail"], timeout=60)
        if not r.ok and "maxresdefault" in v["thumbnail"]:
            r = requests.get(v["thumbnail"].replace("maxresdefault", "hqdefault"), timeout=60)
        if r.ok:
            path = os.path.join(style_dir, f"ref_{i}.jpg")
            open(path, "wb").write(r.content)
            saved.append(path)

    tag_count = Counter(t.lower() for v in videos for t in v["tags"])
    lines = [f"# {channel['nome']}", "", f"URL: {channel['url']}",
             f"Inscritos: {channel['inscritos']}", "", "## Descrição do canal", channel["descricao"], "",
             "## Vídeos (mais vistos primeiro)"]
    for v in top:
        mins = f"{(v['duracao_s'] or 0) // 60}min"
        lines += [f"### {v['titulo']}", f"{v['views']} views · {mins} · {v['data']} · {v['url']}",
                  "Descrição:", v["descricao"].strip()[:1200], "Tags: " + ", ".join(v["tags"]), ""]
    lines += ["## Tags mais usadas", ", ".join(f"{t} ({n})" for t, n in tag_count.most_common(40))]
    open(os.path.join(a.folder, "canal_resumo.md"), "w", encoding="utf-8").write("\n".join(lines))
    print(f"\nOK {len(videos)} vídeos, {len(saved)} miniaturas em {style_dir}")


if __name__ == "__main__":
    main()
