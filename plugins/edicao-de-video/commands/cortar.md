---
description: Corta o vídeo do início da fala até a despedida ("tchau", "se inscreve"), sem reencodar
argument-hint: "<caminho do vídeo ou da pasta com transcript.json>"
---

Corte este vídeo onde eu começo a falar até onde me despeço: $ARGUMENTS

- Se ainda não houver `transcript.json`, transcreva antes com a skill `transcrever-video`.
- Use a skill `cortar-video`: rode o `speech_bounds.py`, leia o transcript inteiro e decida START/END (descarte alucinações do Whisper depois do tchau).
- Pausas longas no meio ficam; só me diga onde estão e quanto duram.
- Corte com `-c copy` para `corte.mp4` e confirme a duração com `ffprobe`.
- Me diga onde a fala começa e termina (mm:ss) e quanto foi cortado. Nunca altere nem apague o bruto.
