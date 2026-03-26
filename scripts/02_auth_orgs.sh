#!/bin/bash

# ==============================================================================
# Script: 02_auth_orgs.sh
# Objetivo: Autenticar o Devin de forma autônoma nas Orgs Salesforce via JWT
# Autor: Arquitetura de IA / DevOps
# ==============================================================================

# Habilita o "Fail-Fast" e rastreamento de falhas em pipes
set -e
set -o pipefail

# Constantes e Definições de Alias
ALIAS_QA="org-qa"

# ==============================================================================
# Funções Utilitárias e de Tratamento de Erro
# ==============================================================================

log() {
    echo -e "\n[DEVIN AUTH] 🔑 $1"
}

# Função de limpeza: Garante que a chave privada nunca fique sobrando no disco,
# mesmo se o script falhar no meio da execução.
cleanup() {
    if [ -f "server.key" ]; then
        rm -f server.key
        log "Lixeira de segurança: Certificado temporário 'server.key' removido do disco."
    fi
}

error_handler() {
    echo -e "\n[DEVIN AUTH] ❌ ERRO CRÍTICO na linha $1. Abortando autenticação."
    cleanup
    exit 1
}

# Associa o error_handler aos erros e a limpeza ao encerramento do script
trap 'error_handler $LINENO' ERR
trap cleanup EXIT

# ==============================================================================
# 1. Validação de Dependências (Secrets)
# ==============================================================================

log "Verificando variáveis de ambiente (Secrets)..."

# O Devin deve ter essas variáveis configuradas no painel de Secrets da Cognition
REQUIRED_VARS=("SF_CLIENT_ID" "SF_USERNAME_QA" "SF_JWT_KEY_BASE64")

for VAR in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!VAR}" ]; then
        echo "[DEVIN AUTH] ❌ Variável de ambiente $VAR não está definida."
        echo "Por favor, adicione $VAR no Secrets Manager do Devin."
        exit 1
    fi
done

log "Variáveis validadas com sucesso."

# ==============================================================================
# 2. Reconstrução Segura do Certificado
# ==============================================================================
# Chaves privadas RSA (.key) têm quebras de linha que costumam quebrar quando
# injetadas diretamente como variáveis de ambiente. Por isso, armazenamos em Base64.

log "Decodificando certificado JWT a partir da variável em Base64..."
echo "$SF_JWT_KEY_BASE64" | base64 --decode > server.key

# Aplica permissões restritas ao arquivo da chave (exigência de segurança padrão)
chmod 600 server.key

# ==============================================================================
# 3. Autenticação na Salesforce (Headless)
# ==============================================================================

log "Iniciando fluxo OAuth JWT para o usuário: $SF_USERNAME_QA..."

# Executa o login usando o Salesforce CLI
sf org login jwt \
    --client-id "$SF_CLIENT_ID" \
    --jwt-key-file server.key \
    --username "$SF_USERNAME_QA" \
    --alias "$ALIAS_QA" \
    --set-default \
    --instance-url "https://test.salesforce.com" # Altere para login.salesforce.com se for prod

# ==============================================================================
# 4. Validação do Estado da Org
# ==============================================================================

log "Validando a conexão e os limites da Org de QA..."
# Mostra ao Devin que a org foi conectada corretamente. 
# O output deste comando ajudará o agente a entender contra qual ambiente ele está trabalhando.
sf org display --target-org "$ALIAS_QA"

log "Autenticação concluída com sucesso! O ambiente de QA está pronto para extração/validação via Flosum CLI."
exit 0