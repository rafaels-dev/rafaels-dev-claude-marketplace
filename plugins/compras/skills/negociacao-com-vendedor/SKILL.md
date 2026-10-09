---
name: negociacao-com-vendedor
description: Conversa com o vendedor de um marketplace (chat da Shopee, perguntas/chat do Mercado Livre, OLX etc.) para pedir desconto, preço no Pix, frete ou condição melhor — com mensagens naturais, contraproposta baseada em preço real encontrado e sempre com aprovação do usuário antes de enviar. Use quando o usuário pedir "negocia com o vendedor", "pergunta se ele faz por X", "chama a loja no chat", "vê se baixa o preço", ou quando o preço de um anúncio estiver acima do melhor preço encontrado e valer tentar uma contraproposta.
---

# Negociação com vendedor de marketplace

Vendedor de marketplace paga comissão e taxas à plataforma, então a margem para desconto costuma ser pequena — e muitos recusam por política. Ainda assim, uma pergunta educada e objetiva custa pouco e às vezes rende frete grátis, um cupom de loja ou um ajuste de preço. O objetivo é tentar sem desgastar e sem expor o usuário.

## Antes de escrever

1. **Saiba o seu número.** Tenha em mãos o melhor preço final real que o usuário já tem (outra loja, com cupom, Pix, frete) — veja `produto-identico-mais-barato`, `cupons-mercadolivre`, `cupons-shopee`. Nunca invente um preço concorrente.
2. **Defina com o usuário**: valor a pedir, valor máximo aceitável e o que fazer se recusarem (agradecer e encerrar? aceitar um meio-termo?). Cada mensagem enviada em nome dele precisa da aprovação dele; uma estratégia aprovada ("pede R$ 420; se não der, agradece") cobre as mensagens dessa estratégia.
3. **Leia o anúncio**: estoque, se o vendedor é da mesma cidade (retirada/entrega rápida), reputação, se já existe cupom de loja ("seguir a loja", "cupom do anúncio").

## Onde conversar

- **Shopee**: botão "Conversar agora" na página do produto → painel de chat (o produto aparece como contexto) → campo "Insira uma mensagem aqui" → Enter. Muitas lojas mandam resposta automática na hora; a resposta real pode levar de minutos a horas. O ícone "Chat" mostra o número de não lidas.
- **Mercado Livre**: antes da compra o canal é "Perguntas ao vendedor" (público, moderado — o ML bloqueia telefone, e-mail, links e negociação explícita fora da plataforma). Pergunte sobre condições permitidas (disponibilidade, prazo, se há cupom de loja) em vez de pedir desconto direto.
- **Lojas físicas pelo WhatsApp**: use a skill `negociacao-whatsapp-lojas` (plugin `whatsapp`).

Nunca leve a negociação para fora da plataforma nem aceite pagamento por fora: perde-se a proteção da compra (e os marketplaces alertam para golpes assim).

## Mensagem

Curta, educada, com um único pedido claro. Mostrar preferência real pelo vendedor ajuda:

> Bom dia! Tenho interesse na <produto> (<código/modelo>). Consegue fazer por R$ <valor> no Pix? Achei por esse valor em outro lugar, mas prefiro comprar de vocês aqui de <cidade>.

Evite: textos longos, pressão ("preciso de resposta agora"), ironia, listas, "Prezados". Não envie dados pessoais do usuário (nome completo, CPF, endereço, telefone) sem ele autorizar.

## Acompanhar e fechar

- Inclua o chat no loop do `monitor-de-cupons` e confira a cada rodada se chegou resposta real (diferencie da resposta automática).
- **Aceitaram o valor (ou menos)**: não responda; avise o usuário imediatamente com o valor e como o vendedor vai aplicar (cupom de loja, preço ajustado no anúncio, link de compra).
- **Contraproposta acima do limite ou recusa**: siga a estratégia combinada. Se for encerrar, agradeça de forma simpática ("Tranquilo, entendo! Obrigado pela atenção e pelo retorno.") — manter a porta aberta é útil para compras futuras.
- **Pediram dados ou pagamento fora da plataforma**: pare e pergunte ao usuário.

A compra em si (clicar em comprar, pagar) é sempre do usuário.

## Registro

Anote no log: plataforma, loja, valor pedido, resposta, horário. Não registre nomes de atendentes nem contatos em arquivos que serão compartilhados.
