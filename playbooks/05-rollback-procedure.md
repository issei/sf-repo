# Playbook 05 — Rollback Seguro

**Quando usar:** Quando uma promoção causar problemas em QA, PreProd ou (especialmente) Produção.

🛑 **REGRA FUNDAMENTAL:** Em ambiente compartilhado, rollback SEMPRE via Flosum.
Nunca fazer deploy direto via sf CLI para corrigir.

---

## Passo 1: Identificar o escopo do problema

```bash
# Verificar qual promoção causou o problema
python3 scripts/flosum/get-promotion-status.py \
  --pipeline-id "${FLOSUM_PIPELINE_ID}" \
  --environment "<ambiente-afetado>"
```

Coletar:
- ID da promoção problemática
- Componentes afetados
- Timestamp do deploy

## Passo 2: Registrar o incidente

```bash
python3 scripts/reporting/log-failure.py \
  --type flosum_api \
  --error-code "ROLLBACK_REQUIRED" \
  --error "Deploy causou regressão em <ambiente>" \
  --context "Rollback iniciado para promoção <ID>"
```

## Passo 3: Notificar imediatamente

🛑 **PARADA HUMANA OBRIGATÓRIA PARA ROLLBACK EM PRODUÇÃO.**

Para QA e PreProd, notificar via Slack `#sf-devops`.
Para Produção, notificar `#sf-incidents` e acionar o Tech Lead imediatamente.

## Passo 4: Identificar o commit alvo do rollback

```bash
# Encontrar a tag de promoção anterior bem-sucedida
git tag -l "flosum/promoted/<ambiente>/*" | sort | tail -5
```

Identificar o commit da última promoção bem-sucedida.

## Passo 5: Criar branch de rollback

```bash
# Nunca reverter diretamente em main
git checkout -b fix/rollback-<ambiente>-$(date +%Y%m%d)
git revert <commit-sha> --no-edit
git push origin fix/rollback-<ambiente>-$(date +%Y%m%d)
```

## Passo 6: Validar o rollback

```bash
# Atualizar o package-deploy.xml com o estado anterior
bash scripts/salesforce/validate-deploy.sh <ambiente> manifests/package-deploy.xml
```

## Passo 7: Abrir PR emergencial de rollback

Abrir PR com:
- Título: `[ROLLBACK] <ambiente>: <descrição do problema>`
- Checklist de segurança preenchido
- Referência ao incidente/issue

🛑 **PARADA:** Aguardar aprovação humana antes de promover o rollback.

## Passo 8: Promover rollback via Flosum

Seguir Playbook 03, Passos 2 a 6, com o branch de rollback.

---

## Verificação Pós-Rollback

- [ ] Incidente registrado em `logs/failures/`
- [ ] Notificações enviadas para os canais corretos
- [ ] Rollback promovido com sucesso via Flosum
- [ ] Ambiente funcional verificado
- [ ] Post-mortem agendado (para incidentes em Produção)
- [ ] Entrada criada em `knowledge-base/known-issues.md`
