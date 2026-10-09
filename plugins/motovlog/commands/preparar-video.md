---
description: Leva um vídeo bruto de motovlog até estar pronto pro YouTube — transcrição, corte, legendas revisadas, títulos A/B, descrição, tags e 3 capas
argument-hint: "<caminho do vídeo bruto> [observações]"
---

Prepare este vídeo de motovlog para o YouTube: $ARGUMENTS

- Use a skill `video-para-youtube`, que coordena `transcrever-video`, `cortar-video`, `legendar-video` (plugin edicao-de-video), `metadados-youtube` e `capas-youtube`.
- Se a pasta do canal não tiver `canal.md`, rode antes a skill `conhecer-canal`.
- Corte do início da fala até a despedida, gere as legendas e abra o editor de revisão.
- Enquanto eu reviso, gere o `youtube.txt` (3 títulos para teste A/B, descrição e tags separadas por vírgula) e as 3 capas.
- PARE antes do render final: só queime as legendas depois que eu disser que terminei a revisão.
- No fim, me mostre o caminho do vídeo final, os títulos, as capas e o que pode ser apagado. Nunca apague o bruto.
