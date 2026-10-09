---
name: cortar-video
description: Corta um vídeo bruto do momento em que a pessoa começa a falar até a despedida ("tchau", "falou", "se inscreve", "até a próxima"), descartando o que vem antes e depois, sem reencodar (corte instantâneo mesmo em arquivos 4K de vários GB). Use quando o usuário pedir para "cortar onde eu começo e paro de falar", "tirar o começo/fim", "cortar no tchau", "aparar o vídeo", ou depois de transcrever um vídeo que vai para o YouTube.
---

# Cortar vídeo pela fala

> Testado em vídeos de motovlog, num PC com Windows 11 e **NVIDIA RTX 4060 Laptop (8 GB)**. O corte em si é `-c copy` e não usa a GPU. A GPU entra na transcrição que alimenta esta skill.

Precisa do `transcript.json` gerado pela `transcrever-video`.

## 1. Encontrar início e fim

```
python -I scripts/speech_bounds.py <pasta>/transcript.json
```

O script imprime o transcript compacto, marca frases de despedida, lista pausas longas e sugere `START`/`END` (1ª palavra − 0,4 s; última palavra da despedida + 1,3 s). Trate isso como sugestão e decida lendo o transcript:

- **Depois do tchau**, segmentos sem sentido são alucinação do Whisper sobre ruído: descarte. Se depois do tchau houver fala real que continua o assunto, pergunte ao usuário.
- **Início**: se o vídeo começa com algo que não é a abertura ("tá gravando?", teste de microfone), comece na abertura de verdade.
- **Pausas longas no meio** (a pessoa ficou em silêncio por causa do que estava acontecendo) normalmente ficam: em vlog fazem parte do vídeo. Só informe ao usuário onde estão e quanto duram, e corte apenas se ele pedir.

## 2. Cortar sem reencodar

```
ffmpeg -ss START -i VIDEO -t DUR -map 0:v:0 -map 0:a:0 -c copy -movflags +faststart <pasta>/corte.mp4
```

- O `-map` explícito descarta as trilhas de dados e de thumbnail que câmeras de ação embutem, porque elas atrapalham players e o render.
- Com `-c copy`, o ffmpeg grava uma *edit list*: o corte começa de fato em START, mesmo que o keyframe esteja antes. Por isso as legendas usam `--start START` e ficam sincronizadas.
- Confira com `ffprobe` que a duração bate com DUR.

Informe ao usuário onde a fala começa e termina (mm:ss), quanto foi cortado do bruto e quais pausas longas ficaram. O arquivo original nunca é alterado.
