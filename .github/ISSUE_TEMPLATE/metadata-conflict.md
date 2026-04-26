---
name: Metadata Conflict
about: Reportar conflito de metadata entre times em ambiente compartilhado
title: '[CONFLITO] <tipo-metadata>: <nome-componente>'
labels: metadata-conflict, needs-coordination
assignees: ''
---

## Componente em Conflito

**Tipo de Metadata:** <!-- ApexClass, Flow, CustomObject, Profile, etc. -->
**Nome do Componente:** <!-- Nome exato do componente -->
**Ambiente afetado:** <!-- QA / PreProd / Produção -->

## Times Envolvidos

| Time | Repositório | Contato |
|---|---|---|
| Time A (este) | <!-- nome do repo --> | <!-- @github-handle --> |
| Time B | <!-- nome do repo --> | <!-- @github-handle --> |

## Descrição do Conflito

<!-- O que cada time está tentando fazer com este componente? -->

**Este time está modificando:** <!-- descreva as mudanças -->
**O outro time está modificando:** <!-- descreva as mudanças, se souber -->

## Evidência

```
Cole aqui o erro do Flosum ou do sf CLI que evidencia o conflito
```

## Verificação de Ownership

- [ ] Componente está em `knowledge-base/metadata-ownership.yaml`
- [ ] Ownership é: `exclusive` / `shared` / `out_of_scope`
- [ ] Script `check-shared-components.py` executado — resultado: ___

## Proposta de Resolução

- [ ] Coordenar modificações com o time B via `#sf-devops`
- [ ] Um time cede a mudança (aguardar a promoção do outro time)
- [ ] Criar componente separado para cada domínio
- [ ] Escalar para Tech Lead / Arquiteto

## Plano de Coordenação

<!-- Detalhe o que cada time vai fazer e em que ordem -->

1. 
2. 
3. 

## Aprovações Necessárias

- [ ] @<!-- co-owner-time-a --> — Aprovado
- [ ] @<!-- co-owner-time-b --> — Aprovado
- [ ] Tech Lead — Aprovado (se necessário)
