#!/usr/bin/env python3
"""
compare-org-state.py — Compara estado local vs org remota.
Uso: python compare-org-state.py --org qa --manifest manifests/package-retrieve.xml
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


def parse_manifest(manifest_path: str) -> dict[str, list[str]]:
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    ns = {"sf": "http://soap.sforce.com/2006/04/metadata"}
    components: dict[str, list[str]] = {}
    for member in root.findall("sf:types", ns):
        mtype = member.find("sf:name", ns)
        mnames = member.findall("sf:members", ns)
        if mtype is not None:
            components[mtype.text] = [m.text for m in mnames if m.text]
    return components


def get_org_components(org_alias: str, metadata_type: str) -> list[str]:
    try:
        result = subprocess.run(
            ["sf", "org", "list", "metadata",
             "--metadata-type", metadata_type,
             "--target-org", org_alias,
             "--json"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            return []
        data = json.loads(result.stdout)
        return [item.get("fullName", "") for item in data.get("result", [])]
    except Exception:
        return []


def compare(org_alias: str, manifest_path: str):
    print(f"🔍 Comparando estado local vs org '{org_alias}'...")
    print(f"   Manifest: {manifest_path}\n")

    components = parse_manifest(manifest_path)
    diffs = []

    for mtype, names in components.items():
        org_names = set(get_org_components(org_alias, mtype))
        local_names = set(names) - {"*"}

        only_local = local_names - org_names
        only_org = org_names - local_names

        if only_local:
            for name in only_local:
                diffs.append(("local only", mtype, name))
        if only_org:
            for name in only_org:
                diffs.append(("org only", mtype, name))

    if not diffs:
        print("✅ Estado local e org sincronizados. Nenhuma diferença encontrada.")
        return

    print(f"⚠️  {len(diffs)} diferença(s) encontrada(s):\n")
    print(f"{'Status':<15} {'Tipo':<30} {'Nome'}")
    print("-" * 75)
    for status, mtype, name in sorted(diffs):
        icon = "→ local" if status == "local only" else "← org"
        print(f"{icon:<15} {mtype:<30} {name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--org", required=True, help="Alias da org Salesforce")
    parser.add_argument("--manifest", required=True, help="Caminho do package.xml")
    args = parser.parse_args()

    if not Path(args.manifest).exists():
        print(f"❌ Manifest não encontrado: {args.manifest}")
        sys.exit(1)

    compare(args.org, args.manifest)
