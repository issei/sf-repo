# Scripts — Catálogo

Automação executável para operações Salesforce, Flosum, validação e relatórios.

## Estrutura

| Diretório | Conteúdo |
|---|---|
| `environment/` | Bootstrap e verificação do ambiente |
| `salesforce/` | Operações com sf CLI |
| `flosum/` | Integração com a API REST do Flosum |
| `validation/` | Validações de segurança pré-deploy |
| `reporting/` | Geração de relatórios e logs de falhas |

## Referência Rápida

### Environment

| Script | Uso | Quando |
|---|---|---|
| `environment/setup.sh` | Bootstrap completo | Primeira execução ou após reset |
| `environment/authenticate-orgs.sh` | Autenticar nas orgs via JWT | Quando credenciais expirarem |
| `environment/verify-dependencies.sh` | Verificar versões | Antes de qualquer operação |

### Salesforce

| Script | Uso | Quando |
|---|---|---|
| `salesforce/retrieve-metadata.sh <org> <manifest>` | Retrieve seletivo | Sincronizar estado da org |
| `salesforce/validate-deploy.sh <org> <manifest>` | Validação checkOnly | Antes de abrir PR |
| `salesforce/run-tests.sh <org>` | Executar testes Apex | Antes de abrir PR |
| `salesforce/compare-org-state.py` | Comparar local vs org | Para detectar desvios |

### Flosum

| Script | Uso | Quando |
|---|---|---|
| `flosum/flosum_api.py --check-connectivity` | Teste de conectividade | No setup |
| `flosum/create-branch.py` | Criar branch no Flosum | Após PR aprovado |
| `flosum/trigger-promotion.py` | Disparar promoção | Após criar branch |
| `flosum/get-promotion-status.py` | Consultar status | Durante promoção |
| `flosum/link-commit-to-branch.py` | Vincular commit | Para rastreabilidade |

### Validation

| Script | Uso | Quando |
|---|---|---|
| `validation/check-metadata-ownership.py` | Verificar ownership | SEMPRE antes de deploy |
| `validation/check-destructive-changes.py` | Detectar deleções | Se houver deleções |
| `validation/check-shared-components.py` | Verificar impacto compartilhado | Se houver componentes shared |

### Reporting

| Script | Uso | Quando |
|---|---|---|
| `reporting/log-failure.py` | Registrar falha | Sempre que algo falhar |
| `reporting/generate-deploy-report.py` | Gerar relatório | Após validação/deploy |
