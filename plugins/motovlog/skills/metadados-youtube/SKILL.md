---
name: metadados-youtube
description: Escreve 3 opções de título para teste A/B, descrição e tags separadas por vírgula para um vídeo de motovlog no YouTube, no estilo do dono do canal (canal.md), a partir da transcrição, e salva tudo num youtube.txt pronto para copiar e colar. Use quando o usuário pedir "título", "descrição", "tags", "metadados", "SEO do vídeo", "texto pro YouTube" ou "opções de título pra teste A/B" de um vídeo de moto, mesmo sem citar arquivo.
---

# Títulos, descrição e tags (motovlog)

> Feito e testado para canais de **motovlog**. Esta etapa não usa GPU, só precisa da transcrição.

Base: o transcript completo do vídeo (`transcrever-video`) e o `canal.md`, na seção "Estilo de metadados". Sem `canal.md`, rode `conhecer-canal` primeiro. O objetivo é parecer escrito pelo dono do canal, não por uma IA.

## Títulos: sempre 3 (A, B e C)

Os títulos são para o teste A/B do YouTube ("Testar e comparar"), então precisam ser **ângulos diferentes**, não variações da mesma frase. Em motovlog, os ângulos que costumam funcionar:
- **Resultado concreto** com o modelo da moto: "Rodei 1.000 km com a <moto>: o que mudou".
- **Teste/comparação**: "<moto A> ou <moto B> pra cidade: testei as duas". Em geral é o formato com mais views.
- **Pergunta ou curiosidade** sobre o tema: "Vale a pena <x>?".

Regras:
- Use 1ª pessoa e o nome concreto da moto, do lugar ou do equipamento.
- Até ~70 caracteres, para não cortar no celular.
- Nada que o vídeo não entregue.

## Descrição

Escreva 2-4 parágrafos curtos em 1ª pessoa, no tom do canal, com as expressões que a pessoa usa no vídeo:
- diga o que acontece no passeio/teste e o que vale a pena ver;
- cite naturalmente os termos de busca: moto, cidade, estrada, assunto;
- termine com uma pergunta para os comentários e um convite para se inscrever.

Sem emojis, a menos que o `canal.md` diga o contrário. Se o vídeo for longo e tiver trechos distintos, acrescente "Linha do tempo:" (mm:ss — trecho), com os tempos do vídeo **cortado**.

## Tags

Use 15-30 tags, minúsculas, **numa linha só separadas por vírgula** (formato que o YouTube aceita colado). Inclua:
- o assunto e suas variações (com e sem acento);
- o modelo da moto e comparações ("<moto a> vs <moto b>");
- cidade/região;
- "motovlog", "motovlog <cidade>", o nome do canal e os termos fixos do canal.

## Saída: `youtube.txt` na pasta do vídeo

Texto puro, sem markdown:

```
TÍTULOS (teste A/B)

A (capa_A.png): ...
B (capa_B.png): ...
C (capa_C.png): ...


DESCRIÇÃO

...


TAGS

tag1, tag2, tag3, ...
```

Cada título fica casado com uma capa (`capas-youtube`), para o teste combinar título + miniatura. Mostre os 3 títulos na resposta e diga o caminho do arquivo.
