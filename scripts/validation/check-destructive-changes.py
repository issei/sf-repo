#!/usr/bin/env python3
"""
check-destructive-changes.py — Detecta deleções e exige confirmação humana.
Uso: python check-destructive-changes.py --destructive-manifest manifests/destructiveChanges.xml
"""

import argparse
import os
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


def parse_destructive_manifest(path: str) -> list[tuple[str, str]]:
    if not Path(path).exists():
        return []
    tree = ET.parse(path)
    root = tree.getroot()
    ns = {"sf": "http://soap.sforce.com/2006/04/metadata"}
    deletions = []
    for mtype_el in root.findall("sf:types", ns):
        name_el = mtype_el.find("sf:name", ns)
        members = mtype_el.findall("sf:members", ns)
        if name_el is not None and name_el.text:
            for m in members:
                if m.text and m.text != "*":
                    deletions.append((name_el.text, m.text))
    return deletions


def check_github_label(required_label: str) -> bool:
    """Verifica se o PR tem o label exigido (via env var do GitHub Actions)."""
    labels_env = os.environ.get("PR_LABELS", "")
    return required_label in labels_env


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destructive-manifest",
                        default="manifests/destructiveChanges.xml")
    parser.add_argument("--require-human-label", default="approved-destructive",
                        help="Label GitHub necessário para aprovar mudanças destrutivas")
    args = parser.parse_args()

    deletions = parse_destructive_manifest(args.destructive_manifest)

    if not deletions:
        print("✅ Nenhuma mudança destrutiva detectada.")
        return

    print(f"⚠️  {len(deletions)} deleção(ões) detectada(s):")
    for mtype, name in deletions:
        print(f"   🗑  {mtype}: {name}")

    has_label = check_github_label(args.require_human_label)
    if not has_label:
        print(f"\n❌ Mudanças destrutivas requerem aprovação humana explícita.")
        print(f"   Adicione o label '{args.require_human_label}' ao Pull Request.")
        print(f"   Consulte o Playbook 02 para o procedimento correto.")
        sys.exit(1)

    print(f"\n✅ Label '{args.require_human_label}' presente. Mudanças destrutivas aprovadas.")


if __name__ == "__main__":
    main()
