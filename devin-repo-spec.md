# devin-repo-spec.md — O Guia do Orquestrador de IA

> Bem-vindo ao time! Este documento é a sua bússola.
> Ele vai mudar a forma como você pensa sobre desenvolvimento.
> Leia com calma — entender isso vai multiplicar a sua produtividade.

---

## O Que É Ser um Orquestrador de IA?

Você provavelmente aprendeu a programar escrevendo código linha por linha. Esse é um jeito válido de trabalhar — mas existe um jeito mais poderoso.

**Um Orquestrador de IA não digita código. Ele descreve problemas.**

Sua função passa a ser:
- Entender profundamente o **problema de negócio**
- Escrever uma **especificação precisa** do que precisa ser feito
- **Delegar a implementação** para o Devin
- **Revisar, validar e aprovar** o resultado

O Devin descobre o *como*. Você define o *o quê* e o *porquê*. Esse é o coração da metodologia **Spec-Driven Development (SDD)**.

---

## Parte 1 — A Nova Arquitetura de Responsabilidades

```
┌─────────────────────────────────────────────────────────────────┐
│                     VISÃO GERAL DO SISTEMA                      │
│                                                                 │
│   Developer / Devin                                             │
│       │                                                         │
│       ▼                                                         │
│   ┌───────────┐   escreve spec   ┌─────────────────────────┐   │
│   │  specs/   │ ──────────────►  │      Devin CLI          │   │
│   │ (O QUÊ)   │                  │  (implementa e valida)  │   │
│   └───────────┘                  └────────────┬────────────┘   │
│                                               │                │
│                                    abre PR    ▼                │
│   ┌────────────────────────┐  ◄─────────  GitHub               │
│   │  GitHub (O Cérebro)    │             (revisão humana)      │
│   │  • Specs e Playbooks   │                  │                │
│   │  • Skills do Devin     │                  │ merge em main  │
│   │  • Histórico de PRs    │                  ▼                │
│   └────────────────────────┘           ┌──────────────┐        │
│                                        │    Flosum    │        │
│   ┌────────────────────────┐           │  (O Músculo) │        │
│   │  Flosum (O Cofre)      │ ◄──────── │  QA → Prod   │        │
│   │  • Versionamento real  │  deploy   └──────────────┘        │
│   │  • Promoção por        │                                   │
│   │    ambientes           │                                   │
│   │  • Branching seguro    │                                   │
│   └────────────────────────┘                                   │
└─────────────────────────────────────────────────────────────────┘
```

### GitHub — O Cérebro (contexto e validação)

O GitHub **não é onde o código de produção vive**. Ele é o sistema nervoso central de conhecimento e colaboração:

- **`specs/`** — onde você escreve o *o quê* precisa ser feito
- **`.agents/skills/`** — biblioteca de habilidades reutilizáveis para o Devin
- **`playbooks/`** — procedimentos operacionais padrão (SOPs)
- **`knowledge-base/`** — limites de domínio, inventário de orgs, mapa de pipelines
- **Pull Requests** — portão de qualidade: toda mudança precisa de revisão humana

> O merge de um PR em `main` é o único gatilho que inicia um deploy. **Ninguém faz deploy manual.**

### Flosum — O Músculo e o Cofre (deploy e versionamento real)

O Flosum é quem **realmente controla o que vai para produção**:

- **Versionamento de metadados Salesforce** com Snapshots parciais (nunca completos)
- **Branches isoladas** para cada funcionalidade (criadas via `flosum` CLI)
- **Pipeline automático**: QA → PreProd → Produção (com aprovação humana na última etapa)
- **Webhook nativo com GitHub**: escuta o merge em `main` e dispara a promoção automaticamente

> Regra absoluta: **Devin e desenvolvedores nunca fazem `sf deploy` direto em QA, PreProd ou Produção.**
> Somente a Sandbox de desenvolvimento local usa deploy direto via `sf` CLI.

---

## Parte 2 — A Jornada do Orquestrador (Spec-Driven Development)

### Passo 1: Entenda o Problema (Antes de Qualquer Código)

Antes de escrever uma spec ou falar com o Devin, responda estas perguntas:

1. **Qual processo de negócio está quebrado ou incompleto?**
2. **Quem é afetado e de que forma?**
3. **Qual seria o comportamento ideal após a mudança?**
4. **Quais objetos/campos/classes do Salesforce estão envolvidos?**
5. **Essa mudança toca metadados de outros times?** (consulte `knowledge-base/metadata-ownership.yaml`)

Se você não consegue responder todas essas perguntas, **não abra uma task para o Devin ainda**. Converse com o Tech Lead ou com o solicitante primeiro.

### Passo 2: Escreva a Especificação

Copie o template em `specs/_TEMPLATE.md` e crie um novo arquivo:

