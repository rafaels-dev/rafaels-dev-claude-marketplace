---
name: capas-youtube
description: Cria 3 capas de motovlog para teste A/B no YouTube — a moto do canal em destaque, frames reais do vídeo, título enorme em pinceladas grunge, no estilo das miniaturas do próprio canal — usando a skill gerar-capa (OpenRouter). Use quando o usuário pedir "capa", "thumbnail", "miniatura", "3 capas pra teste A/B", "refaz a capa" de um vídeo de moto/motovlog, ou reclamar de uma capa.
---

# Capas de motovlog (A/B/C)

> Feito e testado com vídeos de **motovlog** num PC com Windows 11 e NVIDIA RTX 4060 Laptop (8 GB). A geração em si roda na nuvem, via OpenRouter.

Esta skill aplica as regras de motovlog sobre a skill genérica **`gerar-capa`** (plugin `edicao-de-video`). Siga o passo a passo dela, que tem os scripts, a escolha do modelo e a pré-condição da variável `OPENROUTER_API_KEY`. Acrescente o que está abaixo.

## Entradas

- `canal.md`, seção "Capas": linha de canal para o `prompts.md`, modelo exato da moto e regras do dono. Sem `canal.md`, rode `conhecer-canal`.
- `estilo-capas/` na pasta do canal: as miniaturas do canal que servem de referência.
- `youtube.txt`: os 3 títulos (A, B e C). Cada capa reforça o seu título com outras palavras, em vez de repetir o título inteiro.
- Frames do vídeo pelo `extract_frames.py` do `gerar-capa`. Use palavras-chave do assunto (ex.: `--keywords "posto,chuva,estrada"`) e escolha **um frame diferente para cada capa**.

## Regras de motovlog

- **A moto é o objeto principal**: grande, nítida, em 3/4 de frente ou no POV do guidão, fiel ao frame (modelo, cor, carenagem, para-brisa, guidão).
- **Grafia exata do modelo** no adesivo e na carenagem: escreva no prompt `adesivo escrito exatamente "<MODELO>"`, ou peça para deixar a carenagem sem texto. A IA tende a inventar letras.
- **Cenário da cidade do canal**: ruas, serras e estradas reais da região. Peça explicitamente "sem cartões-postais de outras cidades": a IA adora colocar pontes e monumentos famosos que não têm nada a ver com o canal.
- **Piloto de capacete** quando houver pessoa, nunca um rosto inventado como se fosse o dono do canal.
- **Variedade entre A, B e C**. Exemplos de conceito:
  - moto + objetos do tema (cronômetro, placa, mapa com rota);
  - antes × depois com divisória de pincel;
  - POV do guidão (frame real) com um elemento em destaque.

Exemplo de seção do `capas/prompts.md`:

```
canal: <nome do canal>, motovlog em <cidade (UF)>

## A
texto: RODEI 1.000 KM | VALEU A PENA?
ref: frames/f_312.jpg
Título no topo: "RODEI 1.000 KM" em branco sobre pincelada preta, "VALEU A PENA?" em amarelo gigante sobre pincelada
vermelha. À esquerda, a <moto> (igual ao frame, adesivo escrito exatamente "<MODELO>") em 3/4 de frente numa estrada
de serra da região, céu dramático. Seta amarela desenhada à mão apontando do texto para a moto.
```

Confira as 3 capas antes de mostrar, como o `gerar-capa` manda. Aqui o nome da moto errado ou o cenário de outra cidade são motivo para refazer.
