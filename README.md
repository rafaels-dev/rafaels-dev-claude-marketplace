# rafaels-dev Claude Marketplace

Plugins e skills para o [Claude Code](https://claude.com/claude-code), feitos por **Rafael Schettino** ([@rafaels-dev](https://github.com/rafaels-dev)).

## Instalação

No Claude Code:

```
/plugin marketplace add rafaels-dev/rafaels-dev-claude-marketplace
/plugin install compras@rafaels-dev-marketplace
/plugin install whatsapp@rafaels-dev-marketplace
```

## Plugins

### 🛒 `compras` — caçador de ofertas

Para quem quer pagar o menor preço possível em compras online no Brasil.

| Skill | O que faz |
|---|---|
| `monitor-de-cupons` | Orquestra um loop (ex.: a cada 5 min) que lê canais de cupons, testa cada cupom no carrinho, procura o mesmo produto mais barato e só te avisa quando o plano de compra melhora. |
| `cupons-mercadolivre` | Testa códigos no carrinho do Mercado Livre, interpreta as respostas ("produtos selecionados", "já usou"…), calcula o desconto efetivo (limite, compra mínima, Pix) e ativa em massa os cupons da página /cupons. |
| `cupons-shopee` | Testa códigos no carrinho da Shopee e restaura o melhor cupom quando a Shopee troca sozinha para um pior. |
| `produto-identico-mais-barato` | Acha o **mesmo** produto (marca, código de peça, compatibilidade, novo) mais barato ou com entrega mais rápida — sem trocar por similar. |

### 💬 `whatsapp` — WhatsApp Web sem dor

| Skill | O que faz |
|---|---|
| `leitor-canais-whatsapp` | Lê canais de ofertas e conversas do WhatsApp Web de forma confiável (técnicas para o DOM que muda o tempo todo) e extrai cupons das mensagens. |
| `negociacao-whatsapp-lojas` | Encontra lojas da sua cidade, pede cotação com mensagens naturais, acompanha as respostas e negocia preço — sempre com a sua aprovação. |

Os dois plugins funcionam juntos: o `monitor-de-cupons` usa o `whatsapp` para ler canais e negociar com lojas.

## Canais de ofertas no WhatsApp

Canais públicos que uso como fonte de cupons. Siga os que fizerem sentido para você:

| Canal | Foco | Link |
|---|---|---|
| **Promoções THAUTEC** 🛒 | Curadoria manual de ofertas e cupons (Mercado Livre, Shopee, Amazon, Magalu) | https://whatsapp.com/channel/0029Val8yoECHDyoi2TgYt1z |
| **Achados Do Mecanicando** | Ofertas para moto e carro: peças, acessórios, ferramentas | https://whatsapp.com/channel/0029VbCSayMD38CQ1v4Km23K |
| **Ofertas Adrenaline** | Hardware e games | https://whatsapp.com/channel/0029Va7AuWY90x33kNMOMV13 |

> Canais de ofertas normalmente usam links de afiliado. Não muda o preço para você.

## Requisitos

- [Claude in Chrome](https://claude.com/chrome) instalado no navegador onde você já está logado no WhatsApp Web, Mercado Livre e/ou Shopee.
- As skills trabalham **no seu navegador e na sua conta**. Nada de login, senha ou cartão passa pelo Claude.

## Princípios de segurança

- **Nunca finaliza compra.** O carrinho fica pronto com o melhor cupom aplicado; quem clica em "Comprar" é você.
- **Ritmo humano.** Ações espaçadas para não parecer robô e não arriscar bloqueio de conta no WhatsApp ou nas lojas.
- **Mensagens só com aprovação.** Nada é enviado em seu nome (WhatsApp, chat de loja) sem você autorizar, e seus dados pessoais não são compartilhados.
- **Sem roubar seu mouse.** Tudo pelo Claude in Chrome, sem controlar o mouse/teclado do sistema.

## Exemplos de uso

```
Quero comprar uma peça original da minha moto (código <código da peça>). Monitora os canais de
cupom e testa tudo no carrinho do Mercado Livre e da Shopee. Só quero entrega em até 1 semana.
```

```
Pergunta o preço dessa peça nas concessionárias da minha cidade pelo WhatsApp e vê se fazem por R$ 450 no Pix.
```
