## Resumo da Mudança

<!-- Descreva O QUÊ foi feito e POR QUÊ (não como). -->

Ticket: <!-- JIRA-XXX -->
Flosum Branch: <!-- Nome/ID do branch no Flosum -->

## Tipo de Mudança

- [ ] Nova funcionalidade
- [ ] Correção de bug
- [ ] Refatoração (sem mudança de comportamento)
- [ ] Configuração / metadata
- [ ] Mudança destrutiva ⚠️

## Componentes Modificados

<!-- Liste os componentes Salesforce alterados -->

| Tipo | Nome | Ação | Ownership Verificado |
|---|---|---|---|
| ApexClass | NomeClasse | Modified | ✅ |

## Checklist de Segurança (Obrigatório)

- [ ] `check-metadata-ownership.py` executado sem erros
- [ ] `check-destructive-changes.py` executado (se houver deleções)
- [ ] `check-shared-components.py` executado sem conflitos
- [ ] Validação `sf project deploy validate` passou na org QA
- [ ] Testes Apex com cobertura ≥ 75% (classes novas ≥ 85%)
- [ ] Nenhum metadata de outro time incluído no Package.xml

## Impacto em Componentes Compartilhados

<!-- Preencher APENAS se houver mudanças em componentes de ownership compartilhado -->
- [ ] Co-owners notificados via Slack: #sf-{team}
- [ ] Aprovação dos co-owners obtida (comentar neste PR)

## Plano de Rollback

<!-- Se algo der errado após a promoção, como reverter? -->

## Notas para o Revisor

<!-- Informações adicionais, decisões técnicas, alternativas consideradas -->

---
*PR criado por: Devin Agent | Branch Flosum: `{flosum_branch_id}`*
