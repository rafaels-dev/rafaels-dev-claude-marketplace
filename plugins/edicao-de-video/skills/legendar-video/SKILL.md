---
name: legendar-video
description: Gera legendas estilo filme (amarelas com borda preta, até 2 linhas) a partir da transcrição, revisa o texto mantendo o sotaque, abre um editor local sincronizado com o vídeo para o usuário corrigir em tempo real e, depois da aprovação, queima as legendas no vídeo final em 4K na GPU. Use quando o usuário pedir para "legendar", "colocar legenda", "revisar as legendas", "abrir o editor de legendas", "queimar/renderizar com legenda", ou quiser um .srt para o YouTube.
---

# Legendar vídeo

> Testado em vídeos de motovlog (4K60 HEVC 10-bit de câmera de ação), num PC com Windows 11 e **NVIDIA RTX 4060 Laptop (8 GB)**: proxy 720p em ~1 min e render final 4K60 HEVC 10-bit em ~5 min para 7 min de vídeo (decodificação `-hwaccel cuda` + `hevc_nvenc`). Na CPU o mesmo leva 15 min ou mais.

Entrada: `transcript.json` (de `transcrever-video`), `corte.mp4` e o START/END usados no corte (de `cortar-video`). Rode o ffmpeg **a partir da pasta do vídeo** e use caminhos relativos no filtro `subtitles=` — o `D:` de um caminho absoluto quebra o filtro.

## 1. Gerar o SRT

```
python -I scripts/make_srt.py transcript.json legendas.srt --start START --end END
```

Até 2 linhas balanceadas (~42 caracteres por linha), no máximo ~5 s por legenda, uma legenda não atravessa frases do Whisper, fragmentos órfãos de 1-2 palavras são juntados. Tempos já deslocados para o vídeo cortado.

## 2. Revisar o texto você mesmo

Antes de mostrar ao usuário, leia todas as legendas e corrija direto no `.srt`:
- pontuação e maiúsculas (o Whisper junta frases sem ponto);
- nomes próprios e termos do canal (seção "Correções frequentes" do `canal.md`, se existir);
- verbos e palavras claramente mal ouvidas, pelo contexto.

**Mantenha a fala do jeito que a pessoa fala**: "pra", "tá", "tava", "vamo pra cima", "cê". Legenda de vlog não é texto em norma culta. "Corrigir" o sotaque descaracteriza o canal. Anote os números das legendas que ficaram duvidosas (áudio ruim, palavra incerta).

## 3. Proxy e editor sincronizado

O usuário revisa vendo o vídeo, não lendo `.srt` puro (texto solto é ruim de revisar). Gere um proxy 720p **sem legenda** decodificando na GPU:

```
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i corte.mp4 -vf "scale_cuda=1280:720:format=nv12" -c:v h264_nvenc -preset p4 -cq 30 -g 30 -c:a aac -b:a 128k -movflags +faststart proxy_720p.mp4
```

(`h264_nvenc` não aceita 10-bit; o `format=nv12` converte. GOP curto deixa o seek do editor preciso.)

Abra o editor em background e passe o endereço ao usuário:

```
python -I scripts/subtitle_editor.py proxy_720p.mp4 legendas.srt --flag 62,67
```

http://localhost:8765 — vídeo com a legenda sobreposta no mesmo tamanho/estilo do render final, lista que acompanha o vídeo, edição de texto (pausa ao digitar), ajuste de tempos (±0,1 s, "início/fim = agora"), dividir/juntar/apagar/nova legenda, desfazer, busca, linha do tempo clicável. Grava no `.srt` a cada alteração (backup `.srt.bak` na 1ª gravação). `--flag` destaca as legendas duvidosas.

**Espere o usuário dizer que terminou.** Enquanto isso, adiante título/descrição/capas.

## 4. Render final (só depois da aprovação)

1. Pare o servidor do editor e releia o `legendas.srt` (mudou). Mostre ao usuário o que ele alterou (`diff` com o `.srt.bak`) e valide: tempos crescentes, sem sobreposição, sem legenda vazia.
2. Estilo (amarelo `&H0000FFFF`, borda preta; tamanho relativo à altura, igual em 720p e 4K):
   ```
   STYLE="FontName=Arial,FontSize=15,Bold=1,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BackColour=&H80000000,BorderStyle=1,Outline=1.6,Shadow=0.6,MarginV=18,Alignment=2"
   ```
3. Teste 5 s para ver estilo e encoder (com `-ss` a legenda aparece deslocada — é esperado, serve só para ver o visual):
   `ffmpeg -hwaccel cuda -ss 28 -t 5 -i corte.mp4 -vf "subtitles=legendas.srt:force_style='$STYLE'" -c:v hevc_nvenc -profile:v main10 -pix_fmt p010le -preset p5 -cq 20 -c:a copy teste.mp4`
4. Render completo em background:
   ```
   ffmpeg -hwaccel cuda -i corte.mp4 -vf "subtitles=legendas.srt:force_style='$STYLE'" -c:v hevc_nvenc -profile:v main10 -pix_fmt p010le -preset p5 -cq 20 -c:a copy -movflags +faststart final_legendado.mp4
   ```
   Fonte 8-bit (celular, GoPro em H.264): troque por `-c:v h264_nvenc -pix_fmt yuv420p -cq 21`.
5. Confira: `ffprobe` (duração, 10-bit, resolução) e extraia um frame do meio, comparando o texto com a legenda daquele tempo no `.srt`.

O `legendas.srt` final também pode ir para o YouTube como legenda opcional (CC).
