---
name: cupons-mercadolivre
description: Testa e ativa cupons do Mercado Livre no carrinho do próprio usuário (pelo Claude in Chrome), interpreta as respostas do ML ("produtos selecionados", "já usou", "confira se está correto"), calcula o desconto efetivo com limite/compra mínima/Pix e ativa em massa os cupons da página /cupons. Use sempre que o usuário quiser testar um código de cupom do ML/meli, saber se um cupom vale para o carrinho dele, ativar cupons de uma categoria, ou comparar o preço final no Mercado Livre — mesmo que ele só cole um código solto.
---

# Cupons do Mercado Livre

Tudo acontece no navegador logado do usuário. Para cada teste: **aba nova → teste → fechar a aba**. Ritmo humano entre ações.

## Regras do ML que mudam a conta

- Por pedido vale **1 cupom do Mercado Livre + 1 cupom de loja** (acumulam).
- Muitos cupons são **de uso único**; depois de usado, o ML responde "Você já usou este cupom".
- Cupons "em produtos selecionados" só valem para itens de uma lista (container). Fora dela, o ML aceita o código na conta mas não aplica desconto.
- Cupons "meli+" exigem assinatura Meli+. O cabeçalho do site mostrando "meli+ por apenas R$…" sugere que o usuário **não** assina, mas o próprio carrinho pode indicar "com Cupom Meli+" — teste em vez de supor.
- Compra mínima e **limite** definem o desconto real: 10% com limite R$ 50 sobre R$ 600 = 8,3%.
- Desconto Pix é recalculado **depois** do cupom: o ganho líquido pode ser menor que o valor do cupom. Leia o total final do resumo.
- Cupom de loja por "seguir a loja" é por **conta de vendedor** — a mesma marca pode ter várias contas (ex.: `LOJA` e `LOJA_CIDADE`) e o cupom de uma não vale na outra.

## Testar um código no carrinho

1. `navigate` para `https://www.mercadolivre.com.br/gz/cart/v2`. Se a aba ficar em `edge://newtab`/`about:blank`, navegue de novo (acontece com abas recém-criadas).
2. Garanta que só os itens relevantes estão marcados (o checkbox de cada item no carrinho). Desmarcar/marcar é reversível; **não exclua** itens do usuário sem pedir.
3. Clique em "Inserir código do cupom" (ou "Cupons (n/m em uso)") no resumo — use `find` + `left_click`.
4. O modal fica num **iframe**. Clique no campo, `type` o código, clique em "Inserir".
5. Espere 3–4 s e leia o resultado (screenshot com zoom no modal, ou o `innerText` do iframe com `/Inserir/`):

```js
const d=[...document.querySelectorAll('iframe')].map(f=>{try{return f.contentDocument}catch(e){return null}})
  .find(x=>x&&/Inserir/.test(x.body.innerText));
d.body.innerText.replace(/\n+/g,' | ').slice(150,1500)
```

### Como interpretar

| Resposta | Significado |
|---|---|
| "Você está economizando R$ X com 1 cupom" + cupom listado com ✓ | Aplicado. Leia o total no resumo. |
| "Confira se o cupom está correto" | Código não existe no ML (pode ser de outra loja). |
| "Você já usou este cupom" | Uso único já consumido. |
| "Este cupom já foi adicionado, mas ainda pode ser usado em produtos selecionados" | Ativo na conta, mas não vale para estes itens. |
| Campo limpa sem erro e o desconto não muda | Adicionado à conta, mas não aplicável (selecionados/mínimo) ou pior que o atual. O modal lista os cupons e mostra "Adicione R$ X para alcançar a compra mínima" quando é mínimo. |

Teste um código por vez (digitando), com screenshot/zoom após cada um. Scripts que preenchem o campo via setter de `value` em loop tendem a travar o renderer — evite.

Aplicar um cupom ML novo **substitui** o anterior. Se o novo for pior, reaplique o melhor.

## Ver o escopo de um cupom "em selecionados"

Na página de cupons, depois de ativado, o botão vira "Conferir produtos". Ele leva para `lista.mercadolivre.com.br/_Container_<nome>` — o nome do container costuma revelar a categoria (ex.: `fh-cupom-moveis` = móveis/casa). Se não bate com o item, descarte.

## Ativar cupons em massa (/cupons)

- Geral: `https://www.mercadolivre.com.br/cupons` (abas "Novos", "Acabam hoje").
- Por categoria: `https://www.mercadolivre.com.br/cupons/filter?acc_vertical=true&all=true&page=N` (Acessórios para Veículos; há outras verticais).

```js
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let n=0; const names=[];
for(const b of [...document.querySelectorAll('button')].filter(b=>b.innerText.trim()==='Aplicar')){
  let c=b; for(let k=0;k<6&&c.innerText.length<60;k++) c=c.parentElement;
  names.push(c.innerText.replace(/\n/g,' ').slice(0,100));
  b.scrollIntoView({block:'center',behavior:'smooth'}); await sleep(800+Math.random()*1200);
  b.click(); n++; await sleep(1800+Math.random()*2500);
}
'ativados: '+n+'\n'+names.join('\n')+'\n'+(document.body.innerText.match(/\d+ Cupons/)||[''])[0]
```

Espere a página carregar **antes** de rodar (um `await sleep` longo dentro do mesmo script que fez `navigate` dá "Inspected target navigated"). Novos cupons nem sempre aparecem na página 1; o contador total ("756 Cupons") ajuda a perceber mudanças.

## Ler preço e prazo de um anúncio

- Páginas de produto: `produto.mercadolivre.com.br/MLB-<id>` (anúncio) redireciona para `/up/MLBU…` ou `/p/MLB…` (catálogo). Alguns IDs de busca só abrem como `/p/MLB<id>`.
- Preço: o texto logo após "opiniões" contém `R$ <de> R$ <por> <x>% OFF`. "no Pix" e "com Cupom" aparecem quando aplicáveis.
- Prazo: procure "Chegará grátis entre …" — prazos de 3+ semanas indicam envio sob encomenda; pergunte ao usuário se aceita.
- Entrega Full na busca: card com `use[href="#poly_full"]`.

## Saída para o usuário

Uma linha por cupom testado (código → resultado) e, se algum valer, uma tabela com total antes/depois, validade e o que ele precisa clicar. Deixe o melhor cupom aplicado no carrinho.
