#!/usr/bin/env python3
"""
check-shared-components.py — Verifica impacto em componentes de ownership compartilhado.
Uso: python check-shared-components.py --manifest manifests/package-deploy.xml \
          --ownership knowledge-base/metadata-ownership.yaml
"""

import argparse
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

import yaml


def load_ownership(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def parse_manifest(path: str) -> dict[str, list[str]]:
    if not Path(path).exists():
        return {}
    tree = ET.parse(path)
    root = tree.getroot()
    ns = {"sf": "http://soap.sforce.com/2006/04/metadata"}
    components: dict[str, list[str]] = {}
    for mtype_el in root.findall("sf:types", ns):
        name_el = mtype_el.find("sf:name", ns)
        members = mtype_el.findall("sf:members", ns)
        if name_el is not None and name_el.text:
            components[name_el.text] = [m.text for m in members if m.text]
    return components


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="manifests/package-deploy.xml")
    parser.add_argument("--ownership", default="knowledge-base/metadata-ownership.yaml")
    parser.add_argument("--fail-on-shared", action="store_true",
                        help="Falhar se componentes compartilhados forem encontrados")
    args = parser.parse_args()

    ownership = load_ownership(args.ownership)
    components = parse_manifest(args.manifest)

    shared_list = ownership.get("shared", [])
    team_name = ownership.get("team", {}).get("name", "este time")

    shared_found = []
    for item in shared_list:
        mtype = item.get("metadata_type", "")
        component = item.get("component", "")
        co_owners = item.get("co_owners", [])
        note = item.get("note", "")

        if mtype in components and component in components[mtype]:
            shared_found.append({
                "type": mtype,
                "component": component,
                "co_owners": co_owners,
                "note": note,
            })

    if not shared_found:
        print("✅ Nenhum componente de ownership compartilhado no manifest.")
        return

    print(f"⚠️  {len(shared_found)} componente(s) compartilhado(s) detectado(s):\n")
    for item in shared_found:
        print(f"   📋 {item['type']}: {item['component']}")
        print(f"      Co-owners: {', '.join(item['co_owners'])}")
        if item["note"]:
            print(f"      Nota: {item['note']}")
        print()

    print("   Ação obrigatória: notificar co-owners antes de prosseguir.")
    print(f"   Consulte knowledge-base/team-contacts.md para canais de contato.")

    if args.fail_on_shared:
        sys.exit(1)


if __name__ == "__main__":
    main()
