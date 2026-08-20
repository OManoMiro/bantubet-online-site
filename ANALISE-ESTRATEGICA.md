# Análise estratégica Bantubet

Data: 2026-08-20  
Âmbito: landing page, Blog, publicação de conteúdo, aquisição e operação digital.  
Premissas: `bantubetangola.com` é o domínio canónico; a operação atua em Angola; compliance, licença, promoções e dados de contacto devem ser confirmados pelo responsável legal antes de publicação.

## Diagnóstico atual

A landing é essencialmente HTML estático, com Tailwind via CDN e JavaScript inline. O Blog era referenciado em `rais/index.html`, mas o índice não existia. O publicador FastAPI gera artigos e altera ficheiros diretamente, sem autenticação, sem fila de publicação e com publicação Git dentro do pedido HTTP. Não existem testes, pipeline de qualidade, analytics ou um CMS.

O risco imediato é de confiança e continuidade: links/destinos de conversão usam domínios diferentes, há contactos e links legais que precisam de confirmação, e não havia uma forma funcional de listar artigos. Isto reduz conversão, indexação e capacidade de operar conteúdo com segurança.

## SWOT

| Forças | Fraquezas |
|---|---|
| Marca e proposta localizadas para Angola. | Blog e fluxo editorial sem maturidade operacional. |
| Landing leve, simples de publicar e com CTAs visíveis. | SEO técnico incompleto: metadata, sitemap, robots, schema e medição. |
| Conteúdo em português e canais de suporte/WhatsApp. | Domínio e CTAs inconsistentes; alguns links parecem placeholders ou externos. |
| Publicador já iniciado em FastAPI. | Sem autenticação, testes, rate limit, revisão ou auditoria de publicação. |

| Oportunidades | Ameaças |
|---|---|
| Captar pesquisa orgânica com guias locais e conteúdo útil. | Concorrência forte em apostas e custo crescente de aquisição. |
| Melhorar ativação com jornada clara, tracking e suporte local. | Risco regulatório, reputacional e de publicidade de jogo. |
| Reaproveitar artigos em redes sociais e CRM. | Fraude, abuso de promoções, indisponibilidade e falhas de segurança. |
| Criar segmentos por desporto, perfil e intenção. | Penalização SEO por conteúdo fraco, duplicado ou excesso de palavras-chave. |

## Matriz Ansoff

| Estratégia | Aplicação | Prioridade e condição |
|---|---|---|
| Penetração de mercado | Corrigir velocidade, confiança, domínio canónico, CTAs, suporte, tracking e onboarding para converter melhor a audiência atual. | P0. Medir antes/depois e confirmar links oficiais. |
| Desenvolvimento de produto | Blog editorial real, páginas de desporto, FAQ, centro de ajuda, favoritos e comunicação de promoções com termos claros. | P1. Só publicar conteúdo revisto e conforme. |
| Desenvolvimento de mercado | SEO geográfico para províncias e comunidades angolanas, parcerias e afiliados auditados. | P2. Exige validação legal, marca e atribuição. |
| Diversificação | Conteúdo educativo, ferramentas de gestão de banca e produtos de entretenimento adjacentes. | P3. Discovery separado; não misturar com correções críticas. |

## Passivos e solução priorizada

| Passivo | Causa provável | Contramedida | Dono | Meta |
|---|---|---|---|---|
| Blog indisponível | Índice inexistente e marcador frágil | Índice versionado, posts cumulativos, smoke test e revisão editorial | Produto/Conteúdo | 100% links Blog válidos |
| Publicação insegura | Sem auth, escaping e controlo de duplicados | `BLOG_PUBLISHER_TOKEN` obrigatório, token Git apenas no processo, validação, slug único, revisão e logs | Engenharia | 0 publicações não autorizadas |
| Domínio/CTA inconsistente | Configuração e links históricos divergentes | Canonical único, inventário de URLs, redirects e teste de todos os CTAs | Growth/Engenharia | 100% CTAs para destinos aprovados |
| SEO fraco | Metadata e artefactos ausentes | Title/description por página, canonical, sitemap, robots, schema e Search Console | SEO | Impressões e CTR crescentes; 0 erros críticos |
| Baixa observabilidade | Sem eventos nem funil | Analytics consentido: visita, CTA, registo, depósito, artigo e erro | Growth | Funil completo por origem |
| Risco de confiança/compliance | Termos, licença, promoções e contactos não verificados | Gate legal antes de publicar; idade, jogo responsável e termos visíveis | Legal/Operações | 0 claims sem evidência |
| Regressões de deploy | Sem CI, testes ou Definition of Done | CI com HTML/link checks, Python compile, preview e rollback | Engenharia | Deploy só com checks verdes |
| Conteúdo fraco/duplicado | Geração automática sem editor | Brief, fontes, revisão humana, calendário e atualização de artigos | Conteúdo/SEO | 100% artigos aprovados |
| Acessibilidade e UX | Links placeholder, ícones sem nome e mobile incompleto | Auditoria WCAG, teclado, contraste, alt text e viewport smoke tests | Produto/Frontend | Sem bloqueios críticos |

