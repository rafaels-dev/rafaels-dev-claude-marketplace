r"""Gera uma capa de YouTube (1280x720) via OpenRouter no estilo das miniaturas do canal.

Uso: python generate_cover.py --prompt "..." --out capa_A.png [--ref frame.jpg ...]
       [--style-dir estilo-capas] [--channel "Nome do canal (cidade)"]
       [--model openai/gpt-5.4-image-2] [--no-style] [--from-raw capa_A_raw.png]

O modelo recebe miniaturas do próprio canal (pasta estilo-capas/, procurada no diretório atual e
nos pais) como guia de estilo + frames reais do vídeo, e renderiza a capa inteira, inclusive o texto.
Se a imagem voltar fora de 16:9, é recortada no centro (o prompt pede margem de segurança).
--from-raw só refaz o recorte a partir de uma imagem já gerada (sem custo de API).
Chave: OPENROUTER_API_KEY na variável de ambiente ou num .env na pasta atual ou acima (--check-key confere).
"""
import argparse
import base64
import glob
import io
import os
import sys

import requests
from PIL import Image

API = "https://openrouter.ai/api/v1/chat/completions"

STYLE_GUIDE = """
Você é um designer de thumbnails de YouTube. Crie UMA thumbnail horizontal 16:9{channel}, seguindo o estilo
visual das miniaturas de referência do canal quando houver (as primeiras imagens anexadas). Estilo base:
- Fotografia hiper-realista com HDR forte, cores muito saturadas, céu dramático, contraste alto, nitidez exagerada.
- Título ENORME em fonte sans-serif condensada extra-bold (estilo Bebas/Impact), em CAIXA ALTA, com palavras em
  BRANCO e palavras de destaque em AMARELO, contorno preto grosso, levemente inclinado.
- O texto fica sobre faixas de pincelada grunge PRETAS e VERMELHAS (brush strokes com respingos e textura gasta).
- Elementos gráficos de apoio quando fizer sentido: setas amarelas desenhadas à mão, sublinhado amarelo de pincel,
  placas, papéis/tickets, ícones grandes, selos tipo "carimbo".
- Composição cheia e chamativa, o objeto principal do vídeo (ou a pessoa com ele) grande em primeiro plano, legível em tamanho pequeno.
- Escreva o texto em português do Brasil com a grafia EXATA pedida, com acentos corretos, sem letras extras.
- Mantenha todo o texto e o assunto principal dentro da área segura central (margem de ~6% em todas as bordas).
""".strip()


def find_up(name, start=None):
    """Procura um arquivo/pasta no diretório atual e nos pais."""
    d = os.path.abspath(start or os.getcwd())
    while True:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


SETUP_HELP = """Chave do OpenRouter não encontrada (pré-condição desta skill).
1. Crie uma conta em https://openrouter.ai e adicione créditos (Settings > Credits).
2. Gere uma chave em https://openrouter.ai/settings/keys
3. Configure de UM destes jeitos:
   a) arquivo .env na pasta de trabalho dos vídeos (ou numa pasta acima dela), com a linha:
        OPENROUTER_API_KEY=sk-or-...
   b) variável de ambiente do usuário (reinicie o Claude Code depois):
        Windows (PowerShell): [Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "sk-or-...", "User")
        macOS/Linux: export OPENROUTER_API_KEY="sk-or-..."  no ~/.zshrc ou ~/.bashrc"""


def load_key():
    """Variável de ambiente OPENROUTER_API_KEY; se não houver, o primeiro .env achado subindo
    a partir do diretório atual. Devolve (chave, origem) sem nunca imprimir a chave."""
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if key:
        return key, "variável de ambiente"
    path = find_up(".env")
    if path:
        for line in open(path, encoding="utf-8"):
            k, _, v = line.strip().removeprefix("export ").partition("=")
            if k.strip() == "OPENROUTER_API_KEY" and v.strip():
                return v.strip().strip('"').strip("'"), path
    return None, None


