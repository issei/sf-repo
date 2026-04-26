# Inventário de Orgs Salesforce

> IDs reais são injetados via variáveis de ambiente. Nunca hardcode IDs aqui.

## Orgs Ativas

| Alias | Propósito | Acesso do Devin | URL de Instância | Variável de Credencial |
|---|---|---|---|---|
| `qa` | Quality Assurance — testes integrados | Validação apenas (checkOnly) | `SF_INSTANCE_URL_QA` | `SF_JWT_KEY_QA` |
| `preprod` | Homologação — staging pré-produção | Validação apenas (checkOnly) | `SF_INSTANCE_URL_PREPROD` | `SF_JWT_KEY_PREPROD` |
| `prod` | Produção — ambiente live | Apenas leitura | `SF_INSTANCE_URL_PROD` | `SF_JWT_KEY_PROD` |

## Usuários de Serviço (por org)

| Org | Variável de Usuário | Tipo de Acesso |
|---|---|---|
| QA | `SF_USERNAME_QA` | Validação + retrieve |
| PreProd | `SF_USERNAME_PREPROD` | Validação + retrieve |
| Prod | `SF_USERNAME_PROD` | Somente leitura |

## Regras de Acesso

1. **Deploy direto via sf CLI é PROIBIDO** em todas as orgs listadas acima.
2. O único canal de deploy é o Flosum (via API).
3. Validação checkOnly é permitida em QA e PreProd.
4. Retrieve de metadata é permitido em todas as orgs para sincronização.

## Verificar Status das Orgs

```bash
sf org list
sf org display --target-org qa
sf org display --target-org preprod
sf org display --target-org prod
```

## Limites Operacionais Relevantes

| Limite | Org QA | Obs |
|---|---|---|
| Deploys simultâneos | 1 por vez | Coordenar via Flosum |
| Timeout de validação | 10 min | Configurado em `validate-deploy.sh` |
| Cobertura mínima de testes | 75% | 85% para classes novas |