```
specs/SN-12345-nome-curto-da-funcionalidade.md
```

**Uma boa spec tem:**

| Seção | O que colocar |
|---|---|
| **Contexto de Negócio** | Por que isso existe? Qual dor resolve? |
| **Critérios de Aceite Funcionais** | Comportamentos que devem funcionar (testáveis) |
| **Critérios de Aceite Técnicos** | Cobertura ≥ 85%, zero erros lint, validação OK |
| **Matriz de Impacto** | Lista TODOS os metadados afetados |
| **O que NÃO deve ser alterado** | Limites explícitos do escopo |
| **Instruções de Execução** | Passos sequenciais para o Devin seguir |

**O Devin é responsável pelo *como*. Você é responsável pelo *o quê*.**

Exemplo de critério de aceite bem escrito:
```
✅ BOM: Quando um Pedido é criado com Status = "Pendente" e o campo Desconto > 20%,
         o sistema deve acionar aprovação automática e bloquear o avanço para "Confirmado".

❌ RUIM: Criar uma validação de pedidos.
```

### Passo 3: Delegue para o Devin CLI

Com a spec pronta, abra o Devin CLI e aponte para a spec:

```bash
# Inicie uma sessão do Devin apontando para a spec
devin run --spec specs/SN-12345-nome-da-funcionalidade.md
```

O Devin vai:
1. Ler a spec e o knowledge-base
2. Verificar ownership em `metadata-ownership.yaml`
3. Criar a branch no Flosum (`devin/SN-12345-slug`)
4. Implementar em `force-app/`
5. Executar testes e análise estática
6. Validar o deploy (checkOnly) na Sandbox
7. Abrir o Pull Request no GitHub

**Você não precisa escrever uma linha de código.**

### Passo 4: Revise o Pull Request

Quando o Devin abrir o PR, seu trabalho é revisar:

- O código implementa os critérios de aceite da spec?
- Há algum efeito colateral não previsto?
- A cobertura de testes é real (não apenas para "passar no número")?
- Algum metadado fora do escopo foi tocado?

Se algo estiver errado, **comente no PR com instruções claras**. O Devin vai ler e corrigir.

### Passo 5: Approve e Merge → Flosum Faz o Resto

Após aprovação, faça o merge em `main`. O webhook do Flosum assume automaticamente:

```
main ──merge──► Flosum detecta ──► Deploy QA ──► (testes automáticos)
                                ──► Deploy PreProd ──► (aprovação humana)
                                ──► Deploy Produção ──► (aprovação humana)
```

**Você não executa nenhum comando de deploy.** O Flosum gerencia tudo.

---

## Parte 3 — Devin CLI vs. Devin Web Platform

Saber quando usar cada ferramenta economiza muito tempo.

### Use o Devin CLI quando:

| Situação | Por quê |
|---|---|
| Implementar uma spec nova | Devin precisa de acesso ao filesystem e às CLIs (`sf`, `flosum`) |
| Executar validação checkOnly na Sandbox | Requer ambiente com autenticação ativa |
| Criar branch no Flosum e fazer Snapshot parcial | Comandos `flosum branch create`, `flosum snapshot` |
| Corrigir um bug específico em um arquivo | Tarefa atômica, sem necessidade de análise longa |
| Executar scripts de validação | `check-metadata-ownership.py`, `validate-deploy.sh` |
| Resolver um conflito simples de merge | Acesso direto aos arquivos |

```bash
# Exemplo: tarefa atômica via CLI
devin run "Corrija o trigger OrderTrigger.trigger para respeitar a regra de validação da spec specs/SN-99001-order-limit.md"
```

### Use a Devin Web Platform quando:

| Situação | Por quê |
|---|---|
| Discutir arquitetura antes de escrever a spec | Precisa de contexto longo e iterativo ("Ask Devin") |
| Analisar um log de erro extenso (stack trace de prod) | Web Platform suporta conversas longas e análise de documentos |
| Code review profundo de um PR complexo | Discussão iterativa com o Devin sobre decisões técnicas |
| Planejamento inicial de uma iniciativa grande | Exploração de abordagens antes de criar specs individuais |
| Perguntas de "como funciona X neste repositório?" | Consulta de conhecimento sobre o codebase |

> **Dica:** Se você vai pedir ao Devin para *executar* algo (criar arquivo, rodar comando, abrir PR), use o **CLI**. Se você vai *conversar* sobre algo (entender, planejar, analisar), use a **Web Platform**.

---

## Parte 4 — Autenticação para Desenvolvedores Locais

Para simplificar a vida de cada desenvolvedor, usamos **login web interativo** no ambiente local. Você não precisa gerenciar certificados JWT.

### Setup inicial (uma vez por máquina)

