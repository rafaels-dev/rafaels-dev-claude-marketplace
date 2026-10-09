---
name: video-para-youtube
description: Leva um vídeo bruto de motovlog (DJI, GoPro, Insta360, celular) até ele estar pronto para subir no YouTube — transcrição na GPU local, corte do início da fala até a despedida, legendas estilo filme revisadas num editor sincronizado e queimadas no vídeo, 3 títulos para teste A/B, descrição, tags e 3 capas no estilo do canal. Use sempre que o usuário passar o caminho de um vídeo de moto/motovlog e pedir para "preparar pro YouTube", "editar", "fazer o vídeo", "transcrever e cortar", "legendar e fazer capa", ou qualquer combinação dessas etapas, mesmo que não diga "pipeline".
---

# Vídeo de motovlog para YouTube (orquestrador)

> Feito e testado com vídeos de **motovlog** (câmera de ação no capacete/guidão, microfone sem fio, vento e trânsito), num PC com Windows 11 e **NVIDIA RTX 4060 Laptop (8 GB)**, CUDA via PyTorch e ffmpeg com NVENC. Sem GPU NVIDIA RTX tudo fica bem mais lento (transcrição e decodificação 4K na CPU), e os comandos `*_nvenc`/`-hwaccel cuda` precisam ser trocados por `libx264`/`libx265`.

Coordena as skills para transformar um arquivo bruto em: vídeo final legendado + `youtube.txt` (títulos, descrição, tags) + 3 capas. O usuário revisa as legendas antes do render final, porque queimar legenda é irreversível e leva minutos.

| Etapa | Skill | Plugin | Saída |
|---|---|---|---|
| 0. Perfil do canal (1ª vez) | `conhecer-canal` | `motovlog` | `canal.md`, `estilo-capas/` |
| 1. Transcrever | `transcrever-video` | `edicao-de-video` | `transcript.json` |
| 2. Cortar | `cortar-video` | `edicao-de-video` | `corte.mp4` |
| 3. Legendar (gerar, revisar no editor, queimar) | `legendar-video` | `edicao-de-video` | `legendas.srt`, `final_legendado.mp4` |
| 4. Títulos, descrição, tags | `metadados-youtube` | `motovlog` | `youtube.txt` |
| 5. Capas A/B/C | `capas-youtube` | `motovlog` | `capas/capa_A.png` … |

Requer o plugin `edicao-de-video` instalado. As capas também exigem a chave `OPENROUTER_API_KEY`, na variável de ambiente ou num `.env` na pasta do canal (veja `gerar-capa`).

## Pasta do canal

Tudo gira em torno de uma **pasta do canal** (ex.: `~/videos-youtube/`) com:
- `canal.md`: perfil do canal (moto, câmera, cidade, vocabulário para transcrição, correções frequentes, estilo de títulos/descrição/tags, regras das capas);
- `estilo-capas/`: miniaturas do próprio canal;
- `.env`: `OPENROUTER_API_KEY=...` para as capas (se não estiver na variável de ambiente);
- uma subpasta por vídeo: `AAAA-MM-DD_assunto/`.

Procure a pasta no diretório atual, na memória do usuário, ou pergunte. **Sem `canal.md`, rode `conhecer-canal` primeiro**: é o que faz títulos, legendas e capas parecerem do dono do canal, e não genéricos.

## Fluxo

1. Crie a subpasta do vídeo com um nome provisório e renomeie depois de saber o assunto.
2. `transcrever-video`, com o vocabulário do `canal.md`. Leia o transcript inteiro para entender o assunto.
3. `cortar-video`: START/END pela fala e corte sem reencodar.
4. `legendar-video`: gere o SRT, revise você mesmo (nomes, pontuação, mantendo o sotaque), gere o proxy e **abra o editor de revisão** para o usuário. Enquanto ele revisa, adiante as etapas 5 e 6.
5. `metadados-youtube`: `youtube.txt`.
6. `capas-youtube`: 3 capas, cada uma casada com um título.
7. Quando o usuário disser que terminou a revisão: releia o `.srt`, renderize o final e confira um frame do meio contra o SRT.

Entregue no fim:
- o caminho do vídeo final;
- o `youtube.txt`;
- as 3 capas (mostre as imagens);
- o que pode ser apagado (o `corte.mp4` e os proxies ocupam vários GB).

Nunca apague o arquivo bruto original.
