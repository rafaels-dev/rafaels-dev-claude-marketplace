---
name: negociacao-whatsapp-lojas
description: Encontra lojas físicas/concessionárias da cidade do usuário, pede cotação de um produto pelo WhatsApp com mensagens naturais (humanizadas), acompanha as respostas e negocia preço com contraproposta — sempre com aprovação do usuário para cada mensagem. Use quando o usuário pedir "pergunta o preço nas lojas da minha cidade", "manda mensagem pras concessionárias", "negocia com a loja", "vê se fazem por X no Pix", ou quiser comparar o preço online com o de loja física.
---

# Cotação e negociação com lojas pelo WhatsApp

Mandar mensagem é agir em nome do usuário. O usuário autoriza o **objetivo** (ex.: "consulta preço da peça X nessas lojas"); cada desvio relevante (passar dados pessoais, fechar negócio, aceitar condição) volta para ele decidir.

## 1. Achar as lojas

- Busque concessionárias/autopeças/lojas do segmento na cidade (Google Maps, site da marca, Google). Anote nome, bairro e WhatsApp oficial (botão `wa.me` do perfil do Maps ou site).
- Prefira o WhatsApp do **setor de peças** quando a loja divulgar.
- Para lojas que só existem num marketplace, o canal é o chat da plataforma (veja `cupons-shopee`).
- Bases de CNPJ às vezes trazem telefone/e-mail do **contador**, não da loja — não use esses contatos para negociar.

## 2. Primeira mensagem

Curta, natural, com o que a loja precisa para cotar (produto, modelo/ano, código de peça se houver) e a pergunta objetiva (preço à vista/Pix, disponibilidade). Exemplo de tom:

> Boa tarde, tudo bem? Vocês têm a peça original <nome> da <modelo/ano>? Código <código>. Quanto fica no Pix?

Evite cara de robô: sem listas, sem formalidade excessiva, sem travessões, sem "Prezados". Use o nome do vendedor se ele se apresentar.

Para iniciar conversa: `https://web.whatsapp.com/send?phone=<número com DDI>` (veja `leitor-canais-whatsapp` para digitar e confirmar o envio).

## 3. Acompanhar respostas

- Inclua as conversas no loop do `monitor-de-cupons` (checar a prévia da conversa a cada rodada).
- **Atendimento automático** (menus, "informe seu nome completo/CPF para prosseguir"): pare e pergunte ao usuário se quer fornecer o dado.
- Mensagens automáticas de horário/boas-vindas não são resposta real.
- Ao receber preço: avise o usuário com o valor e a comparação com a melhor opção online.

## 4. Negociar

Só com o aval do usuário para a estratégia (ex.: "pergunta se faz por R$ 450 no Pix; se não, agradece"). Táticas que funcionam com educação:

- Perguntar o menor preço à vista/Pix e para retirada no mesmo dia.
- Citar o preço encontrado online (sem inventar valores).
- Mostrar preferência genuína ("se chegar perto disso prefiro comprar aí").

Se recusarem: agradecer e encerrar ("Tranquilo, obrigado pela atenção!"). Nunca confirme compra, reserva ou pagamento pelo usuário.

## 5. Registro

Anote no log: loja, preço cotado, condição (Pix/cartão, retirada), data/hora. Não coloque telefones nem nomes de atendentes em arquivos que serão compartilhados.
