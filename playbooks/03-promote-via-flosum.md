# Playbook 03 — Promover via Flosum

**Quando usar:** Após PR aprovado por revisores humanos e CI passando.

**Pré-requisitos:** PR aprovado com todos os checks de CI verde.

---

## Passo 1: Confirmar aprovação do PR

Verificar que o PR tem:
- [ ] Aprovação de pelo menos 1 revisor humano
- [ ] Todos os checks de CI passando (validate-pr, check-metadata-ownership)
- [ ] Label `approved-destructive` se houver mudanças destrutivas

🛑 **PARADA:** Se o PR não tiver aprovação humana, não prosseguir.

## Passo 2: Criar branch no Flosum

```bash
python3 scripts/flosum/create-branch.py \
  --name "devin/${BRANCH_NAME}" \
  --pipeline-id "${FLOSUM_PIPELINE_ID}" \
  --commit-sha "$(git rev-parse HEAD)" \
  --pr-number "${PR_NUMBER}"
```

Guardar o ID retornado como `FLOSUM_BRANCH_ID`.

## Passo 3: Vincular commit ao branch Flosum

```bash
python3 scripts/flosum/link-commit-to-branch.py \
  --flosum-branch-id "${FLOSUM_BRANCH_ID}" \
  --commit-sha "$(git rev-parse HEAD)" \
  --pr-url "${PR_URL}"
```

## Passo 4: Disparar promoção para QA

```bash
python3 scripts/flosum/trigger-promotion.py \
  --branch-id "${FLOSUM_BRANCH_ID}" \
  --target-environment "qa" \
  --pipeline-id "${FLOSUM_PIPELINE_ID}"
```

## Passo 5: Monitorar status da promoção

```bash
# Polling a cada 30 segundos, máximo 20 tentativas
for i in {1..20}; do
  python3 scripts/flosum/get-promotion-status.py \
    --branch-id "${FLOSUM_BRANCH_ID}" \
    --pipeline-id "${FLOSUM_PIPELINE_ID}"
  sleep 30
done
```

Status possíveis:
- `Pending` / `In Progress` — aguardar
- `Succeeded` — prosseguir para Passo 6
- `Failed` — registrar falha e consultar Playbook 04 ou 05

## Passo 6: Confirmar promoção QA bem-sucedida

Se `Succeeded`:
- Gerar relatório de deploy: `python3 scripts/reporting/generate-deploy-report.py`
- Comentar no PR com o resultado
- Tag automática será criada: `flosum/promoted/qa/YYYYMMDD-HHMMSS`

## Passo 7: Promoção para PreProd

Repetir Passos 4 a 6 com `--target-environment "preprod"`.

Requer aprovação adicional do Tech Lead antes de prosseguir.

## Passo 8: Promoção para Produção

🛑 **PARADA HUMANA OBRIGATÓRIA:** Promoção para Produção requer:
1. PR completamente aprovado e mergeado em `main`
2. Comentário explícito no PR: `/approve-prod-promotion`
3. Aprovação do Tech Lead ou Product Owner

Só prosseguir após estas condições serem atendidas.

```bash
python3 scripts/flosum/trigger-promotion.py \
  --branch-id "${FLOSUM_BRANCH_ID}" \
  --target-environment "prod" \
  --pipeline-id "${FLOSUM_PIPELINE_ID}"
```

---

## Tratamento de Falhas

Se qualquer passo falhar:
1. Registrar falha: `python3 scripts/reporting/log-failure.py --type flosum_api --error "..." --context "promoção QA"`
2. Consultar `knowledge-base/known-issues.md`
3. Se não houver solução conhecida, acionar revisão humana

---

## Verificação Final

- [ ] Promoção QA — Succeeded
- [ ] Promoção PreProd — Succeeded (se aplicável)
- [ ] Promoção Prod — Succeeded (se aplicável, com aprovação humana)
- [ ] Tags de rastreabilidade criadas
- [ ] Relatório de deploy gerado em `reports/`
