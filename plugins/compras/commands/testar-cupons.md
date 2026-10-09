---
description: Testa um ou mais códigos de cupom no carrinho do Mercado Livre e/ou da Shopee e diz quanto cada um desconta de verdade
argument-hint: "<CUPOM1 CUPOM2 ...> [ml|shopee]"
---

Teste estes cupons no meu carrinho: $ARGUMENTS

- Use as skills `cupons-mercadolivre` e `cupons-shopee` (se eu não disse a loja, teste nas duas onde houver itens no carrinho).
- Um código por vez, digitando, com ritmo humano.
- Para cada código, me diga em uma linha o resultado: aplicou (total antes → depois), inválido, já usado, só em produtos selecionados, compra mínima não atingida etc.
- Calcule o desconto efetivo considerando limite, compra mínima e desconto no Pix.
- Deixe aplicado o melhor cupom e não finalize a compra.
