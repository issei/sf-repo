#!/usr/bin/env bash
# ==============================================================================
# 01_setup_env.sh — Setup de ferramentas para o Devin e para desenvolvedores
#
# O que este script FAZ:
#   - Instala Node.js LTS (via nvm, se necessário)
#   - Instala Salesforce CLI (@salesforce/cli)
#   - Instala Flosum CLI (@flosum/cli) — nativo, sem plugin intermediário
#   - Instala plugins obrigatórios (Code Analyzer, SGD)
#   - Instala dependências Python dos scripts de validação
#
# O que este script NÃO FAZ:
#   - Não autentica em nenhuma org (veja instrução abaixo)
#   - Não faz deploy de nada
#   - Não modifica código-fonte
#
# Após rodar este script:
#   → Desenvolvedor local: execute `sf org login web --alias sandbox-dev`
#   → Devin autônomo: execute `bash scripts/environment/authenticate-orgs.sh`
# ==============================================================================

set -euo pipefail

# ── Funções utilitárias ───────────────────────────────────────────────────────

log()   { echo -e "\n[SETUP] ▸ $1"; }
ok()    { echo -e "[SETUP] ✅ $1"; }
warn()  { echo -e "[SETUP] ⚠️  $1"; }
fail()  { echo -e "[SETUP] ❌ $1"; exit 1; }

trap 'fail "Erro inesperado na linha $LINENO. Verifique a saída acima."' ERR

log "Iniciando setup do ambiente Salesforce DevOps..."
log "Sistema operacional: $(uname -s) $(uname -m)"

# ── 1. Node.js via nvm ────────────────────────────────────────────────────────

log "Verificando Node.js..."

if ! command -v node &>/dev/null; then
  log "Node.js não encontrado. Instalando via nvm..."
  if ! command -v nvm &>/dev/null && [[ ! -f "$HOME/.nvm/nvm.sh" ]]; then
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
  fi
  export NVM_DIR="${HOME}/.nvm"
  # shellcheck source=/dev/null
  source "${NVM_DIR}/nvm.sh"
  nvm install 24
  nvm use 24
  nvm alias default 24
else
  NODE_VERSION=$(node --version | grep -oP 'v?\K\d+' | head -1)
  if [[ "$NODE_VERSION" -lt 24 ]]; then
    warn "Node.js v$(node --version) encontrado, mas a versão mínima é v24.0.0."
    warn "Atualize com: nvm install 24 && nvm use 24"
    fail "Node.js versão insuficiente."
  fi
fi

# Verificar npm também
NPM_VERSION=$(npm --version | grep -oP '\d+' | head -1)
if [[ "$NPM_VERSION" -lt 11 ]]; then
  warn "npm v$(npm --version) encontrado, mas a versão mínima é v11.0.0."
  warn "Atualize com: npm install -g npm@latest"
  fail "npm versão insuficiente."
fi

ok "Node.js: $(node --version) | npm: $(npm --version)"

# ── 2. Salesforce CLI (@salesforce/cli) ──────────────────────────────────────

log "Verificando Salesforce CLI..."

if ! command -v sf &>/dev/null; then
  log "Instalando @salesforce/cli globalmente..."
  npm install -g @salesforce/cli
fi

SF_VERSION=$(sf --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+' | head -1 || echo "desconhecida")
ok "Salesforce CLI: v${SF_VERSION}"

# ── 3. Flosum CLI (@flosum/cli) ───────────────────────────────────────────────
#
# Usamos @flosum/cli diretamente — NÃO o plugin "flosum-sfdx-plugin".
# O @flosum/cli é o cliente nativo e oficial da Flosum para operações de
# branch, snapshot parcial e gerenciamento de pipeline.

log "Verificando Flosum CLI (@flosum/cli)..."

if ! command -v flosum &>/dev/null; then
  log "Instalando @flosum/cli globalmente..."
  npm install -g @flosum/cli
fi

FLOSUM_VERSION=$(flosum --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+' | head -1 || echo "instalado")
ok "Flosum CLI: v${FLOSUM_VERSION}"

# ── 4. Plugins do Salesforce CLI ─────────────────────────────────────────────

log "Instalando plugins obrigatórios do Salesforce CLI..."

install_plugin() {
  local plugin_name="$1"
  if sf plugins | grep -q "${plugin_name}"; then
    ok "Plugin já instalado: ${plugin_name}"
  else
    log "Instalando: ${plugin_name}..."
    echo "y" | sf plugins install "${plugin_name}" 2>&1 | tail -3
    ok "Plugin instalado: ${plugin_name}"
  fi
}

# Análise estática de código Apex e LWC (PMD, ESLint)
install_plugin "@salesforce/plugin-code-analyzer"

# SFDX Git Delta — empacotamento cirúrgico baseado em diff do Git
install_plugin "sfdx-git-delta"

# ── 5. Dependências Python ────────────────────────────────────────────────────
#
# Usadas pelos scripts de validação em scripts/validation/ e scripts/reporting/

log "Instalando dependências Python (pyyaml, python-dotenv, tabulate)..."

PIP_CMD="pip3"
if ! command -v pip3 &>/dev/null && command -v pip &>/dev/null; then
  PIP_CMD="pip"
fi

${PIP_CMD} install --quiet --upgrade pyyaml python-dotenv tabulate 2>/dev/null \
  || warn "Falha ao instalar dependências Python. Verifique se o pip está disponível."

ok "Dependências Python instaladas."

# ── 6. Configurações globais do SF CLI ───────────────────────────────────────

log "Aplicando configurações globais..."

sf config set disable-telemetry=true --global 2>/dev/null || true

# Aumenta limite de memória para lidar com metadados grandes (ex: Profiles)
export NODE_OPTIONS="${NODE_OPTIONS:---max-old-space-size=8192}"

ok "Configurações aplicadas."

# ── 7. Resumo e próximos passos ───────────────────────────────────────────────

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  ✅  Setup concluído com sucesso!"
echo ""
echo "  Plugins SF CLI instalados:"
sf plugins 2>/dev/null | sed 's/^/    /'
echo ""
echo "  Próximo passo — Autenticação:"
echo ""
echo "  → Desenvolvedor local (abre o navegador):"
echo "    sf org login web --alias sandbox-dev \\"
echo "      --instance-url https://test.salesforce.com"
echo "    flosum auth login --url \$FLOSUM_ORG_URL"
echo ""
echo "  → Devin autônomo (JWT headless — requer Secrets configurados):"
echo "    bash scripts/environment/authenticate-orgs.sh"
echo "════════════════════════════════════════════════════════════"
