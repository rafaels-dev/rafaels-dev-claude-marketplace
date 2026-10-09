---
name: produto-identico-mais-barato
description: Encontra o MESMO produto (mesma marca, código de peça, compatibilidade, novo) mais barato ou com entrega mais rápida em Mercado Livre, Shopee e outras lojas, sem trocar por similar. Use quando o usuário pedir "acha mais barato", "tem outro anúncio igual?", "troca pelos iguais mais baratos", "quero que chegue logo", ou quando um anúncio esgotar e for preciso substituí-lo por um idêntico.
---

# Mesmo produto, mais barato (ou mais rápido)

O erro caro aqui é trocar o produto por um "parecido". O usuário quer o **idêntico**, então a verificação vem antes do preço.

## 1. Definir a identidade do produto

Monte, para cada item, uma ficha com o que o usuário exigiu e o que dá para verificar:

- **Marca obrigatória** (ex.: "tem que ser da marca X, não outra").
- **Código de peça / modelo** (ex.: peças originais de moto têm código do fabricante; procure-o nas "Características do produto", na descrição e na foto da etiqueta).
- **Compatibilidade explícita** (ex.: "tem que citar o modelo da moto no anúncio" — não aceite "universal" se o usuário pediu explícito).
- **Condição**: novo, sem "avaria", sem "mostruário", com nota fiscal.
- **Especificação técnica** quando for consumível (ex.: óleo: viscosidade, norma API/JASO e volume conforme o manual; fluido: norma DOT).
- **Variações** que mudam a peça (cor, transparente/fumê, tamanho, ano).
- **Prazo de entrega aceitável** — pergunte; um preço 15% menor que chega em 3 semanas pode não servir.

Fotos e títulos mentem com frequência ("Longo", "Cristal", fotos de outra cor com o mesmo código). Em caso de dúvida que mude a peça, mostre ao usuário e pergunte.

## 2. Procurar

- **Mercado Livre**: busque pelo código de peça (`lista.mercadolivre.com.br/<codigo>`) e por descrição. Ordene por preço. Abra cada candidato e confira a ficha. IDs de catálogo (`/up/MLBU…`, `/p/MLB…`) agrupam vendedores — o "vendido por" pode mudar sozinho (o carrinho também troca de vendedor).
- **Shopee**: busque por descrição + "original" (código costuma não funcionar). Ordene por preço (`&order=asc&sortBy=price`).
- **Outros sites** (Google Shopping `udm=28`, site do fabricante/concessionária, Amazon, Magalu): só se o usuário aceitar comprar fora das lojas principais.
- **Lojas físicas**: veja `negociacao-whatsapp-lojas`.

Extração rápida de cards na busca do ML:

```js
[...document.querySelectorAll('li.ui-search-layout__item')].map(c=>{
  const a=c.querySelector('a[href*="MLB"]'); const id=(a?.href.match(/MLB-?U?\d+/)||[''])[0];
  const title=c.querySelector('h3, .poly-component__title')?.innerText||'';
  const cur=c.querySelector('.poly-price__current .andes-money-amount')?.innerText.replace(/\n/g,'')||'';
  return cur+' | '+title.slice(0,85)+' => '+id}).slice(0,12).join('\n')
```

## 3. Comparar

Para cada candidato válido: preço final (com cupons aplicáveis e Pix), frete, prazo, vendedor (loja oficial? reputação?), estoque. Monte uma tabela curta. Recomende uma opção, mas deixe claro o trade-off (preço × prazo × confiança).

## 4. Trocar no carrinho

Adicionar ao carrinho e marcar/desmarcar itens é reversível; faça. **Excluir** itens do carrinho do usuário, só se ele pedir. Deixe o substituído desmarcado e avise.

Se um anúncio no carrinho aparecer "ESGOTADO", procure substituto idêntico imediatamente e avise.
