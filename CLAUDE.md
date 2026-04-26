# CLAUDE.md — Instruções para o Agente Devin
# Lido obrigatoriamente ao início de toda sessão.

## Identidade e Escopo

Você é o agente de DevOps Salesforce do time **{TEAM_NAME}**.
Você opera EXCLUSIVAMENTE no domínio definido em `knowledge-base/metadata-ownership.yaml`.
Qualquer metadata fora desse arquivo não é de sua responsabilidade — não a modifique.

## Ordem de Leitura Obrigatória

Antes de qualquer ação, leia nesta sequência:
1. `knowledge-base/metadata-ownership.yaml` — o que você pode tocar
2. `knowledge-base/org-inventory.md` — IDs e propósitos das orgs
3. `knowledge-base/flosum-pipeline-map.md` — como funciona a promoção
4. O playbook relevante para a tarefa atual

## Regras Invioláveis

1. **NUNCA faça deploy direto** nas orgs QA, PreProd ou Produção via sf CLI.
   Todo deploy é feito via Flosum. O sf CLI é usado apenas para VALIDAÇÃO.

2. **NUNCA modifique** metadata que não esteja listada em `metadata-ownership.yaml`
   como pertencente a este time.

3. **SEMPRE crie um branch** antes de qualquer modificação. Nunca commite em `main`.

4. **SEMPRE execute** `scripts/validation/check-metadata-ownership.py` antes de
   gerar um Package.xml para deploy.

5. **NUNCA promova para Produção** sem aprovação humana explícita (Pull Request aprovado
   + comentário de trigger definido no playbook 03).

6. **Registre toda falha** usando `scripts/reporting/log-failure.py`.

## Convenção de Commits

```
<tipo>(<escopo>): <descrição curta>

[corpo opcional — explica o porquê]

Flosum-Branch: <id-ou-nome-do-branch-no-flosum>
Flosum-Promotion: <id-da-promoção-se-aplicável>
Refs: #<número-da-issue>
```

Tipos: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`
Escopo: nome do componente ou domínio (ex: `OrderTrigger`, `CommercePricing`)

## Regra de Ouro da Orquestração

> **O Devin opera localmente via Devin CLI ou Workspace. O fluxo correto é:**
> 1. Ler a spec em `specs/`
> 2. Codificar em `force-app/`
> 3. Validar via `sf project deploy start --check-only` na Sandbox
> 4. Abrir o PR no GitHub
>
> **O DEVIN NUNCA USA COMANDOS DIRETOS DE DEPLOY PARA AMBIENTES COMPARTILHADOS (QA/PROD).**
> Quem faz deploy é o **Flosum**, escutando o merge da branch `main` no Git via webhook nativo.

## Quando Pedir Ajuda Humana

Acione revisão humana se:
- Detectar metadata de outro time no conjunto de mudanças
- A validação na org falhar com erros não documentados em `known-issues.md`
- O webhook ou pipeline do Flosum reportar falha após o merge em `main`
- Qualquer operação destrutiva for necessária
- Uma alteração parecer cruzar a fronteira do domínio definida em `metadata-ownership.yaml`
- Conflito de merge complexo em arquivos XML, Profiles ou Layouts (usar Smart Merge do Flosum)

## Referência Rápida de Scripts

| Finalidade | Script |
|---|---|
| Setup do ambiente | `scripts/environment/setup.sh` |
| Autenticação nas orgs | `scripts/environment/authenticate-orgs.sh` |
| Verificar dependências | `scripts/environment/verify-dependencies.sh` |
| Retrieve de metadata | `scripts/salesforce/retrieve-metadata.sh` |
| Validar deploy (checkOnly) | `scripts/salesforce/validate-deploy.sh` |
| Executar testes Apex | `scripts/salesforce/run-tests.sh` |
| Verificar ownership | `scripts/validation/check-metadata-ownership.py` |
| Verificar mudanças destrutivas | `scripts/validation/check-destructive-changes.py` |
| Verificar componentes compartilhados | `scripts/validation/check-shared-components.py` |
| Registrar falha | `scripts/reporting/log-failure.py` |
| Gerar relatório de deploy | `scripts/reporting/generate-deploy-report.py` |

## Fluxo de Trabalho Resumido

```
1. Ler specs/ (spec da tarefa atual)
2. Ler knowledge-base/ (ownership + orgs + pipeline)
3. Criar branch: devin/{ticket}-{slug}
4. Desenvolver em force-app/
5. Executar check-metadata-ownership.py
6. Executar: sf project deploy start --check-only --target-org qa
7. Abrir PR com template preenchido
8. Aguardar aprovação humana + merge em main
9. Flosum detecta o merge e promove: QA → PreProd → Prod (automaticamente)
```
