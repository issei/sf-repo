#!/usr/bin/env python3
"""
link-commit-to-branch.py — Vincula commit GitHub a branch Flosum para rastreabilidade bidirecional.

Convenção:
  GitHub → Flosum: commit message contém "Flosum-Branch: <id>"
  Flosum → GitHub: tag Git criada após promoção bem-sucedida
    formato: flosum/promoted/{ambiente}/{YYYYMMDD-HHMMSS}
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime

import requests

FLOSUM_BASE_URL = os.environ.get("FLOSUM_API_BASE_URL", "").rstrip("/")
FLOSUM_TOKEN = os.environ.get("FLOSUM_API_TOKEN", "")


def get_current_commit_sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()


def tag_promoted_commit(ambiente: str, commit_sha: str) -> str:
    """Cria tag Git após promoção bem-sucedida para rastreabilidade reversa."""
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    tag_name = f"flosum/promoted/{ambiente}/{timestamp}"
    subprocess.run([
        "git", "tag", "-a", tag_name, commit_sha,
        "-m", f"Promoted to {ambiente} via Flosum at {timestamp}"
    ], check=True)
    subprocess.run(["git", "push", "origin", tag_name], check=True)
    print(f"✅ Tag criada: {tag_name} → {commit_sha[:8]}")
    return tag_name


def update_flosum_branch_with_commit(flosum_branch_id: str, commit_sha: str, pr_url: str):
    """Atualiza o branch Flosum com metadados do commit GitHub."""
    if not FLOSUM_BASE_URL or not FLOSUM_TOKEN:
        print("❌ FLOSUM_API_BASE_URL e FLOSUM_API_TOKEN são obrigatórios.")
        sys.exit(1)

    url = f"{FLOSUM_BASE_URL}/branches/{flosum_branch_id}"
    payload = {
        "github_commit_sha": commit_sha,
        "github_pr_url": pr_url,
        "linked_at": datetime.utcnow().isoformat(),
    }
    headers = {
        "Authorization": f"Bearer {FLOSUM_TOKEN}",
        "Content-Type": "application/json",
    }
    resp = requests.patch(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    print(f"✅ Branch Flosum {flosum_branch_id} vinculado ao commit {commit_sha[:8]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--flosum-branch-id", required=True)
    parser.add_argument("--commit-sha", default="")
    parser.add_argument("--pr-url", default="")
    parser.add_argument("--tag-environment", default="",
                        help="Se fornecido, cria tag de promoção para este ambiente")
    args = parser.parse_args()

    commit_sha = args.commit_sha or get_current_commit_sha()

    update_flosum_branch_with_commit(args.flosum_branch_id, commit_sha, args.pr_url)

    if args.tag_environment:
        tag_promoted_commit(args.tag_environment, commit_sha)


if __name__ == "__main__":
    main()
