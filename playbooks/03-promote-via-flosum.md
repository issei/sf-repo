# Playbook 03 — Promover via Flosum (Git-Native)

**Quando usar:** Após o desenvolvimento estar concluído, validação checkOnly passou e o código está pronto para revisão.

**Pré-requisitos:** Branch criada, testes Apex passando, `check-metadata-ownership.py` sem violações.

> **Princípio fundamental:** A promoção ocorre **exclusivamente via merge do Pull Request
> na branch `main`**. O Devin não faz deploy de código para QA ou Prod.
> O Devin abre o PR no GitHub e, após aprovação humana e merge, o **webhook nativo do
> Flosum** assume o pacote e o implanta nas Orgs alvo automaticamente.

---

## Passo 1: Confirmar pré-requisitos antes de abrir o PR

- [ ] Validação checkOnly passou na org QA:
  ```bash
  sf project deploy start \
    --check-only \
    --source-dir force-app \
    --target-org qa \
    --test-level RunLocalTests
  ```
- [ ] Ownership verificado: `python3 scripts/validation/check-metadata-ownership.py`
- [ ] Mudanças destrutivas verificadas (se aplicável): `python3 scripts/validation/check-destructive-changes.py`
- [ ] Componentes compartilhados verificados: `python3 scripts/validation/check-shared-components.py`
- [ ] Todos os arquivos staged e commitados na branch `devin/{ticket}-{slug}`

🛑 **PARADA:** Se qualquer verificação falhar, corrija antes de abrir o PR.

---

## Passo 2: Abrir o Pull Request

```bash
gh pr create \
  --title "feat(<escopo>): <descrição curta> [SN-XXXXX]" \
  --body-file .github/PULL_REQUEST_TEMPLATE.md \
  --base main
```

O PR acionará automaticamente os workflows de CI:
- `validate-pr.yml` — validação e testes Apex na org QA
- `check-metadata-ownership.yml` — verificação de ownership e mudanças destrutivas

---

## Passo 3: Aguardar aprovação humana

🛑 **PARADA HUMANA OBRIGATÓRIA:** O Devin não avança após abrir o PR.

O PR deve ter:
- [ ] Aprovação de pelo menos 1 revisor humano
- [ ] Todos os checks de CI passando (verde)
- [ ] Label `approved-destructive` se houver mudanças destrutivas

O revisor humano é responsável por fazer o **merge** do PR em `main`.

---

## Passo 4: Promoção automática pelo Flosum (pós-merge)

Após o merge em `main`, o Flosum detecta a mudança via webhook nativo do GitHub e executa o pipeline de promoção automaticamente:

```
main (merge) → Flosum Webhook → QA → (aprovação Tech Lead) → PreProd → (aprovação humana) → Prod
```

O Devin **não executa nenhum comando** nesta etapa. O monitoramento do pipeline é feito diretamente na interface web do Flosum.

---

## Passo 5: Verificação pós-promoção (opcional)

Se solicitado pelo Tech Lead, verificar o estado da org após promoção:

```bash
# Verificar que os componentes estão na org QA
sf org list metadata \
  --metadata-type ApexClass \
  --target-org qa
```

Gerar relatório de deploy se necessário:
```bash
python3 scripts/reporting/generate-deploy-report.py
```

---

## Tratamento de Falhas no Pipeline Flosum

Se o pipeline Flosum reportar falha após o merge:

1. **NÃO tente re-executar comandos de deploy diretamente**
2. Registrar a falha: `python3 scripts/reporting/log-failure.py --type flosum_pipeline --error "..." --context "promoção QA"`
3. Consultar `knowledge-base/known-issues.md`
4. Acionar revisão humana com o log de erro do Flosum

---

## Verificação Final

- [ ] PR aberto com template preenchido
- [ ] CI passou (validate-pr + check-metadata-ownership)
- [ ] PR aprovado por revisor humano
- [ ] Merge em `main` realizado pelo revisor
- [ ] Pipeline Flosum executando (monitorar na interface web do Flosum)
- [ ] Relatório de deploy gerado em `reports/` (se solicitado)
