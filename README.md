# rafaels-dev Claude Marketplace

Plugins e skills para o [Claude Code](https://claude.com/claude-code), feitos por **Rafael Schettino** ([@rafaels-dev](https://github.com/rafaels-dev)).

## Instalação

No Claude Code:

```
/plugin marketplace add rafaels-dev/rafaels-dev-claude-marketplace
/plugin install compras@rafaels-dev-marketplace
/plugin install whatsapp@rafaels-dev-marketplace
/plugin install edicao-de-video@rafaels-dev-marketplace
/plugin install motovlog@rafaels-dev-marketplace
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
| `negociacao-com-vendedor` | Conversa com o vendedor no chat do marketplace (Shopee, perguntas do ML) para pedir preço melhor no Pix, com contraproposta baseada em preço real e sempre com a sua aprovação. |

### 💬 `whatsapp` — WhatsApp Web sem dor

| Skill | O que faz |
|---|---|
| `leitor-canais-whatsapp` | Lê canais de ofertas e conversas do WhatsApp Web de forma confiável (técnicas para o DOM que muda o tempo todo) e extrai cupons das mensagens. |
| `negociacao-whatsapp-lojas` | Encontra lojas da sua cidade, pede cotação com mensagens naturais, acompanha as respostas e negocia preço — sempre com a sua aprovação. |

Os dois plugins funcionam juntos: o `monitor-de-cupons` usa o `whatsapp` para ler canais e negociar com lojas.

### 🎬 `edicao-de-video` — do bruto ao vídeo legendado

Skills genéricas de edição para quem grava e publica vídeo falado em português.

| Skill | O que faz |
|---|---|
| `transcrever-video` | Transcreve na GPU local com faster-whisper `large-v3`, com timestamps por palavra e vocabulário/sotaque do canal no prompt. |
| `cortar-video` | Acha onde a fala começa e onde está a despedida ("tchau", "se inscreve"…), ignora alucinações do Whisper sobre ruído e corta sem reencodar. |
| `legendar-video` | Gera legendas estilo filme (amarelas, borda preta, 2 linhas), abre um **editor de revisão sincronizado com o vídeo** no navegador (edita texto e tempos com o vídeo tocando, salva direto no .srt) e, depois da sua aprovação, queima as legendas em 4K na GPU. |
| `gerar-capa` | Extrai frames nítidos do próprio vídeo e gera capas de alto impacto (título renderizado pela IA, estilo das suas miniaturas) via OpenRouter, com 3 opções para teste A/B. |

### 🏍️ `motovlog` — vídeo de moto pronto pro YouTube

Usa o `edicao-de-video` e acrescenta o que é específico de canal de motovlog.

| Skill | O que faz |
|---|---|
| `conhecer-canal` | Lê o seu canal no YouTube (títulos, descrições, tags, views, miniaturas) e monta o `canal.md` com seu estilo, moto, câmera, cidade e vocabulário. Só para o seu próprio canal. |
| `video-para-youtube` | Orquestra tudo: transcrição → corte → legendas com revisão → títulos/descrição/tags → capas. |
| `metadados-youtube` | 3 títulos com ângulos diferentes para o teste A/B, descrição no seu tom e tags separadas por vírgula, num `youtube.txt` pronto para colar. |
| `capas-youtube` | 3 capas com a sua moto em destaque (grafia exata do modelo, cenário da sua cidade), cada uma a partir de um frame diferente do vídeo. |

> **Testado com vídeos de motovlog num PC com Windows 11 e NVIDIA RTX 4060 Laptop (8 GB).** Tempos de referência para um vídeo 4K60 de 12 min: transcrição em ~1-2 min, proxy de revisão em ~1 min, render final legendado em ~5 min. Sem GPU NVIDIA RTX funciona, mas bem mais devagar (transcrição e decodificação na CPU, encoders `libx264`/`libx265` no lugar de NVENC).

#### Requisitos dos plugins de vídeo

- **GPU NVIDIA RTX** com driver atualizado (recomendado; é onde foi testado).
- **ffmpeg** com NVENC no PATH (`ffmpeg -encoders | grep nvenc`). No Windows: `choco install ffmpeg-full` ou `winget install Gyan.FFmpeg`.
- **Python 3.10+** com: `pip install faster-whisper requests pillow yt-dlp` e PyTorch com CUDA (https://pytorch.org/get-started/locally/).
- **OpenRouter** (só para as capas). A variável de ambiente `OPENROUTER_API_KEY` precisa existir antes de pedir capas:
  1. Crie uma conta em https://openrouter.ai e adicione créditos (Settings → Credits). Cada capa custa alguns centavos de dólar.
  2. Gere uma chave em https://openrouter.ai/settings/keys.
  3. Defina a variável de ambiente do usuário e reinicie o Claude Code:
     - Windows (PowerShell): `[Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "sk-or-...", "User")`
     - macOS/Linux: `export OPENROUTER_API_KEY="sk-or-..."` no `~/.zshrc` ou `~/.bashrc`

  Não cole a chave no chat: as skills só leem a variável de ambiente.

#### Pasta do canal

Os dados do seu canal ficam **só na sua máquina**, numa pasta de trabalho (ex.: `~/videos-youtube/`): `canal.md` (gerado pelo `conhecer-canal`), `estilo-capas/` (suas miniaturas de referência) e uma subpasta por vídeo. Nada disso vai para o plugin nem para o repositório.

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

## Comandos prontos (exemplos de prompt)

Além das skills, cada plugin traz comandos com prompts já escritos. Digite `/` no Claude Code para ver a lista, ou use direto:

| Comando | Exemplo |
|---|---|
| `/compras:cacar-ofertas` | `/compras:cacar-ofertas capacete X tamanho 58, só Mercado Livre, entrega em até 1 semana, quero pelo menos 15% de desconto` |
| `/compras:testar-cupons` | `/compras:testar-cupons CUPOMEXCLUSIVO BOLSOCHEIO ml` |
| `/compras:achar-mais-barato` | `/compras:achar-mais-barato filtro de óleo original código <código>, chegando até sexta` |
| `/compras:negociar-vendedor` | `/compras:negociar-vendedor <link do anúncio> pedir R$ 420 no Pix; se recusar, agradece` |
| `/whatsapp:ler-canais` | `/whatsapp:ler-canais só cupons do Mercado Livre e Shopee` |
| `/whatsapp:cotar-lojas` | `/whatsapp:cotar-lojas peça <código> em <sua cidade>, referência R$ 450 no Pix` |
| `/edicao-de-video:transcrever` | `/edicao-de-video:transcrever "D:\Videos\bruto\DJI_0011.MP4" sotaque do interior, fala sobre trilha e pneu` |
| `/edicao-de-video:cortar` | `/edicao-de-video:cortar "D:\Videos\bruto\DJI_0011.MP4"` |
| `/edicao-de-video:legendar` | `/edicao-de-video:legendar D:\Videos\2026-10-08_meu-video` |
| `/edicao-de-video:gerar-capas` | `/edicao-de-video:gerar-capas D:\Videos\2026-10-08_meu-video títulos no youtube.txt` |
| `/motovlog:conhecer-canal` | `/motovlog:conhecer-canal https://www.youtube.com/@<meu-canal> pasta D:\Videos` |
| `/motovlog:preparar-video` | `/motovlog:preparar-video "D:\Videos\bruto\DJI_0011.MP4" quero revisar as legendas antes` |
| `/motovlog:titulos` | `/motovlog:titulos D:\Videos\2026-10-08_meu-video foco no comparativo de consumo` |
| `/motovlog:capas` | `/motovlog:capas D:\Videos\2026-10-08_meu-video refaz a B, nome da moto saiu errado` |

## Exemplos de uso

```
Quero comprar uma peça original da minha moto (código <código da peça>). Monitora os canais de
cupom e testa tudo no carrinho do Mercado Livre e da Shopee. Só quero entrega em até 1 semana.
```

```
Pergunta o preço dessa peça nas concessionárias da minha cidade pelo WhatsApp e vê se fazem por R$ 450 no Pix.
```

```
Esse é o meu canal: https://www.youtube.com/@<meu-canal>. Aprende o meu estilo e monta o canal.md.
```

```
"D:\Videos\bruto\DJI_0011.MP4" prepara pro YouTube: transcreve, corta no tchau,
legenda (quero revisar antes), 3 títulos, descrição, tags e 3 capas pra teste A/B.
```

```
Refaz a capa B: o nome da moto saiu errado no tanque.
```
