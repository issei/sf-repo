# sf-repo — Repositório Salesforce DX

Projeto Salesforce gerenciado com **Salesforce DX (SFDX)** e pipeline de CI/CD via **Flosum**. O desenvolvimento segue o paradigma de pacotes modulares (Unlocked Packages / 2GP), com controle de versão via Git e entregas obrigatoriamente revisadas por Pull Request.

---

## Índice

- [Visão Geral](#visão-geral)
- [Pré-requisitos e Inicialização](#pré-requisitos-e-inicialização)
- [Estrutura de Pastas](#estrutura-de-pastas)
  - [.agents/](#agents)
  - [.claude/](#claude)
  - [.github/](#github)
  - [data-seeding/](#data-seeding)
  - [docs/](#docs)
  - [knowledge-base/](#knowledge-base)
  - [playbooks/](#playbooks)
  - [prompts/](#prompts)
  - [scripts/](#scripts)
- [Arquivos Raiz](#arquivos-raiz)
- [Skills Disponíveis](#skills-disponíveis)
- [Fluxo de Trabalho](#fluxo-de-trabalho)

---

## Visão Geral

| Item | Descrição |
|------|-----------|
| **Paradigma** | Desenvolvimento baseado em pacotes modulares (Unlocked Packages / 2GP) |
| **Deploy** | Flosum CLI (`flosum-sfdx-plugin`) orquestrando promoções entre ambientes |
| **Ambientes** | Scratch Org (dev efêmero), QA (`org-qa`), Produção |
| **Controle de versão** | Git — toda entrega via Pull Request revisado |
| **Agentes de IA** | Claude Code + Devin/Cognition, com skills especializadas |

---

## Pré-requisitos e Inicialização

**Toda nova sessão de agente autônomo (Devin / Cognition) deve executar os scripts abaixo antes de qualquer outra ação:**

```bash
# 1. Instalar ferramentas e CLIs
bash scripts/01_setup_env.sh

# 2. Autenticar nas orgs Salesforce via JWT
bash scripts/02_auth_orgs.sh
```

> Se qualquer script falhar, interrompa e reporte o erro ao Tech Lead antes de prosseguir.

Os **Secrets obrigatórios** (`SF_CLIENT_ID`, `SF_USERNAME_QA`, `SF_JWT_KEY_BASE64`) devem estar configurados no painel da Cognition.

---

## Estrutura de Pastas

```
sf-repo/
├── .agents/
│   └── skills/                 # Skills especializadas para agentes de IA
├── .claude/                    # Configurações do Claude Code
├── .github/
│   └── workflows/              # Pipelines de CI/CD (GitHub Actions)
├── data-seeding/               # Configurações de seed de dados
├── docs/                       # Documentação técnica e relatórios
├── knowledge-base/             # Arquitetura e documentação de domínio
├── playbooks/                  # Procedimentos operacionais padrão
├── prompts/                    # Prompts reutilizáveis para tarefas específicas
├── scripts/                    # Scripts de automação e setup
└── AGENTS.md                   # Diretrizes para sessões autônomas
```

---

### `.agents/`

Contém as **skills** que ensinam os agentes de IA (Claude Code, Devin) a executar tarefas Salesforce com qualidade e padrões de projeto da equipe.

```
.agents/skills/
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

Configurações locais do **Claude Code** para este repositório (settings, comandos customizados, permissões de ferramentas). Não deve ser editado manualmente sem necessidade.

---

### `.github/`

```
.github/
└── workflows/        # Pipelines GitHub Actions (CI/CD)
```

Contém os workflows de integração contínua que validam PRs, executam análise estática, e podem acionar validações via Flosum automaticamente.

---

### `data-seeding/`

Configurações e scripts para popular orgs com dados de teste padronizados. Garante consistência entre ambientes ao criar registros necessários para desenvolvimento e QA.

---

### `docs/`

Documentação técnica gerada ou mantida pela equipe:

| Arquivo | Descrição |
|---------|-----------|
| `ajuste-referencias-skills.md` | Registro de ajustes de referências entre skills |
| `relatorio-ajuste-referencias.md` | Relatório detalhado dos ajustes realizados |

---

### `knowledge-base/`

Base de conhecimento arquitetural do projeto:

```
knowledge-base/
└── 01_domain_boundaries.md     # Fronteiras de domínio e mapa de responsabilidades
```

Contém diagramas Mermaid de arquitetura, decisões técnicas (ADRs), modelo de dados e documentação de domínios de negócio. É a **fonte de verdade arquitetural** do projeto.

---

### `playbooks/`

Procedimentos operacionais padrão (SOPs) que guiam o desenvolvimento do dia a dia:

```
playbooks/
└── 01_development.md           # Criação de Scratch Org, desenvolvimento,
                                # testes Apex e análise estática
```

Os playbooks definem o passo a passo para operações críticas como setup de ambiente, desenvolvimento de features, deploy, rollback, hotfix e resolução de conflitos. Devem ser seguidos rigorosamente por agentes e desenvolvedores.

---

### `prompts/`

Prompts reutilizáveis para tarefas recorrentes específicas do projeto. Complementam as skills com instruções contextuais para o Claude ou outros agentes.

---

### `scripts/`

Scripts de automação executados no setup e operação do ambiente:

```
scripts/
├── 01_setup_env.sh     # Instala Node.js LTS, Salesforce CLI e plugins obrigatórios
│                       # (flosum-sfdx-plugin, code-analyzer, sfdmu, sfdx-git-delta)
│                       # Aplica configurações globais (telemetria off, memória Node)
│
└── 02_auth_orgs.sh     # Valida secrets obrigatórios no painel da Cognition
                        # Decodifica certificado JWT (Base64) e autentica nas orgs
                        # Valida conexão e apaga server.key do disco ao final
```

> **Importante:** os scripts são idempotentes — podem ser executados múltiplas vezes com segurança.

---

## Arquivos Raiz

| Arquivo | Descrição |
|---------|-----------|
| `AGENTS.md` | **Leitura obrigatória para agentes autônomos.** Define identidade do projeto, protocolo de inicialização de sessão, fluxo de trabalho padrão e regras de comportamento para Devin / Cognition. |
| `README.md` | Este arquivo — visão geral e guia de navegação do repositório. |

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
1. Nova sessão
   └── bash scripts/01_setup_env.sh
   └── bash scripts/02_auth_orgs.sh

2. Desenvolvimento
   └── Consultar playbooks/01_development.md
   └── Criar Scratch Org → Desenvolver → Testar Apex → Análise estática

3. Validação e Deploy
   └── Flosum CLI → Validação QA → Pull Request → Code Review → Merge

4. Dúvidas arquiteturais
   └── Consultar knowledge-base/01_domain_boundaries.md
```

---

> **Dúvidas?** Consulte o `AGENTS.md` para regras de comportamento de agentes, ou os `playbooks/` para procedimentos operacionais detalhados.
