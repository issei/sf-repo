# Prompt: Auditoria e Ajuste de Referências de Skills

> **Para:** Agente de engenharia autônomo (Devin, Claude Code ou equivalente)
> **Escopo:** Repositório `sf-repo` (orquestração DevOps Salesforce + Flosum)
> **Tipo de tarefa:** Refatoração de documentação — sem alteração de código executável.

---

## 1. Contexto

Este repositório é o arcabouço operacional que você usa para trabalhar no ecossistema Salesforce federado da squad. Ele contém quatro camadas:

- `scripts/` — bootstrap de ambiente (Node, `sf` CLI, plugins).
- `knowledge-base/` — limites de domínio que você DEVE respeitar.
- `playbooks/` — SOPs operacionais que você executa em cada tarefa.
- `.agents/skills/` — biblioteca local de skills especializadas que você carrega sob demanda.

**O problema:** os playbooks e a knowledge base foram redigidos antes da consolidação da pasta `.agents/skills/`. Eles referenciam:

1. Um repositório externo `Jaganpro/sf-skills` que não é mais a fonte de verdade.
2. Invocações genéricas como `@skills:create-scratch-org`, `@skills:run-apex-tests`, `@skills:run-sfdx-scanner`, `@skills:create-apex-class`, `@skills:create-lwc` que não correspondem aos nomes reais das skills locais.
3. Playbooks futuros (ex.: `playbooks/03_flosum_integration.md`) que ainda não foram criados.

Sua missão é **auditar todas as referências cruzadas e ajustá-las** para apontar para a estrutura real do repositório, sem alterar a lógica operacional dos documentos.

---

## 2. Fonte de verdade

Antes de qualquer alteração, **liste e leia** o conteúdo de cada subpasta de `.agents/skills/`. Esta é a fonte de verdade dos nomes canônicos. As skills atuais incluem (não exaustivo):

- **Flosum:** `flosum-auth`, `flosum-branch`, `flosum-deploy`, `flosum-repo`, `flosum-setup`, `flosum-snapshot`, `flosum-source-pull`, `flosum-source-push`.
- **Salesforce core:** `sf-apex`, `sf-lwc`, `sf-flow`, `sf-soql`, `sf-deploy`, `sf-metadata`, `sf-permissions`, `sf-testing`, `sf-debug`, `sf-docs`, `sf-data`, `sf-integration`, `sf-connected-apps`.
- **Diagramas:** `sf-diagram-mermaid`, `sf-diagram-nanobananapro`.
- **Agentforce / IA:** `sf-ai-agentforce`, `sf-ai-agentforce-observability`, `sf-ai-agentforce-persona`, `sf-ai-agentforce-testing`, `sf-ai-agentscript`.
- **Data Cloud:** `sf-datacloud`, `sf-datacloud-act`, `sf-datacloud-connect`, `sf-datacloud-harmonize`, `sf-datacloud-prepare`, `sf-datacloud-retrieve`, `sf-datacloud-segment`.
- **Industries Common Core:** `sf-industry-commoncore-callable-apex`, `sf-industry-commoncore-datamapper`, `sf-industry-commoncore-flexcard`, `sf-industry-commoncore-integration-procedure`, `sf-industry-commoncore-omniscript`, `sf-industry-commoncore-omnistudio-analyze`.

Para cada skill, abra o `SKILL.md` correspondente e identifique **qual o nome canônico de invocação** declarado nos metadados — use exatamente esse nome nas referências.

---

## 3. Tarefas — execute na ordem

### 3.1. Mapeamento

Construa uma tabela de equivalência entre os nomes antigos (encontrados nos documentos) e os nomes canônicos (encontrados em `.agents/skills/<nome>/SKILL.md`). Sugestão inicial — **valide cada linha lendo o SKILL.md correspondente antes de aplicar**:

