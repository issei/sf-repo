# Arquitetura do Pipeline de DevOps Salesforce

## Diagrama do Modelo Federado

```mermaid
graph TD
    subgraph "Time Commerce (este repo)"
        DEV1[Dev Local] --> GH1[GitHub\nteam-commerce-sf]
        GH1 --> FL1[Flosum Branch\ncommerce/*]
    end

    subgraph "Time Sales (repo separado)"
        DEV2[Dev Local] --> GH2[GitHub\nteam-sales-sf]
        GH2 --> FL2[Flosum Branch\nsales/*]
    end

    subgraph "Time Service (repo separado)"
        DEV3[Dev Local] --> GH3[GitHub\nteam-service-sf]
        GH3 --> FL3[Flosum Branch\nservice/*]
    end

    subgraph "Flosum — Pipeline Unificado"
        FL1 --> QA_FL[Flosum: QA Pipeline]
        FL2 --> QA_FL
        FL3 --> QA_FL
        QA_FL --> PREPROD_FL[Flosum: PreProd Pipeline]
        PREPROD_FL --> PROD_FL[Flosum: Prod Pipeline]
    end

    subgraph "Orgs Salesforce Compartilhadas"
        QA_FL --> ORG_QA[(Org QA)]
        PREPROD_FL --> ORG_PREPROD[(Org PreProd)]
        PROD_FL --> ORG_PROD[(Org Prod)]
    end

    style GH1 fill:#2d6a4f,color:#fff
    style FL1 fill:#1b4332,color:#fff
```

## Regra de Ouro do Ambiente Compartilhado

> Cada time é responsável somente por sua fatia de metadata.
> O Flosum serializa as promoções, mas não garante isolamento de metadata.
> **O isolamento é garantido pelo `metadata-ownership.yaml` e pelos scripts de validação.**

## Acesso por Ambiente

| Ambiente | Acesso do Devin | Deploy via |
|---|---|---|
| Dev/Scratch | Leitura + escrita total | sf CLI direto |
| QA | Apenas validação (checkOnly) | Flosum |
| PreProd | Apenas validação (checkOnly) | Flosum |
| Produção | Apenas leitura | Flosum (humano aprova) |

## Por que o Flosum é o único canal de deploy

```
sf CLI deploy → Bypassa pipeline Flosum → Sem rastreabilidade de aprovação
                                        → Sem serialização entre times
                                        → Risco de sobrescrita silenciosa

Flosum deploy  → Registro de aprovação  → Serializado por ambiente
               → Histórico auditável   → Notificações para todos os times
               → Rollback controlado   → Visibilidade unificada
```

O Devin possui credenciais JWT com **acesso de leitura/validação** nas orgs,
mas **nunca possui** as credenciais de deploy direto.
Isso torna a restrição arquitetural, não apenas documental.
