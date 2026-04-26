# sf-repo — Scaffolding Salesforce + Devin + Flosum

Este repositório é um **scaffolding** (estrutura base reutilizável) para projetos de desenvolvimento Salesforce que utilizam o **Devin** (Cognition) como agente de IA autônomo.

### O papel de cada ferramenta neste projeto

| Ferramenta | Papel | O que NÃO faz aqui |
|------------|-------|--------------------|
| **Flosum** | Ferramenta **central** de versionamento e promoção de código entre ambientes (QA → PreProd → Produção) | — |
| **GitHub** | Armazena **documentação e contexto** para o Devin — playbooks, knowledge-base, skills e scripts de setup | Não é a fonte de verdade do código Salesforce; não gerencia promoções entre orgs |
| **Devin (Cognition)** | Agente autônomo que executa as tarefas de desenvolvimento | Não toma decisões de promoção sem aprovação humana explícita |
| **Salesforce CLI** | Usado apenas para **validação** (`checkOnly`) e tarefas locais | Não realiza deploys diretos em QA, PreProd ou Produção |

### Por que o GitHub existe neste projeto?

O Devin começa cada sessão do zero — sem memória da sessão anterior. Cada leitura de arquivo ou busca de contexto consome **ACUs** (Autonomous Compute Units). Este repositório foi projetado para **minimizar esse consumo** ao concentrar em um único lugar tudo que o Devin precisa saber para iniciar uma sessão produtiva:

- `AGENTS.md` — protocolo de inicialização obrigatório
- `knowledge-base/` — arquitetura, orgs e domínios do projeto
- `playbooks/` — passo a passo para cada tipo de tarefa
- `.agents/` — skills especializadas que ampliam as capacidades do Devin
- `scripts/` — setup de ambiente e autenticação idempotentes

> **Regra de ouro:** se algo precisa ser lembrado entre sessões, deve estar neste repositório.

---

## Índice

