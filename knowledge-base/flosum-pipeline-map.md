# Mapa do Pipeline Flosum

## Estrutura de Ambientes

| Ambiente | Propósito | Acesso do Devin | Quem promove |
|---|---|---|---|
| Dev (local/scratch) | Desenvolvimento | Leitura/escrita total | Devin |
| QA | Testes integrados | Apenas validação | Flosum (via API) |
| PreProd | Homologação | Apenas validação | Flosum (via API) |
| Produção | Live | Apenas leitura | Flosum (humano aprova) |

## Fluxo de Promoção

```
GitHub PR (aprovado)
    → scripts/flosum/create-branch.py   [cria branch no Flosum]
    → scripts/flosum/trigger-promotion.py [dispara promoção QA]
    → Poll: scripts/flosum/get-promotion-status.py
    → Se sucesso: tag no commit + comentário no PR
    → Para PreProd: repetir ciclo com aprovação adicional
    → Para Prod: SOMENTE com aprovação humana explícita
```

## IDs de Referência do Pipeline

> Os IDs reais são injetados via variáveis de ambiente.
> Nunca hardcode IDs de pipeline no código.

| Variável | Descrição |
|---|---|
| `FLOSUM_PIPELINE_ID` | ID do pipeline principal deste time |
| `FLOSUM_ORG_CREDENTIAL_ID_QA` | Credencial da org QA no Flosum |
| `FLOSUM_ORG_CREDENTIAL_ID_PREPROD` | Credencial da org PreProd no Flosum |

## Convenção de Branches Flosum

| Prefixo | Quando usar |
|---|---|
| `devin/` | Branches criados autonomamente pelo Devin |
| `feature/` | Features desenvolvidas pela equipe |
| `fix/` | Correções de bug |
| `hotfix/` | Correções urgentes em produção |
| `release/` | Release candidates |

## Rastreabilidade GitHub ↔ Flosum

**GitHub → Flosum:**
- Commit message contém `Flosum-Branch: <id>` e `Flosum-Promotion: <id>`

**Flosum → GitHub:**
- Tag Git criada após promoção bem-sucedida
- Formato: `flosum/promoted/{ambiente}/{YYYYMMDD-HHMMSS}`

## Regras de Aprovação por Ambiente

| Ambiente | Aprovações necessárias |
|---|---|
| QA | PR aprovado por 1 revisor + CI verde |
| PreProd | PR aprovado por 1 revisor + Tech Lead confirmou |
| Produção | PR aprovado + mergeado em main + comentário `/approve-prod-promotion` |
