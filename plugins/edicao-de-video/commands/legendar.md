---
description: Gera legendas estilo filme, abre o editor de revisão sincronizado e, após minha aprovação, queima no vídeo em 4K
argument-hint: "<pasta do vídeo (com transcript.json e corte.mp4)>"
---

Legende este vídeo: $ARGUMENTS

- Use a skill `legendar-video`.
- Gere o `legendas.srt` (amarelo com borda preta, até 2 linhas) e revise você mesmo pontuação e nomes próprios, mantendo o meu jeito de falar (pra, tá, cê).
- Gere o proxy 720p e abra o editor de revisão em http://localhost:8765, marcando as legendas duvidosas com `--flag`.
- PARE e espere eu dizer que terminei a revisão. Não queime legenda sem a minha aprovação.
- Depois da aprovação: mostre o que eu mudei, teste 5 s, renderize o `final_legendado.mp4` na GPU e confira um frame do meio contra o SRT.
