#!/usr/bin/env bash
# retrieve-metadata.sh — Retrieve seletivo de metadata por manifest
# Uso: bash retrieve-metadata.sh <org-alias> <manifest-path>
# Exemplo: bash retrieve-metadata.sh qa manifests/package-retrieve.xml
set -euo pipefail

ORG_ALIAS="${1:?Uso: $0 <org-alias> <manifest-path>}"
MANIFEST="${2:?Uso: $0 <org-alias> <manifest-path>}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

[[ ! -f "$MANIFEST" ]] && echo "❌ Manifest não encontrado: $MANIFEST" && exit 1

echo "📥 Iniciando retrieve de metadata..."
echo "   Org: ${ORG_ALIAS}"
echo "   Manifest: ${MANIFEST}"

sf project retrieve start \
  --manifest "${MANIFEST}" \
  --target-org "${ORG_ALIAS}" \
  --wait 10

echo ""
echo "✅ Retrieve concluído."
echo "   Verifique as mudanças com: git status"