```bash
# 1. Instale as ferramentas
bash scripts/01_setup_env.sh

# 2. Autentique-se nas orgs via navegador
sf org login web --alias sandbox-dev --instance-url https://test.salesforce.com
```

Isso abrirá seu navegador. Faça login com suas credenciais da Salesforce. O CLI captura o token automaticamente.

### Autenticação no Flosum CLI

```bash
# Configure sua conexão com o Flosum (uma vez)
flosum auth login --url $FLOSUM_ORG_URL
```

> O `FLOSUM_ORG_URL` é fornecido pelo Tech Lead. Não está no repositório por segurança.

### Diferença: Dev Local vs. Devin Autônomo

| | Dev Local (você) | Devin Autônomo (CI) |
|---|---|---|
| **Auth Salesforce** | Web login interativo | JWT (headless) via Secrets do Cognition |
| **Auth Flosum** | `flosum auth login` interativo | Token via `FLOSUM_API_TOKEN` |
| **Quando autenticar** | Uma vez, sessão dura horas | A cada sessão nova do Devin |

---

## Parte 5 — Snapshotting Parcial (Nunca Completo)

Uma das regras mais importantes: **nunca faça um Snapshot completo da org**.

Por quê? Um Snapshot completo baixa TODOS os metadados — incluindo os de outros times, configurações sensíveis e componentes obsoletos. Isso cria conflitos, aumenta o tempo de deploy e borra as fronteiras de ownership.

**O fluxo correto é Snapshot Parcial:**

```bash
# Recupere APENAS os metadados afetados pelo seu ticket
flosum snapshot partial \
  --branch "devin/SN-12345-slug" \
  --components "ApexClass:OrderTrigger,ApexClass:OrderTriggerTest,CustomObject:Order__c"
```

Antes de rodar, confirme quais componentes estão no escopo consultando:
1. A sua spec (`specs/SN-12345-*.md`) — seção "Matriz de Impacto"
2. O arquivo `knowledge-base/metadata-ownership.yaml` — confirma que são seus

---

## Parte 6 — Estrutura do Repositório (Referência Rápida)

```
.
├── devin-repo-spec.md          ← Este documento (leia primeiro)
├── AGENTS.md                   ← Instruções de sessão para o Devin (leia segundo)
├── CLAUDE.md                   ← Instruções adicionais para Claude/Devin
├── .devin.yaml                 ← Configuração da máquina do Devin
│
├── specs/                      ← Suas especificações (O QUÊ fazer)
│   └── _TEMPLATE.md            ← Template para novas specs
│
├── knowledge-base/             ← Fonte da verdade do domínio
│   ├── metadata-ownership.yaml ← O que cada time pode tocar
│   ├── org-inventory.md        ← IDs e URLs das orgs
│   └── flosum-pipeline-map.md  ← Como funciona a promoção
│
├── playbooks/                  ← Procedimentos passo a passo (SOPs)
│   ├── 01_development.md       ← Fluxo principal de desenvolvimento
│   └── 03-promote-via-flosum.md← Como funciona a promoção no Flosum
│
├── .agents/skills/             ← Biblioteca de habilidades do Devin
│   ├── flosum-branch/          ← Criar e gerenciar branches no Flosum
│   ├── flosum-snapshot/        ← Snapshots parciais de metadados
│   ├── sf-apex/                ← Padrões de desenvolvimento Apex
│   └── sf-lwc/                 ← Padrões de desenvolvimento LWC
│
├── scripts/
│   ├── 01_setup_env.sh         ← Instala ferramentas (rode primeiro)
│   ├── validation/             ← Scripts de validação de ownership/qualidade
│   └── salesforce/             ← Scripts de retrieve e validação
│
└── force-app/                  ← Código-fonte Salesforce (SFDX)
    └── main/default/           ← Classes Apex, LWC, Flows, etc.
```

---

## Checklist do Orquestrador

Antes de delegar qualquer tarefa ao Devin, confirme:

- [ ] Entendi o problema de negócio completamente
- [ ] Consultei `knowledge-base/metadata-ownership.yaml` e os metadados são do meu time
- [ ] Escrevi uma spec com critérios de aceite testáveis em `specs/`
- [ ] A spec inclui uma Matriz de Impacto com TODOS os componentes afetados
- [ ] Não há metadados de outros times no escopo (ou já notifiquei os co-owners)

Após o Devin completar a tarefa:

- [ ] Revisei o código no PR e ele implementa os critérios da spec
- [ ] Confirmei que nenhum arquivo fora do escopo foi modificado
- [ ] Aprovei o PR consciente do que está indo para produção

---

*"O melhor código é o código que você não precisou escrever porque descreveu o problema tão bem que a IA entendeu."*

*Última atualização: 2026-04-26*
