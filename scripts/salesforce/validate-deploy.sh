#!/usr/bin/env bash
# validate-deploy.sh — Validação sem deploy (checkOnly)
# Uso: bash validate-deploy.sh <org-alias> <manifest-path>
# Exemplo: bash validate-deploy.sh qa manifests/package-deploy.xml
set -euo pipefail

ORG_ALIAS="${1:?Uso: $0 <org-alias> <manifest-path>}"
MANIFEST="${2:?Uso: $0 <org-alias> <manifest-path>}"
MAX_RETRIES=3
RETRY_WAIT=300  # 5 minutos — para KI-001 (DEPLOY_IN_PROGRESS)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

[[ ! -f "$MANIFEST" ]] && echo "❌ Manifest não encontrado: $MANIFEST" && exit 1

echo "🔍 Iniciando validação (checkOnly)..."
echo "   Org: ${ORG_ALIAS}"
echo "   Manifest: ${MANIFEST}"

attempt=1
while [[ $attempt -le $MAX_RETRIES ]]; do
  echo ""
  echo "   Tentativa ${attempt}/${MAX_RETRIES}..."

  set +e
  OUTPUT=$(sf project deploy validate \
    --manifest "${MANIFEST}" \
    --target-org "${ORG_ALIAS}" \
    --wait 15 \
    --test-level RunLocalTests \
    2>&1)
  EXIT_CODE=$?
  set -e

  if [[ $EXIT_CODE -eq 0 ]]; then
    echo "✅ Validação bem-sucedida."
    echo "$OUTPUT"

    # Gerar relatório se o script existir
    if [[ -f "${REPO_ROOT}/scripts/reporting/generate-deploy-report.py" ]]; then
      echo "$OUTPUT" | python3 "${REPO_ROOT}/scripts/reporting/generate-deploy-report.py" \
        --environment "${ORG_ALIAS}" 2>/dev/null || true
    fi
    exit 0
  fi

  # KI-001: DEPLOY_IN_PROGRESS — retry automático
  if echo "$OUTPUT" | grep -q "DEPLOY_IN_PROGRESS"; then
    echo "⚠️  DEPLOY_IN_PROGRESS detectado. Aguardando ${RETRY_WAIT}s antes de retry..."
    echo "$OUTPUT"
    sleep $RETRY_WAIT
    ((attempt++))
    continue
  fi

  # Outros erros — falha imediata
  echo "❌ Validação falhou:"
  echo "$OUTPUT"

  # Registrar falha se o script existir
  if [[ -f "${REPO_ROOT}/scripts/reporting/log-failure.py" ]]; then
    python3 "${REPO_ROOT}/scripts/reporting/log-failure.py" \
      --type sf_cli \
      --error-code "VALIDATE_FAILED" \
      --error "$(echo "$OUTPUT" | tail -5)" \
      --context "validate-deploy.sh ${ORG_ALIAS}" \
      --command "sf project deploy validate --manifest ${MANIFEST} --target-org ${ORG_ALIAS}" \
      2>/dev/null || true
  fi

  exit 1
done

echo "❌ Todas as ${MAX_RETRIES} tentativas falharam por DEPLOY_IN_PROGRESS."
echo "   Consulte known-issues.md (KI-001) para próximos passos."
exit 1
