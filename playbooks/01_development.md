# Playbook 01 — Desenvolvimento Local com Spec-Driven Development

**Para quem é este playbook?**
Para você, desenvolvedor júnior, que vai trabalhar com o Devin para implementar uma nova funcionalidade ou correção no Salesforce.

**Pré-requisitos obrigatórios antes de começar:**
- Ferramentas instaladas: `bash scripts/01_setup_env.sh` ✅
- Autenticado na sua sandbox: `sf org login web --alias sandbox-dev` ✅
- Autenticado no Flosum: `flosum auth login --url $FLOSUM_ORG_URL` ✅
- Você leu `devin-repo-spec.md` e entende o papel do Devin ✅
- Você leu `knowledge-base/metadata-ownership.yaml` e sabe o que seu time pode tocar ✅

---

## Antes de Tudo: A Sua Spec

Você não vai pedir ao Devin para "criar um trigger". Você vai **descrever o problema que precisa ser resolvido**.

Copie o template e crie a spec:

```bash
cp specs/_TEMPLATE.md specs/SN-XXXXX-nome-da-funcionalidade.md
```

Preencha todas as seções. Uma boa spec tem:
- **O que o usuário experimenta hoje** (problema)
- **O que ele deve experimentar depois** (solução esperada)
- **Quais metadados Salesforce estão envolvidos** (Matriz de Impacto)
- **Critérios de aceite testáveis** — comportamentos verificáveis, não intenções

> Quando a spec estiver clara, o Devin vai implementar com autonomia.
> Quando a spec for vaga, o Devin vai implementar algo errado com confiança.

---

## FASE 1 — Criar a Branch e Recuperar Metadados

**Quem faz:** Devin CLI (você inicia, o Devin executa)

### 1.1 — Criar branch no Flosum

O Flosum é o centro de versionamento. Toda funcionalidade começa com uma branch isolada lá:

```bash
flosum branch create --name "devin/SN-XXXXX-nome-da-funcionalidade"
```

Isso cria uma branch isolada no Flosum, vinculada ao seu pipeline de promoção.
Após criar, verifique:

```bash
flosum branch list
```

### 1.2 — Snapshot Parcial (recuperar apenas o que você vai mexer)

Esta é uma das regras mais importantes: **nunca faça snapshot completo**.

Consulte a Matriz de Impacto da sua spec e liste apenas os componentes afetados:

```bash
flosum snapshot partial \
  --branch "devin/SN-XXXXX-nome-da-funcionalidade" \
  --components "ApexClass:OrderTrigger,ApexClass:OrderTriggerTest,CustomObject:Order__c"
```

O Flosum vai buscar exatamente esses componentes do ambiente de Produção e sincronizar
com o seu repositório local. Você agora tem a versão mais atual para trabalhar em cima.

> Por que não snapshot completo?
> Um snapshot completo baixa TUDO — incluindo metadados de outros times,
> configurações sensíveis e componentes obsoletos. Cria conflitos e borra a fronteira
> de ownership. Seja cirúrgico.

### 1.3 — Verificar git status após o snapshot

```bash
git status
```

Você deve ver apenas os arquivos listados na sua Matriz de Impacto. Se aparecer
qualquer arquivo inesperado (especialmente Profiles ou objetos de outros domínios),
**pare e consulte o Tech Lead antes de prosseguir**.

---

## FASE 2 — Desenvolver no Repositório Local

**Quem faz:** Devin CLI

O Devin vai implementar a funcionalidade em `force-app/` baseado na spec.
Você não precisa escrever código — mas precisa **revisar o que o Devin escreveu**.

### 2.1 — Orientações que o Devin segue

O Devin usa as Agent Skills em `.agents/skills/` para manter padrões:
- **Apex:** `.agents/skills/sf-apex/SKILL.md` — padrões de Trigger handlers, Service layers
- **LWC:** `.agents/skills/sf-lwc/SKILL.md` — estrutura de componentes, eventos
- **Testes:** `.agents/skills/sf-testing/SKILL.md` — classes de teste, mocks, assertivas

### 2.2 — Regras de domínio (Devin respeita automaticamente)

O Devin consulta `knowledge-base/metadata-ownership.yaml` antes de tocar qualquer arquivo.
Se um metadado não pertence ao seu time, o Devin não modifica e alerta você.

### 2.3 — Push para Sandbox de Desenvolvimento (validação rápida)

Depois de implementar, o Devin valida que o código compila e não quebra nada:

```bash
sf project deploy start \
  --source-dir force-app \
  --target-org sandbox-dev
```

> Esta é a única org onde usamos `sf deploy` sem `--check-only`.
> É a sua sandbox **pessoal de desenvolvimento**. Não é QA, não é PreProd.

---

## FASE 3 — Garantia de Qualidade (DoD — Definition of Done)

**Sem passar nesta fase, o PR não abre. Sem exceção.**

