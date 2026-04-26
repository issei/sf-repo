# Playbook 02 — Desenvolver e Validar

**Quando usar:** Durante o ciclo de desenvolvimento após recuperar o estado da org.

**Pré-requisitos:** Branch criado (Playbook 01 concluído).

---

## Fase 1: Desenvolvimento

### 1.1 Verificar ownership antes de criar/modificar qualquer componente

```bash
python3 scripts/validation/check-metadata-ownership.py --validate-config
```

Confirmar que o componente que será criado/modificado está em `knowledge-base/metadata-ownership.yaml`.

### 1.2 Implementar mudanças em `force-app/`

- Classes Apex: `force-app/main/default/classes/`
- Triggers: `force-app/main/default/triggers/`
- LWC: `force-app/main/default/lwc/`
- Flows: `force-app/main/default/flows/`
- Objetos: `force-app/main/default/objects/`

🛑 **PARADA HUMANA OBRIGATÓRIA:** Se precisar modificar um componente não listado
em `metadata-ownership.yaml`, interrompa e solicite aprovação humana.

### 1.3 Atualizar manifests

Adicionar os componentes modificados ao `manifests/package-deploy.xml`.
Se houver deleções, adicionar ao `manifests/destructiveChanges.xml`.

---

## Fase 2: Validação de Ownership

```bash
python3 scripts/validation/check-metadata-ownership.py \
  --manifest manifests/package-deploy.xml \
  --ownership knowledge-base/metadata-ownership.yaml \
  --fail-on-violation
```

Se houver violações: remover os componentes problemáticos do package-deploy.xml antes de continuar.

### 2.1 Verificar mudanças destrutivas (se aplicável)

```bash
python3 scripts/validation/check-destructive-changes.py \
  --destructive-manifest manifests/destructiveChanges.xml
```

🛑 **PARADA HUMANA OBRIGATÓRIA:** Qualquer deleção de metadata requer aprovação humana.

### 2.2 Verificar componentes compartilhados

```bash
python3 scripts/validation/check-shared-components.py \
  --manifest manifests/package-deploy.xml \
  --ownership knowledge-base/metadata-ownership.yaml
```

---

## Fase 3: Testes e Validação na Org

### 3.1 Validar deploy (checkOnly) na org QA

```bash
bash scripts/salesforce/validate-deploy.sh qa manifests/package-deploy.xml
```

O script executa `sf project deploy validate` com `--check-only`. Não faz deploy real.

### 3.2 Executar testes Apex

```bash
bash scripts/salesforce/run-tests.sh qa
```

Meta de cobertura:
- Classes existentes: ≥ 75%
- Classes novas: ≥ 85%

**Regra de auto-correção:** Se cobertura insuficiente ou testes falharem, corrija sem pedir ajuda humana. Analise o log, corrija, re-execute.

---

## Fase 4: Commit e PR

### 4.1 Revisar mudanças finais

```bash
git status
git diff --stat
```

Confirmar que nenhum arquivo indesejado está incluído (ex: Profiles de outros times).

### 4.2 Commit estruturado

```bash
git add force-app/ manifests/
git commit -m "feat(scope): descrição curta

Explica o porquê da mudança.

Flosum-Branch: <nome-do-branch-no-flosum>
Refs: #JIRA-XXX"
```

### 4.3 Push e abertura de PR

```bash
git push origin devin/JIRA-XXX-descricao-curta
```

Abrir PR usando o template em `.github/PULL_REQUEST_TEMPLATE.md`.
Preencher todos os campos, especialmente o checklist de segurança.

---

## Verificação Final

- [ ] Ownership verificado sem violações
- [ ] Mudanças destrutivas aprovadas por humano (se houver)
- [ ] Componentes compartilhados sem conflitos
- [ ] Validação checkOnly na org QA — sucesso
- [ ] Testes Apex — cobertura ≥ mínimo exigido
- [ ] PR aberto com template preenchido

**Próximo passo:** [03-promote-via-flosum.md](03-promote-via-flosum.md) (após aprovação do PR)
