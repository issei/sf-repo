# Contatos do Time e Canais de Escalação

## Time Commerce (este repositório)

| Papel | Nome | GitHub | Slack | Quando acionar |
|---|---|---|---|---|
| Tech Lead | {nome} | @tech-lead | @tech-lead | Decisões arquiteturais, hotfixes, conflitos |
| DevOps Admin | {nome} | @devops-admin | @devops-admin | Credenciais, pipelines, infraestrutura |
| Product Owner | {nome} | @product-owner | @product-owner | Aprovação de promoções para Produção |

## Canais Slack

| Canal | Propósito |
|---|---|
| `#sf-commerce` | Comunicação interna do time |
| `#sf-devops` | Coordenação entre times para deploys |
| `#sf-incidents` | Incidentes em produção |
| `#sf-releases` | Anúncios de releases e promoções |

## Outros Times (co-owners de componentes compartilhados)

| Time | Canal Slack | GitHub Team | Componentes compartilhados |
|---|---|---|---|
| Sales | `#sf-sales` | @team-sales | SalesConsole, Sales_User Profile |
| Service | `#sf-service` | @team-service | Sales_User Profile |

## Protocolo de Escalação

```
Nível 1: Consultar known-issues.md
Nível 2: Notificar no canal do time (#sf-commerce)
Nível 3: Acionar Tech Lead diretamente
Nível 4: Acionar #sf-incidents (apenas para impacto em produção)
```

## Janelas de Deploy Recomendadas

| Ambiente | Janela preferida | Evitar |
|---|---|---|
| QA | Segunda a sexta, horário comercial | Fins de semana |
| PreProd | Terças e quintas | Vésperas de feriados |
| Produção | Terças e quartas, manhã | Sextas, vésperas de feriados, semana de fechamento |