def data_url(path, max_w=1024):
    img = Image.open(path).convert("RGB")
    if img.width > max_w:
        img = img.resize((max_w, int(img.height * max_w / img.width)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def to_16x9(img, w=1280, h=720):
    """Recorta centralizado para 16:9 e redimensiona para 1280x720."""
    src_w, src_h = img.size
    target = w / h
    if src_w / src_h > target:
        nw = int(src_h * target)
        img = img.crop(((src_w - nw) // 2, 0, (src_w - nw) // 2 + nw, src_h))
    else:
        nh = int(src_w / target)
        img = img.crop((0, (src_h - nh) // 2, src_w, (src_h - nh) // 2 + nh))
    return img.resize((w, h), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-key", action="store_true", help="só confere se a chave existe (não mostra o valor)")
    ap.add_argument("--prompt", help="cena + texto exato da capa")
    ap.add_argument("--out")
    ap.add_argument("--ref", action="append", default=[], help="frame real do vídeo (objeto principal/cenário)")
    ap.add_argument("--model", default="openai/gpt-5.4-image-2")
    ap.add_argument("--no-style", action="store_true", help="não enviar as miniaturas de referência")
    ap.add_argument("--style-dir", help="pasta com miniaturas do canal (padrão: estilo-capas/ achada subindo)")
    ap.add_argument("--channel", default="", help='ex.: "Nome do Canal, vlog de viagens em Cidade (UF)"')
    ap.add_argument("--from-raw", help="pula a API e só recorta esta imagem")
    a = ap.parse_args()

    if a.check_key:
        key, origin = load_key()
        if not key:
            sys.exit(SETUP_HELP)
        print(f"ok (chave encontrada em: {origin})")
        return
    if not a.prompt or not a.out:
        ap.error("--prompt e --out são obrigatórios")

    if a.from_raw:
        to_16x9(Image.open(a.from_raw).convert("RGB")).save(a.out)
        print(f"OK {a.out}")
        return

    key, _ = load_key()
    if not key:
        sys.exit(SETUP_HELP)

    style_dir = a.style_dir or find_up("estilo-capas")
    styles = []
    if style_dir and not a.no_style:
        styles = sorted(p for ext in ("jpg", "jpeg", "png", "webp")
                        for p in glob.glob(os.path.join(style_dir, f"*.{ext}")))[:4]
    text = STYLE_GUIDE.format(channel=f' para o canal "{a.channel}"' if a.channel else "")
    if styles:
        text += f"\n\nAs {len(styles)} primeiras imagens são miniaturas do canal (referência de ESTILO, não copie o texto delas)."
    if a.ref:
        text += (f"\nAs {len(a.ref)} imagens seguintes são frames reais deste vídeo: use-as como referência "
                 "fiel do objeto principal (modelo, cor, formato, detalhes) e do cenário.")
    text += "\n\nCAPA DESTE VÍDEO:\n" + a.prompt

    content = [{"type": "text", "text": text}]
    content += [{"type": "image_url", "image_url": {"url": data_url(p)}} for p in styles + a.ref]

    r = requests.post(API, timeout=600, headers={"Authorization": f"Bearer {key}"}, json={
        "model": a.model,
        "modalities": ["image", "text"],
        "image_config": {"aspect_ratio": "16:9"},
        "messages": [{"role": "user", "content": content}],
    })
    if r.status_code != 200:
        sys.exit(f"HTTP {r.status_code}: {r.text[:800]}")
    msg = r.json()["choices"][0]["message"]
    images = msg.get("images") or []
    if not images:
        sys.exit(f"Nenhuma imagem retornada. Resposta: {str(msg)[:800]}")
    url = images[0]["image_url"]["url"]
    raw = base64.b64decode(url.split(",", 1)[1]) if url.startswith("data:") else requests.get(url, timeout=120).content
    src = Image.open(io.BytesIO(raw)).convert("RGB")
    src.save(os.path.splitext(a.out)[0] + "_raw.png")
    to_16x9(src).save(a.out)
    print(f"OK {a.out} (raw {src.size[0]}x{src.size[1]})")


if __name__ == "__main__":
    main()
