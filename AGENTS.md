# AGENTS.md — Diretrizes de Sessão para o Devin

> **Leia este arquivo integralmente antes de executar qualquer tarefa.**
> Este é o contrato de comportamento do agente neste repositório.
> Para o guia completo de arquitetura e metodologia, leia também `devin-repo-spec.md`.

---

## Regra de Ouro

> O Devin opera localmente via Devin CLI. O fluxo correto é:
>
> 1. Ler a spec em `specs/`
> 2. Criar branch no Flosum via `flosum branch create`
> 3. Recuperar metadados afetados via Snapshot Parcial do Flosum
> 4. Codificar em `force-app/`
> 5. Validar via `sf project deploy start --check-only` na Sandbox local
> 6. Abrir Pull Request no GitHub
>
> **O Devin NUNCA usa `sf project deploy start` (sem `--check-only`) em QA, PreProd ou Produção.**
> Quem promove é o **Flosum**, disparado automaticamente pelo merge em `main` via webhook.

---

## 1. Inicialização de Sessão (Execute Sempre ao Iniciar)

Toda nova sessão do Devin começa com estes dois passos, nesta ordem:

### Passo 1 — Instalar ferramentas

```bash
bash scripts/01_setup_env.sh
```

O script instala: Node.js LTS, Salesforce CLI (`@salesforce/cli`), Flosum CLI (`@flosum/cli`),
plugins obrigatórios (`@salesforce/plugin-code-analyzer`, `sfdx-git-delta`) e dependências Python.

### Passo 2 — Autenticar nas orgs

**Devin em modo autônomo (CI/Cognition):** usa JWT via Secrets configurados no painel da Cognition.

```bash
# Autenticação headless (Devin autônomo)
bash scripts/environment/authenticate-orgs.sh
```

**Desenvolvedor local:** usa login web interativo (sem necessidade de certificado JWT).

```bash
# Autenticação web (desenvolvedor local — abre o navegador)
sf org login web --alias sandbox-dev --instance-url https://test.salesforce.com
flosum auth login --url $FLOSUM_ORG_URL
```

> Se o script de autenticação falhar em modo autônomo, pare e reporte o erro exato.
> Nunca tente contornar falhas de autenticação.

---

## 2. Protocolo de Leitura Obrigatória

Antes de escrever qualquer código, leia nesta sequência:

| Ordem | Arquivo | O que aprender |
|---|---|---|
| 1 | `knowledge-base/metadata-ownership.yaml` | O que este time pode tocar |
| 2 | `knowledge-base/org-inventory.md` | IDs, URLs e limites de cada org |
| 3 | `knowledge-base/flosum-pipeline-map.md` | Como funciona a promoção de ambientes |
| 4 | `specs/<ticket>.md` | O que implementar nesta sessão |

---

## 3. Fluxo de Trabalho Padrão

```
┌─────────────────────────────────────────────────────────┐
│                   FLUXO DO DEVIN                        │
│                                                         │
│  1. Ler specs/ e knowledge-base/                        │
│  2. flosum branch create --name "devin/SN-XXXX-slug"    │
│  3. flosum snapshot partial --components "Tipo:Nome"    │
│  4. Desenvolver em force-app/                           │
│  5. python3 scripts/validation/check-metadata-          │
│       ownership.py                                      │
│  6. sf project deploy start --check-only                │
│       --target-org sandbox-dev                          │
│  7. sf apex run test --code-coverage (≥ 85%)            │
│  8. gh pr create --base main                            │
│                                                         │
│  ── STOP ── (aguardar revisão e merge humano)           │
│                                                         │
│  Flosum detecta merge → QA → PreProd → Prod             │
└─────────────────────────────────────────────────────────┘
```

Referência completa dos playbooks:

| Playbook | Objetivo |
|---|---|
| `playbooks/01_development.md` | Desenvolvimento, testes e validação local |
| `playbooks/02-develop-and-validate.md` | Validação contra org de QA via checkOnly |
| `playbooks/03-promote-via-flosum.md` | Promoção via Flosum após merge |

---

## 4. Comandos Flosum CLI (Referência Rápida)

```bash
# Autenticar no Flosum (interativo, uma vez)
flosum auth login --url $FLOSUM_ORG_URL

# Criar branch isolada para a funcionalidade
flosum branch create --name "devin/SN-XXXX-slug"

# Snapshot PARCIAL — recupera apenas os metadados afetados
# NUNCA use snapshot completo. Apenas os componentes da sua spec.
flosum snapshot partial \
  --branch "devin/SN-XXXX-slug" \
  --components "ApexClass:OrderTrigger,ApexClass:OrderTriggerTest"

# Verificar branches existentes
flosum branch list

# Ver status do snapshot
flosum snapshot status --branch "devin/SN-XXXX-slug"
```

> Consulte `knowledge-base/flosum-pipeline-map.md` para entender o pipeline completo.

---

## 5. Regras de Segurança

### 5.1 Deploy direto é proibido

```bash
# PROIBIDO em ambientes compartilhados
sf project deploy start --target-org qa        # ❌
sf project deploy start --target-org preprod   # ❌
sf project deploy start --target-org prod      # ❌

# PERMITIDO apenas em sandbox local de desenvolvimento
sf project deploy start --check-only --target-org sandbox-dev  # ✅ (somente validação)
sf project deploy start --target-org sandbox-dev               # ✅ (sandbox própria)
```

