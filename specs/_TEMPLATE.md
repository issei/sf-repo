# Spec: [Título da Funcionalidade]

> **Instrução:** Copie este template para um novo arquivo em `specs/` com o nome
> `<TICKET>-<slug>.md` (ex: `SN-12345-order-trigger-refactor.md`) antes de iniciar.
> Preencha todas as seções obrigatórias. O Devin não deve iniciar código sem uma spec completa.

---

## Contexto de Negócio

> Descreva o problema de negócio que esta mudança resolve. Por que ela é necessária?
> Qual o impacto esperado para o usuário final ou para o processo?

[Preencher]

---

## Work Item (História ServiceNow)

| Campo | Valor |
|---|---|
| **Número do Ticket** | SN-XXXXX |
| **Título** | [Título da história] |
| **Prioridade** | Alta / Média / Baixa |
| **Solicitante** | [Nome / Time] |
| **Data de entrega** | YYYY-MM-DD |
| **Link** | [URL do ticket no ServiceNow] |

---

## Escopo de Ownership (Owner / Equipe)

| Campo | Valor |
|---|---|
| **Time responsável** | [Nome do time, ex: commerce] |
| **Devin responsável** | [Alias ou identificador] |
| **Revisor humano** | [Nome do Tech Lead ou reviewer] |
| **Co-owners afetados** | [Outros times que precisam ser notificados] |

> Confirme que todos os metadados no escopo estão listados em
> `knowledge-base/metadata-ownership.yaml` como pertencentes a este time.

---

## Matriz de Impacto (Objetos e Metadados Afetados)

| Tipo de Metadata | Nome do Componente | Ação | Owner |
|---|---|---|---|
| ApexClass | `NomeClasse` | Criar / Modificar / Deletar | commerce |
| LWC | `nomeComponente` | Criar / Modificar | commerce |
| CustomObject | `Objeto__c` | Modificar campo | commerce |
| Flow | `NomeFlow` | Modificar | [time] |

> Liste TODOS os componentes que serão alterados. Para componentes compartilhados,
> consulte `knowledge-base/metadata-ownership.yaml` e notifique os co-owners antes de modificar.

---

## Critérios de Aceite (Checklist)

### Funcionais
- [ ] [Critério 1 — comportamento esperado pelo usuário]
- [ ] [Critério 2 — regra de negócio atendida]
- [ ] [Critério 3 — caso de borda tratado]

### Técnicos
- [ ] Cobertura de testes Apex ≥ 85% nos componentes modificados
- [ ] Zero erros de lint (`@salesforce/plugin-code-analyzer`)
- [ ] Validação `checkOnly` passou na org QA sem erros
- [ ] `check-metadata-ownership.py` retornou sem violações
- [ ] `check-destructive-changes.py` executado (se aplicável)
- [ ] PR aberto com template preenchido e revisão solicitada

---

## Instruções de Execução para o Devin CLI

> Passos sequenciais que o Devin deve seguir para implementar esta spec.
> Seja específico — inclua nomes de arquivos, comandos exatos e variáveis de ambiente.

### Pré-condições
- [ ] Ambiente configurado: `bash scripts/environment/setup.sh`
- [ ] Orgs autenticadas: `bash scripts/environment/authenticate-orgs.sh`
- [ ] Branch criado: `git checkout -b devin/SN-XXXXX-<slug>`

### Passos de Implementação

1. **[Passo 1]**: [Descrição do que fazer]
   ```bash
   # comando ou ação
   ```

2. **[Passo 2]**: [Descrição do que fazer]
   ```bash
   # comando ou ação
   ```

3. **Validar ownership**:
   ```bash
   python3 scripts/validation/check-metadata-ownership.py
   ```

4. **Validar deploy (checkOnly)**:
   ```bash
   sf project deploy start \
     --check-only \
     --source-dir force-app \
     --target-org qa \
     --test-level RunLocalTests
   ```

5. **Executar testes Apex**:
   ```bash
   bash scripts/salesforce/run-tests.sh
   ```

6. **Abrir Pull Request**:
   ```bash
   gh pr create \
     --title "feat(SN-XXXXX): [Título curto]" \
     --body-file .github/PULL_REQUEST_TEMPLATE.md \
     --base main
   ```

> Após o merge do PR em `main`, o webhook nativo do Flosum assume a promoção
> automaticamente: QA → PreProd → Prod (com aprovação humana para Prod).
> O Devin não executa nenhum comando adicional de deploy.
