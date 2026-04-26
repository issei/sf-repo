---
name: Devin Failure Report
about: Reportar falha ocorrida durante execução autônoma do Devin
title: '[FALHA] <tipo>: <descrição curta>'
labels: devin-failure, needs-triage
assignees: ''
---

## Resumo da Falha

<!-- Descreva o que o Devin estava tentando fazer quando a falha ocorreu -->

## Tipo de Falha

- [ ] `sf_cli` — Salesforce CLI retornou erro
- [ ] `flosum_api` — API do Flosum retornou 4xx/5xx
- [ ] `validation` — Script de validação detectou violação
- [ ] `auth` — Falha de autenticação JWT
- [ ] `git` — Operação Git falhou
- [ ] `unknown` — Tipo não identificado

## Contexto

**Branch GitHub:** <!-- nome do branch onde ocorreu -->
**Branch Flosum:** <!-- ID/nome do branch no Flosum, se aplicável -->
**Commit:** <!-- SHA do commit relevante -->
**Timestamp (UTC):** <!-- YYYY-MM-DD HH:MM:SS -->

## Código/Mensagem de Erro

```
Cole aqui o output completo do erro
```

## Comando que Falhou

```bash
# Cole aqui o comando exato executado
```

## Arquivo de Log

<!-- Link para o arquivo JSON em logs/failures/ -->
- [ ] Log criado em: `logs/failures/`

## Impacto

- [ ] Tarefa bloqueada (sem impacto em orgs)
- [ ] Validação falhou na org QA
- [ ] Promoção falhou (ambiente: ___)
- [ ] Deploy em produção afetado

## Resolução Proposta

<!-- Descreva a solução ou workaround identificado -->

## Referência

<!-- Link para known-issues.md se for problema recorrente -->
- Relacionado ao KI: <!-- KI-XXX -->
