# Problemas Conhecidos e Soluções

> Consulte este arquivo ANTES de tentar operações que falharam anteriormente.
> Atualizado pelo time após cada incidente resolvido.

---

## KI-001: DEPLOY_IN_PROGRESS na org compartilhada

**Sintoma:** sf CLI retorna `DEPLOY_IN_PROGRESS` ao tentar validar na org QA.
**Causa:** Outro time está fazendo deploy simultâneo na mesma org.
**Solução:**
1. Esperar 5 minutos e tentar novamente (máx 3 tentativas)
2. Se persistir, verificar no Flosum qual pipeline está ativo
3. Notificar `#sf-devops` no Slack se bloquear por mais de 30 min
**Script:** `scripts/salesforce/validate-deploy.sh` já implementa retry automático.

---

## KI-002: INSUFFICIENT_ACCESS em Permission Set

**Sintoma:** Deploy falha com `INSUFFICIENT_ACCESS` em PermissionSet.
**Causa:** O usuário de serviço não tem permissão para modificar o Permission Set alvo.
**Solução:**
1. Verificar se o Permission Set está em `metadata-ownership.yaml` como `exclusive`
2. Se for `shared`, coordenar com co-owners antes do deploy
3. Se for `out_of_scope`, remover do Package.xml imediatamente
**Prevenção:** Sempre executar `check-metadata-ownership.py` antes de gerar Package.xml.

---

## KI-003: Flosum API retorna 401 após rotação de token

**Sintoma:** `flosum_api.py` retorna HTTP 401 após período de inatividade.
**Causa:** Token Flosum expirado ou revogado.
**Solução:**
1. Verificar se o token em `FLOSUM_API_TOKEN` está atualizado nos GitHub Secrets
2. Regenerar token na Connected App do Flosum
3. Atualizar GitHub Secret e re-executar pipeline
**Responsável:** @{TEAM_NAME}-devops-admin

---

## KI-004: JWT Authentication Failed — INVALID_GRANT

**Sintoma:** `sf org login jwt` retorna `INVALID_GRANT`.
**Causa:** Certificado JWT expirado, Connected App não configurada corretamente, ou usuário sem permissão de API.
**Solução:**
1. Verificar validade do certificado X.509 (normalmente 1-3 anos)
2. Confirmar que o Connected App tem `callback_url` configurado
3. Confirmar que o usuário tem a permissão "API Enabled"
4. Verificar que a chave em `SF_JWT_KEY_QA` está em base64 correto: `cat server.key | base64`

---

## KI-005: Flow deployment falha com "Required fields are missing"

**Sintoma:** Deploy de Flow falha com erro de campos obrigatórios.
**Causa:** Versão de API incompatível entre org e metadata local.
**Solução:**
1. Verificar a versão de API no arquivo `.flow-meta.xml` (atributo `apiVersion`)
2. Atualizar para a versão suportada pela org: `sf org display --target-org qa | grep ApiVersion`
3. Re-executar retrieve e comparar com o arquivo local

---

## KI-006: Timeout em validate-deploy para packages grandes

**Sintoma:** `validate-deploy.sh` retorna timeout após 10 minutos.
**Causa:** Package muito grande ou org com alta carga.
**Solução:**
1. Dividir o package em partes menores (máx 50 componentes conforme `.devin.yaml`)
2. Aumentar o timeout: editar `validate-deploy.sh`, parâmetro `--wait`
3. Executar em horário de menor carga (fora do horário de pico do time)
