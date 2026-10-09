---
description: Transcreve um vídeo na GPU local (faster-whisper) com timestamps por palavra e o vocabulário do canal
argument-hint: "<caminho do vídeo> [contexto: sotaque, gírias, nomes próprios]"
---

Transcreva este vídeo: $ARGUMENTS

- Use a skill `transcrever-video` (GPU NVIDIA, `large-v3`).
- Monte o prompt de vocabulário com o contexto que eu passei e, se existir, a seção "Vocabulário para transcrição" do `canal.md` da pasta de trabalho.
- Se eu disser que tem trecho cantado ou fala abafada, use `--no-vad`.
- Salve o `transcript.json` numa subpasta do vídeo e me mostre o texto resumido, apontando palavras suspeitas (baixa confiança) e possíveis alucinações no fim.
- Não altere o arquivo original.
