#!/usr/bin/env python3
"""
generate-deploy-report.py — Gera relatório Markdown de deploy/validação.
Salvo em: reports/deploy-{timestamp}-{environment}.md

Uso:
  python generate-deploy-report.py --environment qa --pr-number 42
  echo "$SF_OUTPUT" | python generate-deploy-report.py --environment qa
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPORTS_DIR = Path(__file__).parent.parent.parent / "reports"


def generate_report(deploy_result: dict, environment: str, pr_number: str = ""):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    filename = f"deploy-{timestamp}-{environment}.md"
    filepath = REPORTS_DIR / filename

    status = "✅ SUCESSO" if deploy_result.get("status") == "Succeeded" else "❌ FALHOU"
    components = deploy_result.get("components", [])
    failures = [c for c in components if c.get("state") == "Failed"]
    successes = [c for c in components if c.get("state") == "Succeeded"]

    lines = [
        f"# Relatório de Deploy — {environment.upper()}",
        "",
        f"**Status:** {status}  ",
        f"**Data:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC  ",
        f"**Ambiente:** {environment}  ",
        f"**PR:** {f'#{pr_number}' if pr_number else '—'}  ",
        f"**Time:** {os.environ.get('TEAM_NAME', 'unknown')}  ",
        "",
        "## Resumo",
        "",
        "| Métrica | Valor |",
        "|---|---|",
        f"| Total de componentes | {len(components)} |",
        f"| Sucesso | {len(successes)} |",
        f"| Falhou | {len(failures)} |",
        f"| Testes executados | {deploy_result.get('tests_total', 0)} |",
        f"| Cobertura de código | {deploy_result.get('code_coverage', 0):.1f}% |",
    ]

    if failures:
        lines += ["", "## Componentes com Falha", ""]
        for fail in failures:
            lines.append(
                f"- **{fail['type']}: {fail['name']}** — {fail.get('error', 'unknown error')}"
            )

    if successes:
        lines += ["", "## Componentes com Sucesso", ""]
        for s in successes[:20]:
            lines.append(f"- {s['type']}: {s['name']}")
        if len(successes) > 20:
            lines.append(f"- ... e mais {len(successes) - 20} componentes")

    with open(filepath, "w") as out:
        out.write("\n".join(lines))

    print(f"📄 Relatório gerado: reports/{filename}")
    return filepath


def parse_sf_output(raw: str) -> dict:
    try:
        data = json.loads(raw)
        return {
            "status": data.get("status", "Unknown"),
            "components": data.get("result", {}).get("details", {}).get("componentSuccesses", []),
            "tests_total": data.get("result", {}).get("numberTestsTotal", 0),
            "code_coverage": data.get("result", {}).get("details", {}).get(
                "runTestResult", {}).get("codeCoverageWarnings", []),
        }
    except json.JSONDecodeError:
        succeeded = "succeeded" in raw.lower() or "success" in raw.lower()
        return {"status": "Succeeded" if succeeded else "Failed", "components": []}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", required=True)
    parser.add_argument("--pr-number", default="")
    parser.add_argument("--result-json", default="",
                        help="JSON do resultado do sf CLI (alternativa ao stdin)")
    args = parser.parse_args()

    if args.result_json:
        raw = args.result_json
    elif not sys.stdin.isatty():
        raw = sys.stdin.read()
    else:
        raw = "{}"

    deploy_result = parse_sf_output(raw)
    generate_report(deploy_result, args.environment, args.pr_number)