### 5.2 Snapshot completo é proibido

```bash
flosum snapshot full   # ❌ NUNCA. Baixa tudo, inclusive metadados de outros times.
flosum snapshot partial --components "..."  # ✅ Apenas o que está na spec.
```

### 5.3 Arquivos que nunca devem ir para o Git

- `server.key`, `*.pem`, `*.p8`, `*.p12` — chaves privadas
- `.env`, `.envrc` — variáveis de ambiente com credenciais
- Profiles de outros domínios (verificar antes de `git add`)

O `.gitignore` já cobre esses padrões. Se `git status` mostrar um desses arquivos,
**não faça `git add` e reporte ao Tech Lead imediatamente**.

### 5.4 Peça ajuda humana se

- Detectar metadata de outro time no conjunto de mudanças
- A validação `--check-only` falhar com erro não documentado em `knowledge-base/known-issues.md`
- O webhook do Flosum reportar falha após o merge
- Qualquer operação destrutiva for necessária
- Conflito de merge em arquivos XML, Profiles ou Layouts

---

## 6. Variáveis de Ambiente / Secrets

### Para Devin Autônomo (Secrets no painel da Cognition)

| Variável | Descrição |
|---|---|
| `SF_CLIENT_ID_QA` | Consumer Key do Connected App — Org QA |
| `SF_USERNAME_QA` | Username do usuário de integração — Org QA |
| `SF_JWT_KEY_QA` | Chave RSA privada codificada em Base64 — Org QA |
| `SF_CLIENT_ID_PREPROD` | Consumer Key — Org PreProd |
| `SF_USERNAME_PREPROD` | Username — Org PreProd |
| `SF_JWT_KEY_PREPROD` | Chave RSA privada Base64 — Org PreProd |
| `SF_CLIENT_ID_PROD` | Consumer Key — Org Produção |
| `SF_USERNAME_PROD` | Username — Org Produção |
| `SF_JWT_KEY_PROD` | Chave RSA privada Base64 — Org Produção |
| `FLOSUM_ORG_URL` | URL da org onde o Flosum está instalado |
| `FLOSUM_API_TOKEN` | Token de API do Flosum (Connected App) |
| `FLOSUM_PIPELINE_ID` | ID do pipeline de promoção no Flosum |

### Para Desenvolvedor Local

Apenas `FLOSUM_ORG_URL` é necessário (fornecido pelo Tech Lead).
Auth Salesforce é feita via `sf org login web` — sem Secrets manuais.

---

## 7. Estrutura do Repositório

```
.
├── AGENTS.md                      ← Este arquivo (leia primeiro)
├── devin-repo-spec.md             ← Guia completo de arquitetura e metodologia
├── CLAUDE.md                      ← Instruções de domínio e regras invioláveis
├── .devin.yaml                    ← Configuração da máquina do Devin
│
├── specs/                         ← Especificações das tarefas (O QUÊ fazer)
│   └── _TEMPLATE.md               ← Template para novas specs
│
├── knowledge-base/
│   ├── metadata-ownership.yaml    ← Ownership por time (consulte antes de codar)
│   ├── org-inventory.md           ← Orgs, URLs e propósitos
│   ├── flosum-pipeline-map.md     ← Como funciona o pipeline de promoção
│   └── known-issues.md            ← Erros conhecidos e workarounds
│
├── playbooks/
│   ├── 01_development.md          ← SOP de desenvolvimento local
│   ├── 02-develop-and-validate.md ← Validação via checkOnly
│   └── 03-promote-via-flosum.md   ← Promoção pelo Flosum
│
├── .agents/skills/                ← Skills reutilizáveis do Devin
│   ├── flosum-branch/SKILL.md     ← Branch management via Flosum CLI
│   ├── flosum-snapshot/SKILL.md   ← Snapshot parcial de metadados
│   ├── sf-apex/SKILL.md           ← Padrões Apex
│   └── sf-lwc/SKILL.md            ← Padrões LWC
│
├── scripts/
│   ├── 01_setup_env.sh            ← Setup de ferramentas (rode sempre ao iniciar)
│   ├── environment/
│   │   └── authenticate-orgs.sh  ← Auth JWT headless (Devin autônomo)
│   ├── validation/
│   │   ├── check-metadata-ownership.py   ← Validar ownership antes de commitar
│   │   ├── check-destructive-changes.py  ← Detectar mudanças destrutivas
│   │   └── check-shared-components.py    ← Identificar metadados compartilhados
│   └── salesforce/
│       ├── validate-deploy.sh     ← Wrapper para checkOnly
│       └── run-tests.sh           ← Executar suite de testes Apex
│
└── force-app/main/default/        ← Código-fonte Salesforce (SFDX)
```

---

## 8. Convenção de Commits

```
<tipo>(<escopo>): <descrição curta em português>

[corpo opcional — explica o porquê, não o que]

Flosum-Branch: devin/SN-XXXXX-<slug>
Flosum-Promotion: <id-da-promoção-se-aplicável>
Refs: #<número-da-issue>
```

| Tipo | Quando usar |
|---|---|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `refactor` | Reestruturação sem mudança de comportamento |
| `test` | Adição ou correção de testes |
| `chore` | Configuração, scripts, dependências |
| `docs` | Documentação |

Escopo: nome do componente ou domínio (ex: `OrderTrigger`, `CommercePricing`)

---

*Última atualização: 2026-04-26*
