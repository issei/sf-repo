# Playbooks — Índice e Guia de Uso

Os playbooks são SOPs (Procedimentos Operacionais Padrão) executáveis passo a passo.
O Devin deve ler o playbook relevante ANTES de iniciar qualquer tarefa.

## Quando usar cada playbook

| Playbook | Quando usar |
|---|---|
| [00-setup-environment.md](00-setup-environment.md) | Primeira execução ou após reset do ambiente |
| [01-retrieve-org-state.md](01-retrieve-org-state.md) | Antes de iniciar desenvolvimento — sincronizar estado da org |
| [02-develop-and-validate.md](02-develop-and-validate.md) | Durante o ciclo de desenvolvimento (codificação + testes) |
| [03-promote-via-flosum.md](03-promote-via-flosum.md) | Após PR aprovado — promover via Flosum |
| [04-handle-conflicts.md](04-handle-conflicts.md) | Quando detectar metadata de outro time ou conflito de merge |
| [05-rollback-procedure.md](05-rollback-procedure.md) | Quando uma promoção causar problemas em QA ou PreProd |
| [06-hotfix-protocol.md](06-hotfix-protocol.md) | Correções urgentes que não podem seguir o fluxo normal |

## Ordem padrão para uma tarefa nova

```
00 (setup, se necessário)
  → 01 (recuperar estado atual da org)
    → 02 (desenvolver e validar)
      → 03 (promover via Flosum)
```

## Princípios dos Playbooks

- Cada passo é verificável — o Devin pode confirmar se concluiu antes de avançar
- Pontos de parada humana são marcados com `🛑 PARADA HUMANA OBRIGATÓRIA`
- Comandos prontos para copiar e executar
- Referências cruzadas para scripts e knowledge-base
