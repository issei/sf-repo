# Playbook 01 — Recuperar Estado Atual das Orgs

**Quando usar:** Antes de iniciar qualquer desenvolvimento — para garantir que o repositório local está sincronizado com a org.

**Pré-requisitos:** Ambiente configurado (Playbook 00 concluído).

---

## Passo 1: Atualizar branch main

```bash
git checkout main
git pull origin main
```

## Passo 2: Criar branch de trabalho

```bash
# Formato: devin/{ticket-id}-{slug-descritivo}
git checkout -b devin/JIRA-XXX-descricao-curta
```

Regras de nomenclatura:
- Prefixo obrigatório: `devin/`
- Slug: lowercase, hífens, máx 50 chars, sem acentos
- Sempre incluir o ID do ticket

## Passo 3: Retrieve do estado atual da org QA

```bash
bash scripts/salesforce/retrieve-metadata.sh qa manifests/package-retrieve.xml
```

Este script executa `sf project retrieve start` com o manifest de retrieve.

## Passo 4: Verificar delta

```bash
git status
git diff --stat
```

Analisar as diferenças entre o estado local e o que foi recuperado da org.
Se houver mudanças não esperadas, investigar antes de prosseguir.

## Passo 5: Comparar estado local vs remoto (opcional)

```bash
python3 scripts/salesforce/compare-org-state.py --org qa --manifest manifests/package-retrieve.xml
```

---

## Verificação Final

- [ ] Branch criado com prefixo `devin/`
- [ ] Retrieve concluído sem erros
- [ ] Diferenças analisadas e compreendidas
- [ ] Nenhum metadata de outro time detectado no retrieve

**Próximo passo:** [02-develop-and-validate.md](02-develop-and-validate.md)
