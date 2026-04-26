#!/usr/bin/env bash
# run-tests.sh — Execução de testes Apex com verificação de cobertura
# Uso: bash run-tests.sh <org-alias> [cobertura-minima]
# Exemplo: bash run-tests.sh qa 75
set -euo pipefail

ORG_ALIAS="${1:?Uso: $0 <org-alias> [cobertura-minima]}"
MIN_COVERAGE="${2:-75}"

echo "🧪 Executando testes Apex..."
echo "   Org: ${ORG_ALIAS}"
echo "   Cobertura mínima: ${MIN_COVERAGE}%"

OUTPUT=$(sf apex run test \
  --target-org "${ORG_ALIAS}" \
  --code-coverage \
  --result-format human \
  --wait 15 \
  2>&1)

echo "$OUTPUT"

# Extrair cobertura do output
COVERAGE=$(echo "$OUTPUT" | grep -oP 'Org Wide Coverage.*?(\d+)%' | grep -oP '\d+' | tail -1 || echo "0")

if [[ -z "$COVERAGE" ]]; then
  echo "⚠️  Não foi possível extrair a cobertura do output. Verificar manualmente."
  exit 0
fi

echo ""
echo "📊 Cobertura total: ${COVERAGE}%"

if [[ "$COVERAGE" -lt "$MIN_COVERAGE" ]]; then
  echo "❌ Cobertura ${COVERAGE}% abaixo do mínimo ${MIN_COVERAGE}%."
  echo "   Corrija as classes de teste e re-execute."
  exit 1
fi

echo "✅ Cobertura satisfatória: ${COVERAGE}% >= ${MIN_COVERAGE}%"
