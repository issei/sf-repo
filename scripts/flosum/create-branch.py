#!/usr/bin/env python3
"""
create-branch.py — Cria branch no Flosum vinculada ao commit GitHub.
Uso: python create-branch.py --name devin/JIRA-123 --commit-sha abc123 [--pr-number 42]
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from flosum_api import FlosumClient


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True, help="Nome do branch no Flosum")
    parser.add_argument("--pipeline-id", default="", help="ID do pipeline (sobrescreve env var)")
    parser.add_argument("--commit-sha", default="", help="SHA do commit GitHub")
    parser.add_argument("--pr-number", default="", help="Número do PR no GitHub")
    parser.add_argument("--priority", default="normal", choices=["normal", "high"])
    args = parser.parse_args()

    if args.pipeline_id:
        os.environ["FLOSUM_PIPELINE_ID"] = args.pipeline_id

    client = FlosumClient()

    print(f"🌿 Criando branch no Flosum: {args.name}")
    result = client.create_branch(
        name=args.name,
        commit_sha=args.commit_sha,
        pr_number=args.pr_number,
        priority=args.priority,
    )

    branch_id = result.get("id", "")
    print(f"✅ Branch criado com sucesso.")
    print(f"   ID: {branch_id}")
    print(f"   Nome: {args.name}")

    # Exportar para uso em scripts subsequentes
    print(f"\nFLOSUM_BRANCH_ID={branch_id}")


if __name__ == "__main__":
    main()
