---
description: Cria 3 capas de motovlog para teste A/B com a minha moto em destaque, a partir de frames do vídeo
argument-hint: "<pasta do vídeo> [o que refazer, ex.: \"refaz a B, nome da moto errado\"]"
---

Faça (ou refaça) as capas deste vídeo de motovlog: $ARGUMENTS

- Use a skill `capas-youtube`, que segue a skill `gerar-capa` (plugin edicao-de-video).
- Confira antes se a variável `OPENROUTER_API_KEY` existe (sem mostrar o valor); se faltar, pare e me diga como configurar.
- Moto em destaque, com o modelo escrito exatamente como no `canal.md`, e cenário da minha cidade, sem cartões-postais de outras cidades.
- Um frame diferente do vídeo para cada capa, casando cada capa com um título do `youtube.txt`.
- Se eu pedir para refazer uma, use `--only` e `--suffix` para não sobrescrever, e guarde as rejeitadas em `capas/v1/`.
- Me mostre as capas antes de considerar pronto.
