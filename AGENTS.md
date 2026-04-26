# AGENTS.md — Diretrizes para Sessões Autônomas (Devin / Cognition)

> **Leia este arquivo integralmente antes de executar qualquer tarefa.**
> Ele é a fonte da verdade para o comportamento do agente neste repositório.

---

## ⭐ Regra de Ouro da Orquestração

> **O Devin opera localmente via Devin CLI ou Workspace. O fluxo correto é:**
> 1. Ler a spec em `specs/`
> 2. Codificar em `force-app/`
> 3. Validar via `sf project deploy start --check-only` na Sandbox
> 4. Abrir o PR no GitHub
>
> **O DEVIN NUNCA USA COMANDOS DIRETOS DE DEPLOY PARA AMBIENTES COMPARTILHADOS (QA/PROD).**
> Quem faz deploy é o **Flosum**, escutando o merge da branch `main` no Git via webhook nativo.
> O Devin não executa, não monitora e não re-tenta promoções de pipeline — isso é responsabilidade
> do Flosum e do revisor humano após o merge.

---

## 1. Identidade do Projeto

Este é um **projeto Salesforce** gerenciado com **Salesforce DX (SFDX)** e integrado ao pipeline de CI/CD via **Flosum** com sincronização nativa de Git.

- **Paradigma:** Desenvolvimento baseado em pacotes modulares (Unlocked Packages ou 2GP).
- **Ferramenta de Deploy:** Flosum via webhook nativo do GitHub — o merge em `main` dispara o pipeline automaticamente.
- **Ferramenta de Validação:** `@salesforce/cli` (`sf`) — usada **apenas** para `--check-only` em Sandbox.
- **Ferramenta de Orquestração Flosum:** `@flosum/cli` — para operações locais de snapshot e diagnóstico quando necessário.
- **Ambientes conhecidos:** Sandbox QA (`org-qa`), PreProd, Produção.
- **Controle de versão:** Git. Toda entrega deve passar por Pull Request revisado e mergeado em `main`.

---

## 2. Protocolo Obrigatório de Inicialização de Sessão

**Toda vez que uma nova sessão for iniciada neste repositório, você DEVE executar os scripts de setup na ordem abaixo antes de realizar qualquer outra ação.**

Isso garante que a máquina virtual do Devin tenha todas as ferramentas instaladas e as credenciais configuradas, independentemente de qual VM foi alocada.

### Passo 1 — Preparar o ambiente (ferramentas e CLIs)

```bash
bash scripts/01_setup_env.sh
```

Este script irá:
- Verificar e instalar o **Node.js LTS** (via `nodesource`) caso ausente.
- Instalar o **Salesforce CLI** (`@salesforce/cli`) globalmente via npm.
- Instalar os plugins obrigatórios: `flosum-sfdx-plugin`, `@salesforce/plugin-code-analyzer`, `sfdmu`, `sfdx-git-delta`.
- Aplicar configurações globais (telemetria desabilitada, memória Node aumentada).

### Passo 2 — Autenticar nas Orgs Salesforce

```bash
bash scripts/02_auth_orgs.sh
```

Este script irá:
- Validar que os **Secrets obrigatórios** estão definidos no painel da Cognition (`SF_CLIENT_ID`, `SF_USERNAME_QA`, `SF_JWT_KEY_BASE64`).
- Decodificar o certificado JWT a partir de Base64 e realizar a autenticação headless via `sf org login jwt`.
- Validar a conexão exibindo os detalhes da Org autenticada.
- **Apagar automaticamente** o arquivo `server.key` do disco ao final (trap `EXIT`).

> **Se qualquer um dos scripts falhar**, interrompa a tarefa e reporte o erro exato ao Tech Lead antes de prosseguir. Não tente contornar falhas de autenticação.

---

## 3. Fluxo de Trabalho Padrão (após inicialização)

Após a inicialização bem-sucedida, siga os playbooks na ordem:

