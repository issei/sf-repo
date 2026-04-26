# Playbook 06 — Protocolo de Hotfix

**Quando usar:** Correções urgentes que afetam Produção e não podem aguardar o ciclo normal de release.

🛑 **REGRA:** Hotfixes também precisam de aprovação humana. A diferença é que o processo é acelerado, não eliminado.

---

## Critérios para Hotfix

Um hotfix é justificado quando:
- Bug em Produção causando impacto direto ao negócio
- Falha de segurança crítica
- Dados sendo corrompidos ou inacessíveis
- SLA em risco

Se a situação não atender esses critérios, usar o fluxo normal (Playbooks 01-03).

---

## Passo 1: Notificar imediatamente

Notificar via Slack `#sf-incidents`:
```
🚨 HOTFIX INICIADO
Time: {TEAM_NAME}
Problema: <descrição do bug>
Impacto: <impacto estimado>
ETA: <estimativa de resolução>
```

Aguardar confirmação do Tech Lead para prosseguir.

## Passo 2: Criar branch hotfix a partir de main

```bash
git checkout main
git pull origin main
git checkout -b hotfix/JIRA-XXX-descricao-urgente
```

## Passo 3: Implementar correção mínima

Implementar APENAS a correção necessária. Sem refatorações adicionais.
Seguir as regras de ownership: mesmo em hotfix, não tocar metadata de outros times.

## Passo 4: Validação acelerada

```bash
# Ownership check (obrigatório mesmo em hotfix)
python3 scripts/validation/check-metadata-ownership.py \
  --manifest manifests/package-deploy.xml \
  --ownership knowledge-base/metadata-ownership.yaml \
  --fail-on-violation

# Validação checkOnly em QA
bash scripts/salesforce/validate-deploy.sh qa manifests/package-deploy.xml

# Testes mínimos (classes afetadas)
bash scripts/salesforce/run-tests.sh qa
```

## Passo 5: PR emergencial

Abrir PR com:
- Label: `hotfix`, `urgent`
- Aprovação de 1 revisor é suficiente (normalmente são 2)
- Mencionar Tech Lead explicitamente: `@tech-lead HOTFIX - por favor revisar urgente`

🛑 **PARADA:** Aguardar aprovação mesmo em hotfix. Tempo mínimo: confirmar com Tech Lead.

## Passo 6: Promoção acelerada via Flosum

```bash
# Criar branch Flosum com flag de urgência
python3 scripts/flosum/create-branch.py \
  --name "hotfix/${BRANCH_NAME}" \
  --pipeline-id "${FLOSUM_PIPELINE_ID}" \
  --priority "high"

# Promoção direta QA → PreProd → Prod (com aprovações)
python3 scripts/flosum/trigger-promotion.py \
  --branch-id "${FLOSUM_BRANCH_ID}" \
  --target-environment "qa"
```

Monitorar status a cada 15 segundos (ao invés de 30).

## Passo 7: Merge em main após promoção bem-sucedida

```bash
# Após promoção em Prod aprovada e concluída
git checkout main
git merge --no-ff hotfix/JIRA-XXX-descricao-urgente
git push origin main
git tag -a "hotfix/JIRA-XXX" -m "Hotfix: <descrição>"
git push origin "hotfix/JIRA-XXX"
```

## Passo 8: Post-mortem

Após resolução, agendar post-mortem com o time:
- O que causou o bug?
- Como poderia ter sido evitado?
- Criar entrada em `knowledge-base/known-issues.md`

---

## Verificação Final

- [ ] Tech Lead notificado e aprovou início do hotfix
- [ ] Correção mínima implementada (sem escopo adicional)
- [ ] Ownership verificado
- [ ] Validação checkOnly passou
- [ ] PR aprovado por pelo menos 1 revisor
- [ ] Promoção bem-sucedida em todos os ambientes
- [ ] Merge em `main` realizado
- [ ] Tag de hotfix criada
- [ ] Post-mortem agendado
