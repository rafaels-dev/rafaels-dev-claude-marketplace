---
name: transcrever-video
description: Transcreve vídeos em português na GPU local (NVIDIA) com faster-whisper large-v3 e timestamps por palavra, adaptando ao sotaque e ao vocabulário do canal (sotaque regional, gírias, nomes próprios, marcas, lugares). Use quando o usuário pedir para "transcrever", "tirar o texto do vídeo", "ver o que eu falei", ou como primeiro passo antes de cortar, legendar ou escrever título/descrição de um vídeo, mesmo que ele só passe o caminho do arquivo.
---

# Transcrever vídeo (GPU local)

> Testado em vídeos de motovlog (câmera de ação com microfone sem fio, ruído de vento e trânsito), num PC com Windows 11 e **NVIDIA RTX 4060 Laptop (8 GB)**: ~1-2 min para 12 min de áudio com `large-v3` em float16. Sem GPU NVIDIA, use `--cpu` (int8) e espere algo como 10x mais tempo.

Requisitos: `ffmpeg`/`ffprobe` no PATH, Python com `faster-whisper` e PyTorch com CUDA (`pip install faster-whisper`). O modelo (~3 GB) baixa sozinho na 1ª vez. Rode Python com `PYTHONIOENCODING=utf-8 python -I`, senão o console do Windows quebra os acentos.

## 1. Inspecionar o arquivo

`ffprobe -v error -show_entries format=duration:stream=index,codec_type,codec_name,width,height,pix_fmt,channels -of compact VIDEO`

Anote duração, resolução e `pix_fmt`, que as outras skills vão precisar. Câmeras de ação (DJI, GoPro) costumam gravar HEVC **10-bit** em 4K60 e embutir trilhas de dados extras. Se houver um `.WAV` separado de microfone sem fio, prefira a trilha do próprio MP4 quando tiver vento, porque o WAV costuma saturar.

## 2. Extrair o áudio (16 kHz mono)

`ffmpeg -i VIDEO -map 0:a:0 -ac 1 -ar 16000 <scratchpad>/audio.wav`

## 3. Transcrever

```
python -I scripts/transcribe.py audio.wav <pasta-do-video>/transcript.json --prompt-file vocab.txt
```

O `--prompt-file` (ou `--prompt`) vira o *initial_prompt* do Whisper. Monte-o com: tipo de vídeo, cidade/região, sotaque, gírias que a pessoa usa e nomes próprios que vão aparecer (marcas, modelos, ruas, pessoas). É isso que faz o Whisper acertar a grafia de nomes e expressões regionais em vez de trocar por palavras parecidas.

Se a pasta de trabalho tiver um perfil do canal (`canal.md`), use a seção de vocabulário dele. Se não tiver, escreva um prompt curto com o que souber do vídeo.

Saída: `{duration, segments:[{start, end, text, words:[{start, end, word, prob}]}]}`, também impressa linha a linha.

## 4. Ler e conferir

Leia o transcript inteiro. Palavras com `prob` baixa e frases sem sentido são suspeitas:
- **Depois da despedida**, o Whisper costuma alucinar frases a partir de ruído (vento, trânsito, música). Isso é tratado no corte.
- **Termos regionais estranhos**: confira num dicionário regional antes de "corrigir" algo que estava certo.
- **Erros recorrentes**: anote no `canal.md` (se existir), para ajustar o prompt da próxima vez.

Não corrija o `transcript.json` à mão: as correções entram nas legendas (`legendar-video`).