| Ordem | Arquivo | Objetivo |
|-------|---------|----------|
| 1 | `playbooks/01_development.md` | Criação de Scratch Org, desenvolvimento, testes Apex e análise estática |
| 2 | `playbooks/02_flosum_validation.md` *(a criar)* | Validação do pacote via Flosum CLI contra QA |
| 3 | `playbooks/03_pr_and_merge.md` *(a criar)* | Abertura e revisão de Pull Request |

---

## 4. Restrições e Regras de Segurança

### 4.1 Arquivos proibidos de commitar

Nunca adicione ao Git, sob nenhuma circunstância:
- `server.key` ou qualquer arquivo `*.key`, `*.pem`, `*.p8`, `*.p12`
- `.env`, `.envrc`, ou qualquer arquivo contendo credenciais em texto plano
- Arquivos de Profile padrão do Salesforce que pertençam a outros domínios

O `.gitignore` já cobre esses padrões. Se o `git status` mostrar qualquer um desses arquivos como "untracked" ou "modified", **não os adicione e reporte ao Tech Lead**.

### 4.2 Nunca pular a inicialização

Mesmo que a VM pareça ter as ferramentas instaladas de uma sessão anterior, execute os scripts de setup. O Devin opera em ambientes efêmeros — a presença de um binário não garante versão correta ou configuração de autenticação válida.

### 4.3 Configuração de Proxy (se aplicável)

Se o ambiente exigir proxy corporativo, defina as variáveis antes de rodar os scripts:

```bash
export HTTP_PROXY="http://<host>:<porta>"
export HTTPS_PROXY="http://<host>:<porta>"
export NO_PROXY="localhost,127.0.0.1,.salesforce.com,.force.com"
```

Essas variáveis devem ser configuradas nos **Secrets do Devin** para persistência entre sessões.

---

## 5. Estrutura do Repositório

```
.
├── AGENTS.md                  ← Este arquivo (leia primeiro)
├── .gitignore                 ← Ignora node_modules, .env, *.key, etc.
├── scripts/
│   ├── 01_setup_env.sh        ← Instalação de ferramentas (rodar sempre ao iniciar)
│   └── 02_auth_orgs.sh        ← Autenticação JWT nas Orgs Salesforce
├── docs/                      ← Documentação de arquitetura (adicionar aqui)
├── knowledge-base/
│   └── 01_domain_boundaries.md ← Limites de domínio do time (leia antes de codar)
├── playbooks/
│   └── 01_development.md      ← SOP de desenvolvimento e testes
└── .agents/
    └── skills/                ← Agent Skills reutilizáveis (Flosum, SF, etc.)
```

---

## 6. Variáveis de Ambiente / Secrets Necessários

Configure estas variáveis no **Secrets Manager do Devin** (painel da Cognition). Nunca as escreva em arquivos do repositório.

| Variável | Descrição |
|----------|-----------|
| `SF_CLIENT_ID` | Consumer Key do Connected App registrado na Salesforce |
| `SF_USERNAME_QA` | Username do usuário de integração na Org de QA |
| `SF_JWT_KEY_BASE64` | Chave privada RSA codificada em Base64 (`base64 server.key`) |
| `HTTP_PROXY` | *(Opcional)* Proxy corporativo HTTP |
| `HTTPS_PROXY` | *(Opcional)* Proxy corporativo HTTPS |

---

## 7. Autenticação via Web (fallback interativo)

O fluxo padrão é JWT (headless). Se, por algum motivo, o JWT falhar e for necessária autenticação interativa via navegador, use:

```bash
sf org login web --alias org-qa --instance-url https://test.salesforce.com
```

> Isso abrirá um link de autorização no terminal. Copie o link, abra em um navegador, faça login com as credenciais da Org e autorize o acesso. O CLI capturará o token automaticamente após o redirecionamento.

Este método **não é recomendado para automação** — use apenas em sessões de depuração manual.

---

*Última atualização: 2026-04-26*
