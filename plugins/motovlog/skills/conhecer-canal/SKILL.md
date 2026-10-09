---
name: conhecer-canal
description: Monta o perfil de um canal de motovlog (canal.md) a partir do link do YouTube — coleta títulos, descrições, tags, views e miniaturas dos vídeos recentes, identifica o estilo do dono do canal e completa com uma conversa rápida (moto, câmera, cidade, sotaque, gírias). Use na primeira vez que o usuário for preparar vídeos de um canal, quando ele passar o link do canal, pedir para "configurar meu canal", "aprender o estilo do meu canal", "atualizar o canal.md" ou quando outra skill do plugin motovlog não encontrar o canal.md.
---

# Conhecer o canal → `canal.md`

> Feito e testado para canais de **motovlog**, num PC com Windows 11 e NVIDIA RTX 4060 Laptop (8 GB). Esta skill não usa GPU.

O `canal.md` é o que faz as outras skills (`video-para-youtube`, `metadados-youtube`, `capas-youtube` e as do plugin `edicao-de-video`) escreverem **no jeito do dono do canal**: vocabulário certo na transcrição, títulos no estilo dele, capas parecidas com as dele.

## Só para o canal do próprio usuário

Monte perfil apenas do canal **do usuário** (ou de um canal que ele administra). O perfil serve para escrever títulos, descrições e capas *como se fosse o dono*; fazer isso para o canal de outra pessoa seria produzir conteúdo em nome dela. Se o link não parecer ser do usuário, pergunte antes de seguir.

## 1. Pasta do canal

Pergunte (ou descubra pela memória/diretório atual) onde fica a pasta de trabalho do canal, ex.: `~/videos-youtube/`. Lá vão ficar `canal.md`, `estilo-capas/` e uma subpasta por vídeo.

## 2. Coletar dados públicos

```
pip install yt-dlp requests     # se faltar
python -I scripts/fetch_channel.py https://www.youtube.com/@canal <pasta-do-canal> --limit 20 --thumbs 4
```

Saídas:
- `canal_dados.json`: dados brutos.
- `canal_resumo.md`: vídeos ordenados por views, com título, descrição, tags e tags mais usadas.
- `estilo-capas/ref_1..4.jpg`: miniaturas dos vídeos mais vistos, que viram a referência de estilo das capas.

Às vezes o YouTube pede "confirme que não é um robô" ao abrir cada vídeo. Nesse caso só vêm títulos, views e miniaturas, sem descrições e tags. Para completar, rode de novo com `--cookies-from-browser edge` (ou `firefox`/`chrome`; no Windows o navegador precisa estar fechado), ou abra 3-4 vídeos pelo navegador (Claude in Chrome) e leia a descrição.

Abra as miniaturas de `estilo-capas/` e confira se representam o estilo que o usuário quer manter. Pergunte se ele quer trocar alguma.

## 3. Analisar o estilo

Leia o `canal_resumo.md` e extraia:
- **Títulos**: pessoa (1ª pessoa?), tamanho, caixa alta, padrões ("X: Y", "TESTEI...", pergunta), presença do modelo da moto, e quais formatos têm mais views.
- **Descrições**: número de parágrafos, tom (gírias, "pra", "cê"), emojis ou não, fechamento (pergunta, pedido de inscrição), "Linha do tempo".
- **Tags**: quantidade, minúsculas, termos fixos que aparecem em todo vídeo.
- **Motos e lugares** citados: modelos atuais e antigos, cidade, estradas.

## 4. Completar com o usuário

Pergunte só o que os dados não respondem, em poucas perguntas:
- moto atual (modelo exato, cor) e anteriores;
- câmera e microfone;
- cidade/região e sotaque;
- gírias ou nomes que costumam sair errados na transcrição;
- regras para as capas (ex.: sempre a moto em destaque, nunca o rosto).

## 5. Escrever `canal.md`

Use este formato. As outras skills procuram estas seções pelo nome:

```markdown
# Canal: <nome>

<tipo de canal, cidade/UF> — <url>

## Equipamento
- Moto atual: <modelo, cor>. Anteriores: ...
- Câmeras/microfone: ... (notas úteis, ex.: "usar o áudio do MP4, o WAV do mic satura com vento")
- PC/GPU: ...

## Vocabulário para transcrição
<1 parágrafo corrido, usado como prompt do Whisper: tipo de vídeo, cidade, sotaque, gírias, modelos de moto, ruas e lugares frequentes>

## Correções frequentes da transcrição
- "<como o Whisper escreve>" → <certo>
- Manter a fala do dono nas legendas: ...

## Estilo de metadados
- Títulos: ... (2-3 exemplos reais dos mais vistos)
- Descrição: ...
- Tags: ...

## Capas
- Referências em `estilo-capas/`. Linha de canal para os prompts: `<nome>, motovlog em <cidade (UF)>`.
- Regras: grafia exata do modelo da moto no adesivo, cenário da cidade do canal, ...
```

Mostre o `canal.md` ao usuário para ele ajustar. O arquivo fica só na máquina dele: não envie nem publique em lugar nenhum.
