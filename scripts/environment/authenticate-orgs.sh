#!/usr/bin/env bash
# authenticate-orgs.sh — Autenticação nas orgs Salesforce via JWT
# Executar quando as sessões expirarem ou credenciais forem rotacionadas.
set -euo pipefail

ORGS=("qa" "preprod" "prod")

log() { echo -e "\n[AUTH] 🔑 $1"; }
error() { echo -e "\n[AUTH] ❌ $1"; exit 1; }

cleanup() {
  for alias in "${ORGS[@]}"; do
    rm -f "/tmp/jwt_key_${alias}.pem"
  done
}
trap cleanup EXIT

authenticate_org() {
  local alias=$1
  local client_id_var="SF_CLIENT_ID_${alias^^}"
  local jwt_key_var="SF_JWT_KEY_${alias^^}"
  local username_var="SF_USERNAME_${alias^^}"
  local instance_url_var="SF_INSTANCE_URL_${alias^^}"

  [[ -z "${!client_id_var:-}" ]] && error "Variável ${client_id_var} não definida"
  [[ -z "${!jwt_key_var:-}" ]]   && error "Variável ${jwt_key_var} não definida"
  [[ -z "${!username_var:-}" ]]  && error "Variável ${username_var} não definida"

  local default_url="https://test.salesforce.com"
  [[ "$alias" == "prod" ]] && default_url="https://login.salesforce.com"
  local instance_url="${!instance_url_var:-$default_url}"

  log "Autenticando: ${alias} (${!username_var})..."
  echo "${!jwt_key_var}" | base64 -d > "/tmp/jwt_key_${alias}.pem"
  chmod 600 "/tmp/jwt_key_${alias}.pem"

  sf org login jwt \
    --client-id "${!client_id_var}" \
    --jwt-key-file "/tmp/jwt_key_${alias}.pem" \
    --username "${!username_var}" \
    --instance-url "${instance_url}" \
    --alias "${alias}" \
    --set-default-dev-hub false

  log "✅ ${alias} autenticada com sucesso."
}

log "Iniciando autenticação nas orgs Salesforce..."

for org in "${ORGS[@]}"; do
  authenticate_org "$org"
done

log "Verificando status das orgs..."
sf org list

echo ""
echo "════════════════════════════════════"
echo "✅ Todas as orgs autenticadas."
echo "════════════════════════════════════"