| Referência antiga | Skill local equivalente | Observação |
|---|---|---|
| `@skills:create-scratch-org` | `sf-deploy` ou `sf-metadata` | Confirmar qual cobre criação de scratch org. |
| `@skills:create-apex-class` | `sf-apex` | — |
| `@skills:create-lwc` | `sf-lwc` | — |
| `@skills:run-apex-tests` | `sf-testing` | — |
| `@skills:run-sfdx-scanner` | `sf-debug` ou nova skill `sf-code-analyzer` | Verificar se existe skill dedicada; senão, reportar gap. |
| `Jaganpro/sf-skills` (repositório externo) | `.agents/skills/` (local) | Substituir todas as menções. |

> Se algum mapeamento **não tiver equivalente local**, NÃO invente. Registre o gap na seção 5 (relatório).

### 3.2. Arquivos a auditar

Faça grep recursivo por `@skills:`, `sf-skills`, `Jaganpro` e qualquer caminho `playbooks/` mencionado, em pelo menos:

- `playbooks/01_development.md`
- `knowledge-base/01_domain_boundaries.md`
- `scripts/*.sh` (verificar se algum eco/comentário menciona skills)
- Qualquer outro `*.md` no repositório (use `grep -rn` para garantir cobertura).

### 3.3. Edições a aplicar

Para cada referência encontrada:

1. **Substitua** o nome antigo pelo nome canônico da skill local.
2. **Atualize** menções ao repositório `Jaganpro/sf-skills` para `.agents/skills/<skill>` (caminho local).
3. **Mantenha** o fallback CLI (`sf <comando>`) intacto — ele continua válido como plano B.
4. **Marque com `<!-- TODO -->`** qualquer referência a playbook ainda não existente (ex.: `playbooks/03_flosum_integration.md`), em vez de removê-la — ela sinaliza trabalho futuro.

### 3.4. Limites — o que você NÃO pode fazer

- NÃO altere a lógica operacional dos playbooks (fases, ordem dos passos, metas de cobertura).
- NÃO modifique scripts em `scripts/` exceto comentários que mencionem skills antigas.
- NÃO crie playbooks novos (ex.: o `03_flosum_integration.md`) nesta tarefa — escopo é só ajuste de referências.
- NÃO renomeie pastas de skills em `.agents/skills/`.
- NÃO altere o `01_domain_boundaries.md` além das referências; ele ainda está em formato de meta-prompt e o preenchimento real é tarefa separada.

---

## 4. Critérios de aceitação (DoD)

Antes de fechar a tarefa, garanta que:

- [ ] `grep -rn "@skills:" .` retorna apenas invocações com nomes canônicos válidos (presentes em `.agents/skills/`).
- [ ] `grep -rn "Jaganpro" .` não retorna nada, ou apenas em arquivos de `.git/` (que você não deve tocar).
- [ ] `grep -rn "sf-skills" .` retorna apenas referências legítimas a `.agents/skills/`.
- [ ] Para cada skill referenciada, existe `.agents/skills/<nome>/SKILL.md` correspondente.
- [ ] Toda referência a playbook inexistente está marcada com `<!-- TODO -->`.
- [ ] `git diff` mostra apenas alterações em arquivos `.md` (e eventualmente comentários de `.sh`), sem mudanças funcionais.

---

## 5. Relatório final

Ao concluir, produza um arquivo `prompts/relatorio-ajuste-referencias.md` contendo:

1. **Tabela de mapeamento aplicada** — nome antigo → nome canônico → arquivos onde foi alterado.
2. **Gaps identificados** — referências antigas sem equivalente local (ex.: se `run-sfdx-scanner` não tiver skill local).
3. **Pendências marcadas como TODO** — lista dos playbooks futuros referenciados.
4. **Diff resumido** — arquivos alterados e número de substituições por arquivo.

---

## 6. Comportamento em caso de dúvida

Se durante a execução você encontrar uma referência ambígua (ex.: dois SKILL.md poderiam atender o mesmo nome antigo), **pause e pergunte ao Tech Lead** antes de aplicar a substituição. Não chute o mapeamento — referências erradas em playbook geram retrabalho silencioso em todas as tarefas futuras.
