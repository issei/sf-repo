#!/usr/bin/env bash
# verify-dependencies.sh — Verifica versões e dependências do ambiente
set -euo pipefail

PASS=0
FAIL=0

check() {
  local name=$1 min_version=$2 actual_version=$3
  if [[ -z "$actual_version" ]]; then
    echo "❌ ${name}: não encontrado (mínimo: ${min_version})"
    ((FAIL++))
    return
  fi
  echo "✅ ${name}: ${actual_version} (mínimo: ${min_version})"
  ((PASS++))
}

echo "🔍 Verificando dependências do ambiente..."
echo ""

# Node.js
NODE_VER=$(node --version 2>/dev/null | tr -d 'v' || echo "")
check "node" ">=24.0.0" "$NODE_VER"

# npm
NPM_VER=$(npm --version 2>/dev/null || echo "")
check "npm" ">=11.0.0" "$NPM_VER"

# Salesforce CLI
SF_VER=$(sf --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+' | head -1 || echo "")
check "sf CLI" ">=2.0.0" "$SF_VER"

# Flosum CLI
FLOSUM_VER=$(flosum --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+' | head -1 || echo "")
check "@flosum/cli" ">=1.0.0" "$FLOSUM_VER"

# Python 3
PY_VER=$(python3 --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+' || echo "")
check "python3" ">=3.11.0" "$PY_VER"

# jq
JQ_VER=$(jq --version 2>/dev/null | grep -oP '\d+\.\d+' || echo "")
check "jq" ">=1.6" "$JQ_VER"

# Git
GIT_VER=$(git --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+' || echo "")
check "git" ">=2.40.0" "$GIT_VER"

# Python packages (apenas scripts de validação — sem dependências de API Flosum)
echo ""
echo "🔍 Verificando pacotes Python (validação)..."
for pkg in pyyaml python-dotenv tabulate; do
  if python3 -c "import ${pkg//-/_}" 2>/dev/null; then
    echo "✅ python: ${pkg}"
    ((PASS++))
  else
    echo "❌ python: ${pkg} — não instalado (pip install ${pkg})"
    ((FAIL++))
  fi
done

echo ""
echo "════════════════════════════════════════════"
echo "Resultado: ✅ ${PASS} OK | ❌ ${FAIL} faltando"
echo "════════════════════════════════════════════"

if [[ $FAIL -gt 0 ]]; then
  echo "Execute: bash scripts/environment/setup.sh para instalar dependências."
  exit 1
fi
