# Playbook 00 — Setup do Ambiente

**Quando usar:** Primeira execução do Devin neste repositório, ou após reset do ambiente.

**Pré-requisitos:** Variáveis de ambiente configuradas conforme `.env.example`.

---

## Passo 1: Verificar dependências

```bash
bash scripts/environment/verify-dependencies.sh
```

Saída esperada: todas as ferramentas com ✅. Se houver ❌, prosseguir para o Passo 2.

## Passo 2: Bootstrap completo do ambiente

```bash
bash scripts/environment/setup.sh
```

Este script irá:
- Verificar variáveis de ambiente obrigatórias
- Instalar/verificar Node.js e sf CLI
- Instalar dependências Python
- Autenticar nas orgs QA, PreProd e Prod via JWT
- Verificar conectividade com a API do Flosum
- Validar o arquivo `metadata-ownership.yaml`

## Passo 3: Verificar autenticação

```bash
sf org list
```

Saída esperada: orgs `qa`, `preprod` e `prod` listadas com status `Connected`.

## Passo 4: Verificar conectividade com Flosum

```bash
python3 scripts/flosum/flosum_api.py --check-connectivity
```

Saída esperada: `✅ Flosum API acessível (HTTP 200)`.

## Passo 5: Confirmar ownership

```bash
python3 scripts/validation/check-metadata-ownership.py --validate-config
```

Saída esperada: `✅ Arquivo de ownership válido`.

## Passo 6: Ler instruções primárias

Ler obrigatoriamente, nesta ordem:
1. `CLAUDE.md`
2. `knowledge-base/metadata-ownership.yaml`
3. `knowledge-base/org-inventory.md`
4. `knowledge-base/flosum-pipeline-map.md`

---

## Verificação Final

- [ ] `verify-dependencies.sh` — sem erros
- [ ] `setup.sh` — concluído com sucesso
- [ ] `sf org list` — 3 orgs autenticadas
- [ ] Flosum API — 200 OK
- [ ] ownership YAML — válido
- [ ] Documentação lida

**Próximo passo:** [01-retrieve-org-state.md](01-retrieve-org-state.md)
