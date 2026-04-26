#!/usr/bin/env bash
# setup.sh — Bootstrap completo do ambiente para o Devin
# Executar uma vez ao inicializar o ambiente ou após reset.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

echo "🚀 Iniciando setup do ambiente Salesforce DevOps..."

# ── 1. Verificar variáveis de ambiente obrigatórias ──────────────────────────
required_vars=(
  "SF_CLIENT_ID_QA" "SF_JWT_KEY_QA" "SF_USERNAME_QA"
  "SF_CLIENT_ID_PREPROD" "SF_JWT_KEY_PREPROD" "SF_USERNAME_PREPROD"
  "SF_CLIENT_ID_PROD" "SF_JWT_KEY_PROD" "SF_USERNAME_PROD"
  "FLOSUM_API_BASE_URL" "FLOSUM_API_TOKEN" "FLOSUM_PIPELINE_ID"
)
missing=()
for var in "${required_vars[@]}"; do
  [[ -z "${!var:-}" ]] && missing+=("$var")
done
if [[ ${#missing[@]} -gt 0 ]]; then
  echo "❌ Variáveis de ambiente ausentes: ${missing[*]}"
  echo "   Consulte .env.example para referência."
  exit 1
fi

# ── 2. Instalar/verificar Node.js ────────────────────────────────────────────
if ! command -v node &>/dev/null; then
  echo "📦 Instalando Node.js via nvm..."
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
  export NVM_DIR="$HOME/.nvm"
  # shellcheck source=/dev/null
  source "$NVM_DIR/nvm.sh"
  nvm install 20 && nvm use 20 && nvm alias default 20
fi
echo "✅ Node.js: $(node --version)"

# ── 3. Instalar/atualizar sf CLI ─────────────────────────────────────────────
if ! command -v sf &>/dev/null; then
  echo "📦 Instalando Salesforce CLI..."
  npm install -g @salesforce/cli
fi
SF_VERSION=$(sf --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+' | head -1)
echo "✅ sf CLI: ${SF_VERSION}"

sf plugins install @salesforce/plugin-packaging 2>/dev/null || true

# ── 4. Instalar dependências Python ──────────────────────────────────────────
echo "📦 Instalando dependências Python..."
pip install --quiet requests pyyaml python-dotenv tabulate 2>/dev/null || \
  pip3 install --quiet requests pyyaml python-dotenv tabulate

# ── 5. Autenticar nas orgs via JWT ───────────────────────────────────────────
authenticate_org() {
  local alias=$1 client_id=$2 jwt_key_b64=$3 username=$4 instance_url=$5
  echo "🔐 Autenticando na org: ${alias}..."
  echo "${jwt_key_b64}" | base64 -d > "/tmp/jwt_key_${alias}.pem"
  chmod 600 "/tmp/jwt_key_${alias}.pem"
  sf org login jwt \
    --client-id "${client_id}" \
    --jwt-key-file "/tmp/jwt_key_${alias}.pem" \
    --username "${username}" \
    --instance-url "${instance_url}" \
    --alias "${alias}" \
    --set-default-dev-hub false
  rm -f "/tmp/jwt_key_${alias}.pem"
  echo "✅ Org ${alias} autenticada."
}

authenticate_org "qa"      "$SF_CLIENT_ID_QA"      "$SF_JWT_KEY_QA"      \
  "$SF_USERNAME_QA"      "${SF_INSTANCE_URL_QA:-https://test.salesforce.com}"
authenticate_org "preprod" "$SF_CLIENT_ID_PREPROD" "$SF_JWT_KEY_PREPROD" \
  "$SF_USERNAME_PREPROD" "${SF_INSTANCE_URL_PREPROD:-https://test.salesforce.com}"
authenticate_org "prod"    "$SF_CLIENT_ID_PROD"    "$SF_JWT_KEY_PROD"    \
  "$SF_USERNAME_PROD"    "${SF_INSTANCE_URL_PROD:-https://login.salesforce.com}"

# ── 6. Verificar conectividade Flosum ────────────────────────────────────────
echo "🔗 Verificando conectividade com Flosum API..."
python3 "${SCRIPT_DIR}/../flosum/flosum_api.py" --check-connectivity
echo "✅ Flosum API acessível."

# ── 7. Validar arquivo de ownership ──────────────────────────────────────────
echo "📋 Validando metadata-ownership.yaml..."
python3 "${SCRIPT_DIR}/../validation/check-metadata-ownership.py" --validate-config
echo "✅ Arquivo de ownership válido."

echo ""
echo "════════════════════════════════════════════════"
echo "✅ Setup completo. Ambiente pronto para o Devin."
echo "════════════════════════════════════════════════"
