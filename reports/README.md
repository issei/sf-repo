# Relatórios de Deploy

Relatórios gerados automaticamente após validações e promoções via Flosum.

## Geração Automática

Os relatórios são criados por `scripts/reporting/generate-deploy-report.py` após:
- Validação checkOnly na org QA
- Promoção bem-sucedida via Flosum

## Formato dos Arquivos

`deploy-{YYYYMMDD-HHMMSS}-{ambiente}.md`

Exemplos:
- `deploy-20260115-143022-qa.md`
- `deploy-20260115-160000-preprod.md`
- `deploy-20260116-090000-prod.md`

## Retenção

- Relatórios de QA: 30 dias
- Relatórios de PreProd: 60 dias
- Relatórios de Produção: permanente (auditoria)

Os arquivos antigos podem ser removidos manualmente pelo time, mantendo os de Produção.
