---
description: Gera 3 capas de YouTube para teste A/B via OpenRouter, a partir de frames do próprio vídeo, no estilo das minhas miniaturas
argument-hint: "<pasta do vídeo> [títulos ou ideia de cada capa]"
---

Crie 3 capas para teste A/B: $ARGUMENTS

- Use a skill `gerar-capa`.
- Antes de tudo, confira se a variável de ambiente `OPENROUTER_API_KEY` existe (sem mostrar o valor). Se não existir, pare e me passe as instruções de configuração.
- Extraia frames nítidos com `extract_frames.py`, olhe a folha de contato e use um frame diferente em cada capa.
- Use as miniaturas de `estilo-capas/` como referência e escreva 3 conceitos bem diferentes em `capas/prompts.md`, cada um casado com um título.
- Use o melhor modelo de imagem disponível no OpenRouter (confira a lista antes).
- Abra as 3 imagens, refaça as que tiverem erro de grafia no título ou no objeto, e me mostre o resultado.
