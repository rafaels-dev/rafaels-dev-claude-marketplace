---
name: cupons-shopee
description: Testa cupons da Shopee no carrinho do próprio usuário (Claude in Chrome), escolhe o melhor da carteira, e restaura o melhor quando a Shopee troca sozinha para um cupom pior. Use quando o usuário quiser testar códigos de cupom da Shopee, comparar o preço final de um item da Shopee com outra loja, ou quando um canal de promoções postar códigos soltos/teasers que possam ser da Shopee.
---

# Cupons da Shopee

Mesmo princípio das outras lojas: navegador logado do usuário, ritmo humano, nunca finalizar a compra.

## Preparar o carrinho

1. Abra o produto e clique em "Adicionar ao carrinho". A página é pesada: depois de `navigate`, espere ~5 s ou confirme pelo `document.title` antes de procurar o botão. Confirme o toast "Adicionado ao carrinho" (um clique cedo demais não adiciona nada).
2. Vá para `https://shopee.com.br/cart`, marque o item (checkbox "Selecionar Tudo" no rodapé ou o do item).
3. O rodapé mostra "Cupom de Desconto", o desconto aplicado e o **Total**. A Shopee já aplica automaticamente o melhor cupom da carteira na maioria das vezes.

## Testar um código

1. Rodapé → "Trocar cupom" (ou "Selecione ou insira o código").
2. No modal "Selecione Cupons De Desconto": campo "Adicionar Cupom" → `type` o código → "APLICAR".
3. Resultados possíveis:
   - Erro vermelho: "Desculpe, este cupom foi totalmente resgatado", código inválido, etc.
   - Cupom válido: ele entra na carteira e a Shopee **seleciona o novo automaticamente, mesmo que seja pior**.
4. Compare: o modal mostra "N cupons selecionados. Promoção de frete aplicada e R$ X de desconto"; o total aparece no rodapé.
5. Se o novo for pior: **CANCELAR não basta** (a troca pode já ter sido aplicada). Abra "Trocar cupom" de novo, marque o rádio do melhor cupom (`find("cupom '<descrição>' (radio)")`) e clique em "APLICAR". Confirme o total no rodapé.

Há duas seções independentes: **Frete Grátis** (selecione 1) e **Desconto e Moeda Cashback** (selecione 1). Cupons "Limitado" mostram % utilizado e "Termina em: Xh".

## Ler o anúncio

- Preço "no Pix com cupom" vs "sem cupom em outros métodos de pagamento".
- "Enviado de <cidade>" e frete — vendedor na mesma cidade do usuário costuma entregar rápido.
- Estoque ("1 quantidades disponíveis"), número de vendas e avaliações do anúncio e da loja.
- A busca por código de peça na Shopee costuma falhar; busque por descrição + "original" e confira código/foto da etiqueta no anúncio.

## Chat com o vendedor

Botão "Conversar agora" → painel de chat → campo "Insira uma mensagem aqui" → botão enviar. Muitas lojas têm resposta automática; não confunda com resposta real. Só envie mensagens aprovadas pelo usuário (veja `negociacao-whatsapp-lojas` para o tom).
