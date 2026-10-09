---
name: gerar-capa
description: Gera capas (miniaturas/thumbnails) de YouTube de alto impacto via OpenRouter com o melhor modelo de imagem disponível — a IA renderiza a imagem inteira com o título, no estilo das miniaturas do próprio canal (HDR saturado, título enorme sobre pinceladas grunge, setas, objeto principal em destaque), usando frames reais do vídeo como referência. Use quando o usuário pedir "capa", "thumbnail", "miniatura", "3 opções de capa pra teste A/B", "refaz a capa", ou reclamar de uma capa, mesmo que não fale em OpenRouter.
---

# Gerar capa (thumbnail)

> Testado em vídeos de motovlog, num PC com Windows 11 e **NVIDIA RTX 4060 Laptop (8 GB)**. A imagem é gerada na nuvem (OpenRouter); a máquina local só extrai frames e recorta.

## Pré-condição: OpenRouter configurado

A variável de ambiente `OPENROUTER_API_KEY` precisa existir **antes** de usar esta skill. Verifique primeiro, sem mostrar o valor: `python -c "import os;print('ok' if os.environ.get('OPENROUTER_API_KEY') else 'faltando')"`. Se estiver faltando, pare e passe ao usuário estes passos (o script também imprime isso):

1. Crie uma conta em https://openrouter.ai e adicione créditos (Settings → Credits). Cada capa custa alguns centavos de dólar.
2. Gere uma chave em https://openrouter.ai/settings/keys.
3. Defina a variável de ambiente do usuário e reinicie o Claude Code para ela ser carregada:
   - Windows (PowerShell): `[Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "sk-or-...", "User")`
   - macOS/Linux: `export OPENROUTER_API_KEY="sk-or-..."` no `~/.zshrc` ou `~/.bashrc`

Nunca imprima, grave em arquivo nem peça a chave no chat: quem configura é o usuário. Outros requisitos: Python com `requests` e `Pillow`.

## Por que este estilo

Capa minimalista com o texto sobreposto por script fica fraca e foi rejeitada na prática. O que funciona é a IA renderizar a **capa inteira, inclusive o texto**, imitando as miniaturas do canal. O estilo base (já embutido no script) é: fotografia hiper-realista com HDR forte e cores saturadas, céu dramático, título enorme em fonte condensada extra-bold em caixa alta (branco + destaque amarelo, contorno preto) sobre pinceladas grunge pretas/vermelhas, setas amarelas desenhadas à mão, objeto principal grande em primeiro plano, composição cheia. As miniaturas de referência do canal refinam esse estilo.

## 1. Escolher o modelo

Padrão: `openai/gpt-5.4-image-2` (out/2026), que devolve 16:9 nativo (1280x720) e escreve texto em português muito bem. Saem modelos novos toda hora, então confira antes:

```
curl -s https://openrouter.ai/api/v1/models | python -c "import json,sys;[print(m['id']) for m in json.load(sys.stdin)['data'] if 'image' in m['architecture'].get('output_modalities',[])]"
```

Se o usuário pedir OpenAI, use o `openai/*-image*` mais novo; senão, o melhor disponível (ex.: `google/gemini-nano-banana-*`). Evite os antigos `openai/gpt-5-image*`: devolvem 1024x1024, e o recorte para 16:9 corta o título.

## 2. Referências

- **Estilo**: pasta `estilo-capas/` na pasta de trabalho, com 3-4 miniaturas do canal (o script acha sozinho ou recebe `--style-dir`). Se não existir, peça ao usuário miniaturas que ele goste e salve lá, redimensionadas a 1280px.
- **Frames do próprio vídeo** (a base de cada capa): extraia candidatos nítidos e olhe a folha de contato:
  ```
  python -I scripts/extract_frames.py video.mp4 <pasta-do-video>/frames --transcript transcript.json --keywords "palavra1,palavra2"
  ```
  O script pega ~24 instantes espalhados pelo vídeo, mais os momentos em que o transcript cita as palavras-chave do assunto. Descarta os frames borrados, mantém os 12 mais nítidos e gera `frames/folha_de_contato.jpg`. Abra a folha (Read) e escolha **um frame diferente para cada capa**: o teste A/B fica mais rico quando as capas variam também na cena real, não só no texto. Prefira frames que mostrem o objeto principal, o lugar ou um momento marcante do vídeo. Para pegar um instante específico: `ffmpeg -ss T -i video.mp4 -frames:v 1 -vf scale=1280:-2 frames/f_T.jpg`.

## 3. Prompts: `capas/prompts.md`

Para teste A/B, faça 3 conceitos **bem diferentes**: o teste só ensina algo se as capas forem diferentes. Cada um vai casado com um título e parte de um frame diferente do vídeo (linha `ref:`). Ideias: o frame real realçado + elementos do tema; antes × depois com divisória de pincel; pessoa reagindo ou mostrando algo. No texto do prompt, diga como usar o frame: "use o frame como base da cena" (fiel ao vídeo) ou "use o frame só como referência do objeto/lugar" (cena recriada).

```
canal: Nome do Canal, vlog de viagens em Cidade (UF)

## A
texto: TESTEI POR 30 DIAS | VALEU A PENA?
ref: frames/f_120.jpg
<onde fica o título e a cor de cada linha; o objeto principal (modelo, cor, logos/textos com grafia exata);
cenário real do lugar; elementos gráficos (setas, ícones, X vermelho, selos...)>
```

O texto da capa tem 2-6 palavras fortes, com as linhas separadas por `|`. Peça sempre a grafia exata de nomes e logos que aparecem no objeto, e um cenário coerente com o lugar real do vídeo. A IA tende a inventar letras em logos e a colocar cartões-postais famosos de outras cidades.

## 4. Gerar

```
python -I scripts/generate_covers.py <pasta-do-video>                         # A, B e C em paralelo, ~1-2 min
python -I scripts/generate_covers.py <pasta-do-video> --only B --suffix _v2   # refaz uma sem sobrescrever
```

Cada capa sai em `capas/capa_X.png` (1280x720), mais `capa_X_raw.png` (o original do modelo). Para uma capa avulsa: `python -I scripts/generate_cover.py --prompt "..." --ref frame.jpg --out capa.png [--channel "..."]`.

## 5. Conferir antes de mostrar

Abra as imagens e confira:
- título com grafia exata e acentos;
- objeto parecido com o real, com nomes e logos corretos;
- cenário plausível;
- nada estranho em destaque.

Texto miúdo ilegível no fundo é aceitável. Erro no título ou no nome do objeto não é: refaça só aquela capa com `--only`. Guarde as versões rejeitadas em `capas/v1/` e mantenha `capa_A/B/C.png` como as oficiais.
