---
description: Liga o caçador de ofertas para uma lista de compras — monitora canais de cupons, testa no carrinho e avisa quando o preço melhora
argument-hint: "<o que quer comprar, critérios e prazo>"
---

Quero comprar o seguinte, pagando o menor preço possível:

$ARGUMENTS

Use a skill `monitor-de-cupons` para montar o plano e deixar um loop rodando:

1. Confirme comigo só o que faltar: critérios de "mesmo produto" (marca, código, compatibilidade, novo), lojas aceitas, cupons a ignorar, prazo máximo de entrega e meta de desconto.
2. Coloque os itens no carrinho (Mercado Livre e/ou Shopee) e anote o preço atual num arquivo de log.
3. Agende um loop a cada 5 minutos que leia os canais de ofertas do WhatsApp que eu sigo, teste todo cupom novo no carrinho, confira a página de cupons das lojas a cada ~30 min e procure o mesmo produto mais barato.
4. Só me avise quando o plano melhorar ou quando eu precisar decidir algo.

Ritmo humano, só pelo Claude in Chrome, e nunca finalize a compra — deixe o carrinho pronto para eu fechar.
