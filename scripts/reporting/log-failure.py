#!/usr/bin/env python3
"""
log-failure.py — Persiste falhas estruturadas no repositório.
Uso: python log-failure.py --type sf_cli --error "DEPLOY_IN_PROGRESS" --context "deploy QA"

Cria um arquivo em logs/failures/YYYY-MM-DD_HHMMSS_{type}.json
e atualiza logs/failure-index.md com entrada linkada.
"""

import argparse
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
FAILURES_DIR = LOGS_DIR / "failures"
INDEX_FILE = LOGS_DIR / "failure-index.md"

FAILURE_TYPES = ["sf_cli", "flosum_api", "validation", "git", "auth", "unknown"]


def get_git_context():
    try:
        return {
            "branch": subprocess.check_output(
                ["git", "branch", "--show-current"]).decode().strip(),
            "commit": subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"]).decode().strip(),
            "author": subprocess.check_output(
                ["git", "config", "user.email"]).decode().strip(),
        }
    except Exception:
        return {}


def log_failure(failure_type: str, error_code: str, error_message: str,
                context: str, command: str = "", resolution: str = ""):
    FAILURES_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow()
    ts_str = timestamp.strftime("%Y-%m-%d_%H%M%S")
    filename = f"{ts_str}_{failure_type}.json"
    filepath = FAILURES_DIR / filename

    payload = {
        "id": f"{ts_str}_{failure_type}",
        "timestamp": timestamp.isoformat(),
        "type": failure_type,
        "error_code": error_code,
        "error_message": error_message,
        "context": context,
        "command": command,
        "resolution": resolution,
        "git": get_git_context(),
        "environment": {
            "team": os.environ.get("TEAM_NAME", "unknown"),
            "flosum_pipeline": os.environ.get("FLOSUM_PIPELINE_ID", "unknown"),
        },
    }

    with open(filepath, "w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    _update_index(payload, filename)

    print(f"✅ Falha registrada: logs/failures/{filename}")
    return filepath


def _update_index(payload: dict, filename: str):
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not INDEX_FILE.exists():
        INDEX_FILE.write_text(
            "# Índice de Falhas\n\n"
            "| Data | Tipo | Código | Contexto | Resolução | Arquivo |\n"
            "|---|---|---|---|---|---|\n"
        )

    date_str = payload["timestamp"][:10]
    row = (
        f"| {date_str} | `{payload['type']}` | `{payload['error_code']}` "
        f"| {payload['context']} | {payload['resolution'] or '—'} "
        f"| [ver](failures/{filename}) |\n"
    )
    with open(INDEX_FILE, "a") as f:
        f.write(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=FAILURE_TYPES, required=True)
    parser.add_argument("--error-code", default="UNKNOWN")
    parser.add_argument("--error", required=True, help="Mensagem de erro")
    parser.add_argument("--context", required=True, help="O que estava sendo feito")
    parser.add_argument("--command", default="", help="Comando que falhou")
    parser.add_argument("--resolution", default="", help="Como foi resolvido (preencher após)")
    args = parser.parse_args()

    log_failure(
        failure_type=args.type,
        error_code=args.error_code,
        error_message=args.error,
        context=args.context,
        command=args.command,
        resolution=args.resolution,
    )
