# Playbook 04 — Tratar Conflitos de Metadata

**Quando usar:** Quando detectar metadata de outro time no conjunto de mudanças, ou quando a validação/promoção falhar por conflito.

---

## Identificação do Conflito

### Cenário A: `check-metadata-ownership.py` detectou metadata fora do escopo

```
VIOLATION: ApexClass 'CaseService' não pertence ao time 'commerce'
```

**Ação imediata:** Remover o componente do `package-deploy.xml` e do `force-app/`.
Nunca incluir componentes de outros times em um deploy deste repositório.

### Cenário B: Promoção Flosum falhou por conflito de merge

```
CONFLICT: Flow 'Order_Approval' já foi modificado pelo time 'service'
```

**Ação imediata:** Não tentar resolver o conflito unilateralmente.
Seguir o protocolo de coordenação abaixo.

### Cenário C: `check-shared-components.py` detectou componente compartilhado

```
WARNING: CustomApplication 'SalesConsole' é owned compartilhado com @team-sales
```

**Ação imediata:** Notificar co-owners antes de qualquer modificação.

---

## Protocolo de Coordenação

### Passo 1: Identificar o time conflitante

Consultar `knowledge-base/metadata-ownership.yaml` para identificar quem é o co-owner.
Consultar `knowledge-base/team-contacts.md` para encontrar o canal de contato.

### Passo 2: Pausar operação

NÃO prosseguir com a promoção enquanto o conflito não for resolvido.
Registrar o bloqueio:

```bash
python3 scripts/reporting/log-failure.py \
  --type validation \
  --error-code "METADATA_CONFLICT" \
  --error "Conflito detectado em <componente>" \
  --context "Promoção para <ambiente> bloqueada"
```

### Passo 3: Abrir issue de conflito

Abrir issue usando o template `.github/ISSUE_TEMPLATE/metadata-conflict.md`.
Notificar os co-owners via Slack no canal `#sf-devops`.

### Passo 4: Aguardar coordenação humana

🛑 **PARADA HUMANA OBRIGATÓRIA:** Conflitos de metadata em componentes compartilhados
requerem coordenação entre times. Não resolver sozinho.

### Passo 5: Após resolução

Quando os times chegarem a acordo:
1. Atualizar `package-deploy.xml` conforme acordado
2. Re-executar `check-shared-components.py`
3. Retomar o fluxo de promoção pelo Playbook 03

---

## Conflitos de Merge no Git

### Conflitos simples (arquivos de texto não-XML)

Se houver conflito de merge ao fazer rebase/merge em `main`:

```bash
git fetch origin main
git rebase origin/main
```

Se conflitos aparecerem em arquivos de outro time:
1. Manter a versão de `origin/main` (aceitar o incoming)
2. Nunca modificar componentes de outros times para resolver um conflito

```bash
# Aceitar a versão do main para arquivos conflitantes de outros times
git checkout origin/main -- force-app/main/default/classes/CaseService.cls
git add force-app/main/default/classes/CaseService.cls
```

### Conflitos complexos (XML, Profiles, Layouts, Permission Sets)

🛑 **Conflitos de metadados complexos (XML, Profiles, Layouts, Permission Sets) NÃO devem
ser resolvidos pelo Devin via Git Rebase ou edição manual de XML.**

Em caso de conflito nesse tipo de arquivo, o Devin deve:

1. **Alertar o revisor humano** imediatamente com o nome dos arquivos conflitantes
2. **Não tentar mesclar manualmente** arquivos XML de metadata Salesforce — a estrutura
   é frágil e uma mesclagem incorreta pode corromper silenciosamente o componente
3. **Solicitar que o conflito seja resolvido** utilizando a ferramenta **"Smart Merge"**
   na interface web do Flosum, que entende a semântica do metadata Salesforce

```
Ação correta do Devin:
  → Registrar o conflito via log-failure.py
  → Abrir issue usando .github/ISSUE_TEMPLATE/metadata-conflict.md
  → Comentar no PR: "Conflito complexo em [arquivo.xml] — requer Smart Merge no Flosum"
  → Aguardar resolução humana antes de prosseguir
```

---

## Verificação Final

- [ ] Componentes fora do escopo removidos do package-deploy.xml
- [ ] Conflito registrado em `logs/failures/`
- [ ] Issue de conflito aberta (se necessário)
- [ ] Co-owners notificados (se componente compartilhado)
- [ ] Resolução acordada com aprovação humana
