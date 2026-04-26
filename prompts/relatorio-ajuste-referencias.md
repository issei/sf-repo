# Relatório: Ajuste de Referências de Skills

**Data:** 2026-04-26  
**Escopo:** `playbooks/01_development.md`, `knowledge-base/01_domain_boundaries.md`, `scripts/*.sh`

---

## 1. Tabela de Mapeamento Aplicado

| Referência antiga | Skill canônica local | Arquivo(s) alterado(s) | Observação |
|---|---|---|---|
| `@skills:create-scratch-org` | `@sf-deploy` | `playbooks/01_development.md` | `sf-deploy` cobre gerenciamento de Scratch Org (criação, push, validação). |
| `@skills:create-apex-class` | `@sf-apex` | `playbooks/01_development.md` | Mapeamento direto — `sf-apex` é a skill canônica para classes e triggers. |
| `@skills:create-lwc` | `@sf-lwc` | `playbooks/01_development.md` | Mapeamento direto — `sf-lwc` é a skill canônica para componentes LWC. |
| `@skills:run-apex-tests` | `@sf-testing` | `playbooks/01_development.md` | `sf-testing` é a skill canônica para execução de testes e análise de cobertura. |
| `@skills:run-sfdx-scanner` | `@sf-deploy` *(parcial — ver Gaps)* | `playbooks/01_development.md` | Não existe skill dedicada para análise estática. `sf-deploy` menciona Code Analyzer v5 no pipeline de CI/CD. Marcado com comentário `GAP`. Também corrigido o comando CLI obsoleto: `sf scanner run` → `sf code-analyzer run`. |
| `Jaganpro/sf-skills` (repositório externo) | `.agents/skills/` (local) | `playbooks/01_development.md` | Todas as menções ao repositório externo substituídas pelo caminho local. |
| `sf-skills` (nome genérico) | `.agents/skills/` | `playbooks/01_development.md` | Referência textual atualizada para o caminho canônico local. |

---

## 2. Gaps Identificados

### `@skills:run-sfdx-scanner` — sem skill dedicada local

Não existe a skill `sf-code-analyzer` (nem equivalente) em `.agents/skills/`. A skill `sf-debug` foi descartada como substituta, pois cobre análise de debug logs, não análise estática de código (PMD/ESLint).

A skill `sf-deploy` foi usada como mapeamento provisório, pois:
- menciona explicitamente o **Code Analyzer v5** (`sf code-analyzer`) em seu pipeline de CI/CD
- inclui "análise estática" como etapa 3 do pipeline padrão (`CI/CD Guidance`)

**Recomendação:** criar a skill `.agents/skills/sf-code-analyzer/SKILL.md` dedicada para cobrir execução de `sf code-analyzer`, interpretação de resultados PMD/ESLint, e loop de auto-correção de apontamentos de severidade 1–3.

**Adicionalmente:** o comando CLI referenciado no playbook estava desatualizado (`sf scanner run` → o plugin `scanner` foi aposentado). Corrigido para `sf code-analyzer run`, alinhado com Code Analyzer v5 já instalado em `scripts/01_setup_env.sh`.

---

## 3. Pendências Marcadas como TODO

| Referência | Arquivo | Marcação aplicada |
|---|---|---|
| `playbooks/03_flosum_integration.md` | `playbooks/01_development.md` | `<!-- TODO: playbooks/03_flosum_integration.md ainda não foi criado — referência futura pendente. -->` |

---

## 4. Diff Resumido

### `playbooks/01_development.md` — 6 substituições

| Linha (aprox.) | Antes | Depois |
|---|---|---|
| 15 | `repositório \`sf-skills\`` | `\`.agents/skills/\`` |
| 17 | `` `@skills:create-scratch-org` `` | `` `@sf-deploy` `` |
| 30 | `Agent Skills do \`Jaganpro/sf-skills\`` | `Agent Skills de \`.agents/skills/\`` |
| 32 | `` `@skills:create-apex-class` ou `@skills:create-lwc` `` | `` `@sf-apex` ou `@sf-lwc` `` |
| 45 | `` `@skills:run-apex-tests` `` | `` `@sf-testing` `` |
| 51–52 | `` `@skills:run-sfdx-scanner` `` + `sf scanner run ...` | `` `@sf-deploy` `` + `sf code-analyzer run ...` + comentário GAP |
| 63 | `playbooks/03_flosum_integration.md` (sem marcação) | Idem + comentário `<!-- TODO -->` |

### `knowledge-base/01_domain_boundaries.md` — 0 alterações

O arquivo está em formato de meta-prompt (instrução para gerar o documento real). Não contém referências a skills ou repositórios externos. Nenhuma alteração necessária.

### `scripts/01_setup_env.sh` e `scripts/02_auth_orgs.sh` — 0 alterações

Nenhum comentário ou eco menciona skills ou o repositório `Jaganpro/sf-skills`. Nenhuma alteração necessária.

---

## 5. Verificação de Integridade (DoD)

Após aplicar as correções, verificar com:

```bash
# Deve retornar apenas nomes canônicos (presentes em .agents/skills/)
grep -rn "@skills:" . --include="*.md" --exclude-dir=".git"

# Deve retornar vazio (exceto .git/)
grep -rn "Jaganpro" . --include="*.md" --exclude-dir=".git"

# Deve retornar apenas referências legítimas a .agents/skills/
grep -rn "sf-skills" . --include="*.md" --exclude-dir=".git"
```