## Método de execução

### Lean Six Sigma: DMAIC

- **Define:** objetivo: aquisição e ativação confiáveis, com conteúdo sustentável e operação conforme.
- **Measure:** baseline semanal de uptime, LCP, CTR de CTA, registo, depósito, erro 4xx/5xx, artigos publicados, páginas indexadas e reclamações.
- **Analyze:** funil por origem/dispositivo, Pareto de erros e 5 Whys para cada falha repetida.
- **Improve:** aplicar primeiro P0, experimentar uma mudança por vez e usar preview/rollback.
- **Control:** dashboards, alertas, checklist editorial, auditoria mensal e limites de publicação.

### Scrum + Kanban

Usar Scrum para entrega de produto em ciclos semanais e Kanban para suporte/incidentes. Backlog inicial:

1. **Sprint 0, P0:** confirmar domínio, URLs, licença, contactos e termos; publicar Blog; corrigir links locais; adicionar smoke tests; configurar analytics e Search Console.
2. **Sprint 1, P0:** proteger endpoint, validar payload, escapar HTML, impedir sobrescrita, remover token de URLs Git e separar publicação assíncrona.
3. **Sprint 2, P1:** SEO técnico, sitemap/robots/schema, melhorias mobile/acessibilidade e performance; unificar CTAs aprovados.
4. **Sprint 3, P1:** calendário editorial, templates por intenção de pesquisa, páginas de suporte e instrumentação de conteúdo.
5. **Sprint 4, P2:** experiências de conversão, segmentação, afiliados auditados e expansão geográfica baseada em dados.

Quadro Kanban: `Backlog -> Ready -> Em desenvolvimento -> Code review -> QA/Preview -> Aprovado -> Produção -> Medir`. Limites WIP: 2 itens em desenvolvimento e 2 em QA. Incidentes críticos furam a fila, são registados e geram retrospectiva.

## Critérios de aceitação

- Nenhum link interno ou asset crítico devolve 404.
- HTTP e `www` chegam a `https://bantubetangola.com` com redirect permanente.
- O Blog abre, lista artigos e preserva artigos já publicados.
- Um pedido malformado ou não autorizado não cria ficheiros nem faz push.
- `BLOG_PUBLISHER_TOKEN` e o token Git existem apenas como secrets do ambiente de execução.
- Títulos, temas e slugs não permitem injeção nem sobrescrita.
- Deploy tem preview, validação automática e rollback documentado.
- Promoções, licença, termos, contacto e jogo responsável estão confirmados pelo responsável legal.
- Cada alteração relevante tem métrica, responsável, hipótese e janela de avaliação.

## Decisão recomendada

Executar primeiro Penetração de mercado e estabilização operacional. Desenvolvimento de produto vem depois de confiança, tracking e compliance estarem controlados. Não avançar para expansão ou diversificação enquanto os gates P0 permanecerem vermelhos.

## Estado de execução

- **Entregue:** Blog versionado, publicação cumulativa, escaping, slugs únicos, autenticação do endpoint, proteção do token Git, redirect canónico, rewrites Vercel, SEO técnico, sitemap, robots, correções de links/WhatsApp e smoke tests.
- **Pendente:** configuração dos secrets no ambiente, deploy e testes live, confirmação legal de claims/contactos/termos, analytics/Search Console, CI/CD com preview/rollback e publicação assíncrona.
- **Próximo gate:** só avançar para crescimento e diversificação depois de o deploy live passar os critérios P0 e os responsáveis confirmarem compliance.