### 3.1 — Validar Ownership de Metadados

```bash
python3 scripts/validation/check-metadata-ownership.py
```

Deve retornar sem violações. Se houver violação, o Devin ajusta os arquivos ou
você consulta o Tech Lead sobre o metadado compartilhado.

### 3.2 — Verificar Mudanças Destrutivas

```bash
python3 scripts/validation/check-destructive-changes.py
```

Se o script detectar mudanças destrutivas (campo deletado, regra de validação removida),
pare e solicite aprovação humana antes de prosseguir.

### 3.3 — Testes Unitários Apex (cobertura ≥ 85%)

```bash
sf apex run test \
  --target-org sandbox-dev \
  --code-coverage \
  --result-format human \
  --wait 10
```

Meta mínima: **85% de cobertura** nos componentes modificados.

Se a cobertura for menor:
1. O Devin analisa quais caminhos de código não estão cobertos
2. Adiciona casos de teste para cobrir esses cenários
3. Re-executa a suite até atingir a meta

Não peça ajuda ao humano por falha de cobertura — o Devin resolve sozinho.

### 3.4 — Análise Estática (zero falhas de severidade 1-3)

```bash
sf code-analyzer run \
  --target force-app \
  --engine pmd,eslint \
  --severity-threshold 3 \
  --format table
```

Se retornar alertas de severidade 1, 2 ou 3:
1. O Devin identifica a violação (SOQL em loop, FLS não verificado, etc.)
2. Refatora o código para corrigir
3. Re-executa o scanner

### 3.5 — Validação checkOnly na Org QA (simulação do deploy real)

Esta etapa simula exatamente o que o Flosum fará durante a promoção:

```bash
sf project deploy start \
  --check-only \
  --source-dir force-app \
  --target-org qa \
  --test-level RunLocalTests \
  --wait 30
```

Se falhar com um erro não documentado em `knowledge-base/known-issues.md`,
pare e acione revisão humana com o log completo do erro.

---

## FASE 4 — Commit e Pull Request

**Quem faz:** Devin CLI

### 4.1 — Criar branch Git e commitar

```bash
git checkout -b devin/SN-XXXXX-nome-da-funcionalidade
git add force-app/
git commit -m "feat(OrderTrigger): implementa validação de margem mínima conforme spec SN-XXXXX

Adiciona lógica de validação no OrderTrigger para bloquear pedidos com
margem abaixo de 15%. Inclui classe de teste com 91% de cobertura.

Flosum-Branch: devin/SN-XXXXX-nome-da-funcionalidade
Refs: #SN-XXXXX"
```

### 4.2 — Abrir Pull Request no GitHub

```bash
gh pr create \
  --title "feat(SN-XXXXX): [Título curto da funcionalidade]" \
  --body-file .github/PULL_REQUEST_TEMPLATE.md \
  --base main
```

O PR é o portão de qualidade. O revisor humano vai:
- Confirmar que os critérios de aceite da spec foram atendidos
- Verificar que nenhum arquivo fora do escopo foi alterado
- Aprovar ou solicitar ajustes

### 4.3 — Aguardar (o Devin para aqui)

Após o PR aberto, o Devin **não faz mais nada**. O fluxo humano assume:

```
PR revisado → aprovado → merge em main
  │
  └─► Flosum webhook detecta merge
        │
        └─► Promoção automática: QA → PreProd
              │
              └─► Aprovação humana → Produção
```

---

## Referência Rápida de Comandos

| Etapa | Comando |
|---|---|
| Criar branch no Flosum | `flosum branch create --name "devin/SN-XXXX-slug"` |
| Snapshot parcial | `flosum snapshot partial --branch "..." --components "..."` |
| Deploy na sandbox dev | `sf project deploy start --target-org sandbox-dev` |
| Validar ownership | `python3 scripts/validation/check-metadata-ownership.py` |
| Mudanças destrutivas | `python3 scripts/validation/check-destructive-changes.py` |
| Testes Apex | `sf apex run test --target-org sandbox-dev --code-coverage` |
| Análise estática | `sf code-analyzer run --target force-app --engine pmd,eslint` |
| CheckOnly QA | `sf project deploy start --check-only --target-org qa` |
| Abrir PR | `gh pr create --base main` |

---

## Quando Pedir Ajuda Humana

Você (ou o Devin) deve acionar o Tech Lead imediatamente se:

- `check-metadata-ownership.py` retornar violações não resolvíveis
- `check-destructive-changes.py` detectar mudanças destrutivas no escopo
- O `--check-only` falhar com erro desconhecido (não está em `known-issues.md`)
- Aparecerem arquivos de outros domínios no `git status` após o snapshot
- O Flosum reportar falha na promoção após o merge em `main`
- Houver conflito complexo em XML, Profiles ou Layouts

---

*Última atualização: 2026-04-26*