- [Pré-requisitos e Inicialização](#pré-requisitos-e-inicialização)
- [Estrutura de Pastas](#estrutura-de-pastas)
  - [.agents/](#agents)
  - [.claude/](#claude)
  - [.github/](#github)
  - [docs/](#docs)
  - [force-app/](#force-app)
  - [knowledge-base/](#knowledge-base)
  - [manifests/](#manifests)
  - [playbooks/](#playbooks)
  - [prompts/](#prompts)
  - [reports/](#reports)
  - [scripts/](#scripts)
  - [specs/](#specs)
- [Arquivos Raiz](#arquivos-raiz)
- [Skills Disponíveis](#skills-disponíveis)
- [Fluxo de Trabalho](#fluxo-de-trabalho)

---

## Visão Geral do Ambiente

| Item | Detalhe |
|------|---------|
| **Paradigma de deploy** | Flosum CLI (`flosum-sfdx-plugin`) — promoções entre ambientes |
| **Ambientes** | Scratch Org (dev efêmero) → QA (`org-qa`) → PreProd → Produção |
| **Agente autônomo** | Devin / Cognition |
| **Contexto do agente** | Este repositório GitHub |
| **Validação local** | Salesforce CLI (`sf`) — apenas `checkOnly`, nunca deploy direto |

---

## Pré-requisitos e Inicialização

**Toda nova sessão do Devin deve executar os scripts abaixo antes de qualquer outra ação.** As VMs da Cognition são efêmeras — cada sessão começa sem ferramentas instaladas nem credenciais configuradas.

```bash
# 1. Instalar ferramentas e CLIs (idempotente)
bash scripts/01_setup_env.sh

# 2. Autenticar nas orgs Salesforce via JWT (idempotente)
bash scripts/02_auth_orgs.sh
```

> Se qualquer script falhar, interrompa e reporte o erro ao Tech Lead antes de prosseguir. Não tente contornar falhas de autenticação.

Os **Secrets obrigatórios** (`SF_CLIENT_ID`, `SF_USERNAME_QA`, `SF_JWT_KEY_BASE64`) devem estar configurados no painel da Cognition antes de iniciar qualquer sessão.

---

## Estrutura de Pastas

```
sf-repo/
├── .agents/                    # Skills Salesforce especializadas para o Devin
├── .claude/                    # Configurações do Claude Code (uso auxiliar)
├── .github/
│   └── workflows/              # Workflows GitHub Actions (lint, validação)
├── docs/                       # Documentação técnica e relatórios gerados
├── force-app/                  # Código-fonte Salesforce (estrutura SFDX)
├── knowledge-base/             # Arquitetura, orgs, domínios — contexto do Devin
├── manifests/                  # package.xml e destructiveChanges para deploy/retrieve
├── playbooks/                  # Procedimentos passo a passo para o Devin seguir
├── prompts/                    # Prompts reutilizáveis para tarefas recorrentes
├── reports/                    # Relatórios e logs de deploy gerados
├── scripts/                    # Setup de ambiente e automação (rodados a cada sessão)
├── specs/                      # Especificações de features para o Devin implementar
├── AGENTS.md                   # Protocolo obrigatório de inicialização do Devin
└── CLAUDE.md                   # Instruções de comportamento para o agente Claude
```

---

### `.agents/`

Contém as **skills** do Devin — módulos de conhecimento especializado que ampliam as capacidades do agente para tarefas Salesforce específicas, seguindo os padrões de qualidade da equipe. Cada skill é carregada sob demanda pelo Devin, reduzindo o consumo de ACUs ao evitar que o agente "descubra" boas práticas por tentativa e erro.

```
.agents/
│
├── # — Flosum (pipeline CI/CD)
├── flosum-auth/                # Autenticação no Flosum CLI
├── flosum-branch/              # Criação e gestão de branches no Flosum
├── flosum-deploy/              # Deploy de pacotes via Flosum
├── flosum-repo/                # Gestão do repositório Flosum
├── flosum-setup/               # Configuração inicial do Flosum
├── flosum-snapshot/            # Criação de snapshots de metadados
├── flosum-source-pull/         # Pull de source da org para o repo
├── flosum-source-push/         # Push de source do repo para a org
│
├── # — Agentforce & IA
├── sf-ai-agentforce/           # Framework principal de agentes Einstein
├── sf-ai-agentforce-observability/ # Monitoramento e analytics de agentes
├── sf-ai-agentforce-persona/   # Configuração de personas de agentes
├── sf-ai-agentforce-testing/   # Testes de agentes Einstein
├── sf-ai-agentscript/          # Automação com Agent Scripts
│
├── # — Desenvolvimento Core
├── sf-apex/                    # Geração e revisão de código Apex (scoring 150 pts)
├── sf-connected-apps/          # OAuth e Connected Apps
├── sf-data/                    # Operações bulk, data factories, templates SOQL
├── sf-debug/                   # Debugging, análise de logs e performance
├── sf-deploy/                  # Automação de deploy e gestão de metadados
├── sf-docs/                    # Geração de documentação técnica
├── sf-flow/                    # Automação com Flows (templates, subflows, padrões)
├── sf-integration/             # REST/SOAP/CDC, Named Credentials, Platform Events
├── sf-lwc/                     # Lightning Web Components (TS, Jest, SLDS)
├── sf-metadata/                # Objetos, campos, layouts, permission sets
├── sf-permissions/             # Hierarquia de permissões e user access
├── sf-soql/                    # Queries SOQL, otimização, selector classes
├── sf-testing/                 # Testes unitários/integração, mocks, test factories
│
├── # — Data Cloud
├── sf-datacloud/               # Salesforce Data Cloud (skill raiz)
├── sf-datacloud-act/           # Ações e ativações no Data Cloud
├── sf-datacloud-connect/       # Conectores e ingestão de dados
├── sf-datacloud-harmonize/     # Harmonização e mapeamento de dados
├── sf-datacloud-prepare/       # Preparação e transformação de dados
├── sf-datacloud-retrieve/      # Consulta e extração de dados
├── sf-datacloud-segment/       # Segmentação de audiências
│
├── # — Diagramação
├── sf-diagram-mermaid/         # ERD, sequence, diagramas de arquitetura (Mermaid)
├── sf-diagram-nanobananapro/   # Visualização estética de arquitetura
│
└── # — Industry CommonCore (Omnistudio / Vlocity)
    ├── sf-industry-commoncore-callable-apex/        # Callable Apex (Vlocity)
    ├── sf-industry-commoncore-datamapper/           # Data Mapper (Omnistudio)
    ├── sf-industry-commoncore-flexcard/             # FlexCards
    ├── sf-industry-commoncore-integration-procedure/ # Integration Procedures
    ├── sf-industry-commoncore-omniscript/           # OmniScripts
    └── sf-industry-commoncore-omnistudio-analyze/   # Análise de dependências OmniStudio
```

Cada skill segue a estrutura interna padrão:

```
<skill-name>/
├── SKILL.md          # Manifest: nome, descrição, gatilhos, versão, autor
├── README.md         # Visão geral e guia de uso
├── assets/           # Templates, padrões e exemplos de código
├── references/       # Guias e melhores práticas detalhadas
├── hooks/scripts/    # Scripts Python de validação automática
└── scripts/          # Utilitários e scripts de geração
```

---

### `.claude/`

Configurações locais do **Claude Code** para uso auxiliar neste repositório (settings, comandos customizados, permissões de ferramentas). O Claude Code não é o agente principal deste projeto — esse papel pertence ao Devin. Não edite manualmente sem necessidade.

---

### `.github/`

```
.github/
└── workflows/        # Workflows GitHub Actions
```

Os workflows aqui **não substituem o Flosum** como ferramenta de deploy. Seu papel é complementar: validar a qualidade do código nos PRs (análise estática, lint, testes), garantindo que o que chega ao Flosum já passou por uma checagem automatizada.

---

### `docs/`

Documentação técnica gerada ou mantida pela equipe:

| Arquivo | Descrição |
|---------|-----------|
| `ajuste-referencias-skills.md` | Registro de ajustes de referências entre skills |
| `relatorio-ajuste-referencias.md` | Relatório detalhado dos ajustes realizados |

---

### `force-app/`

Código-fonte Salesforce no formato **SFDX** — é aqui que o Devin cria e edita metadados durante o desenvolvimento:

```
force-app/main/default/
├── aura/           # Componentes Aura
├── classes/        # Classes Apex e triggers
├── flows/          # Definições de Flow
├── lwc/            # Lightning Web Components
├── objects/        # Objetos customizados e campos
├── permissionsets/ # Permission Sets
└── triggers/       # Apex Triggers
```

Todo desenvolvimento começa aqui. Após validação, o conteúdo é promovido via Flosum.

---

### `manifests/`

Arquivos XML que controlam quais metadados são incluídos nas operações de deploy e retrieve:

| Arquivo | Descrição |
|---------|-----------|
| `package-deploy.xml` | Manifesto para operações de deploy |
| `package-retrieve.xml` | Manifesto para retrieve de metadados |
| `destructiveChanges.xml` | Manifesto de mudanças destrutivas |

> Sempre execute `scripts/validation/check-metadata-ownership.py` antes de gerar ou modificar um `package.xml`.

---

### `reports/`

Relatórios e logs gerados pelo Devin durante as operações de deploy. Os arquivos são criados via `scripts/reporting/generate-deploy-report.py` e `scripts/reporting/log-failure.py`.

---

### `specs/`

Especificações de features que o Devin lê **antes de iniciar o desenvolvimento**. Use `specs/_TEMPLATE.md` como base ao criar uma nova spec.

---

### `knowledge-base/`

**Contexto arquitetural do projeto para o Devin.** É aqui que o agente encontra as informações que precisaria perguntar ao time — evitando chamadas desnecessárias que consumiriam ACUs:

```
knowledge-base/
├── README.md                      # Guia de navegação desta pasta
├── 01_domain_boundaries.md        # Fronteiras de domínio e mapa de responsabilidades
├── architecture-overview.md       # Visão geral da arquitetura do sistema
├── flosum-pipeline-map.md         # Fluxo e estágios do pipeline Flosum
├── known-issues.md                # Problemas conhecidos e workarounds
├── metadata-ownership.yaml        # Ownership de metadados por time
├── org-inventory.md               # IDs e propósitos das orgs (QA, PreProd, Prod)
├── team-contacts.md               # Contatos da equipe
└── diagrams/                      # Diagramas de arquitetura
```

Quanto mais completa esta pasta, menos o Devin precisa interromper o trabalho para pedir contexto.

---

### `playbooks/`

**Instruções passo a passo para o Devin** executar operações críticas de forma segura e padronizada:

```
playbooks/
├── README.md                         # Guia de navegação desta pasta
├── 00-setup-environment.md           # Checklist de configuração do ambiente
├── 01-retrieve-org-state.md          # Recuperar metadados de orgs
├── 01_development.md                 # Criação de Scratch Org, desenvolvimento, testes e lint
├── 02-develop-and-validate.md        # Fluxo de desenvolvimento e validação
├── 03-promote-via-flosum.md          # Procedimentos de promoção via Flosum
├── 04-handle-conflicts.md            # Estratégias de resolução de conflitos
├── 05-rollback-procedure.md          # Passos para rollback
└── 06-hotfix-protocol.md             # Protocolo de hotfix de emergência
```

Cada playbook elimina a necessidade de o Devin "inferir" o procedimento correto, reduzindo o risco de erros e o consumo de ACUs com retrabalho.

---

### `prompts/`

Prompts reutilizáveis para tarefas recorrentes específicas do projeto. Complementam as skills com instruções contextuais que o Devin pode carregar diretamente, sem precisar reescrever instruções a cada sessão.

---

### `scripts/`

Scripts de automação executados no setup e operação do ambiente:

```
scripts/
├── 01_setup_env.sh             # Instala Node.js LTS, Salesforce CLI e plugins obrigatórios
│                               # (flosum-sfdx-plugin, code-analyzer, sfdmu, sfdx-git-delta)
├── 02_auth_orgs.sh             # Autentica nas orgs Salesforce via JWT
│
├── environment/
│   ├── setup.sh                # Setup geral do ambiente
│   ├── authenticate-orgs.sh    # Autenticação nas orgs
│   └── verify-dependencies.sh  # Verifica ferramentas obrigatórias
│
├── salesforce/
│   ├── validate-deploy.sh      # Validação de deploy (checkOnly)
│   ├── run-tests.sh            # Executa testes Apex
│   ├── retrieve-metadata.sh    # Recupera metadados de uma org
│   └── compare-org-state.py    # Compara estado de metadados entre orgs
│
├── reporting/
│   ├── generate-deploy-report.py  # Gera relatório de deploy
│   └── log-failure.py             # Registra falha de deploy
│
└── validation/
    ├── check-metadata-ownership.py    # Verifica ownership dos metadados
    ├── check-destructive-changes.py   # Valida mudanças destrutivas
    └── check-shared-components.py     # Verifica componentes compartilhados
```

> **Importante:** os scripts são idempotentes — podem ser executados múltiplas vezes com segurança.

---

## Arquivos Raiz

| Arquivo | Descrição |
|---------|-----------|
| `AGENTS.md` | **Leitura obrigatória para o Devin a cada sessão.** Define a identidade do projeto, protocolo de inicialização, fluxo de trabalho padrão e regras de comportamento. É a primeira coisa que o agente deve ler. |
| `CLAUDE.md` | Instruções de comportamento para o agente Claude (escopo, regras invioláveis, convenções de commit, quando pedir ajuda humana). |
| `README.md` | Este arquivo — visão geral e guia de navegação do repositório. |
| `sfdx-project.json` | Configuração do projeto Salesforce DX (diretório-fonte, plugins, namespace). |
| `.env.example` | Template de variáveis de ambiente — copie para `.env` localmente e preencha os secrets. |
| `.devin.yaml` | Configuração específica do agente Devin (Cognition). |

---

## Skills Disponíveis

Resumo rápido das skills por categoria:

| Categoria | Skills |
|-----------|--------|
| **Flosum / CI-CD** | `flosum-auth`, `flosum-branch`, `flosum-deploy`, `flosum-repo`, `flosum-setup`, `flosum-snapshot`, `flosum-source-pull`, `flosum-source-push` |
| **Agentforce / IA** | `sf-ai-agentforce`, `sf-ai-agentforce-observability`, `sf-ai-agentforce-persona`, `sf-ai-agentforce-testing`, `sf-ai-agentscript` |
| **Desenvolvimento Core** | `sf-apex`, `sf-connected-apps`, `sf-data`, `sf-debug`, `sf-deploy`, `sf-docs`, `sf-flow`, `sf-integration`, `sf-lwc`, `sf-metadata`, `sf-permissions`, `sf-soql`, `sf-testing` |
| **Data Cloud** | `sf-datacloud`, `sf-datacloud-act`, `sf-datacloud-connect`, `sf-datacloud-harmonize`, `sf-datacloud-prepare`, `sf-datacloud-retrieve`, `sf-datacloud-segment` |
| **Diagramação** | `sf-diagram-mermaid`, `sf-diagram-nanobananapro` |
| **Industry CommonCore** | `sf-industry-commoncore-callable-apex`, `sf-industry-commoncore-datamapper`, `sf-industry-commoncore-flexcard`, `sf-industry-commoncore-integration-procedure`, `sf-industry-commoncore-omniscript`, `sf-industry-commoncore-omnistudio-analyze` |

---

## Fluxo de Trabalho

```
┌─────────────────────────────────────────────────────────────┐
│  INÍCIO DE SESSÃO (obrigatório a cada nova VM do Devin)      │
│                                                             │
│  1. ler AGENTS.md                                           │
│  2. bash scripts/01_setup_env.sh                            │
│  3. bash scripts/02_auth_orgs.sh                            │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│  DESENVOLVIMENTO                                            │
│                                                             │
│  4. Ler knowledge-base/ (orgs, domínios, arquitetura)       │
│  5. Seguir playbooks/01_development.md                      │
│  6. Criar Scratch Org → Desenvolver → Testes → Lint         │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│  VALIDAÇÃO (sf CLI — checkOnly, nunca deploy direto)        │
│                                                             │
│  7. validate-deploy.sh → checkOnly na org QA               │
│  8. Abrir Pull Request no GitHub (code review humano)       │
└─────────────────────────────────────────────────────────────┘
          │
          ▼ (após aprovação humana)
┌─────────────────────────────────────────────────────────────┐
│  PROMOÇÃO — 100% via Flosum (não via sf CLI)                │
│                                                             │
│  9.  Flosum: QA → PreProd → Produção                        │
│  10. Registrar resultado (log-failure.py se erro)           │
└─────────────────────────────────────────────────────────────┘
```

---

> **Dúvidas?** Consulte o `AGENTS.md` para regras de comportamento do Devin, ou os `playbooks/` para procedimentos operacionais detalhados.
