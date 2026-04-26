#!/usr/bin/env python3
"""
check-metadata-ownership.py — Valida se metadata no manifest pertence ao time.
Uso:
  python check-metadata-ownership.py --manifest manifests/package-deploy.xml \
         --ownership knowledge-base/metadata-ownership.yaml --fail-on-violation
  python check-metadata-ownership.py --validate-config
"""

import argparse
import fnmatch
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


def is_allowed(component_name: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(component_name, p) for p in patterns)


def check_ownership(manifest_path: str, ownership_path: str, fail_on_violation: bool):
    ownership = load_ownership(ownership_path)
    components = parse_manifest(manifest_path)

    exclusive = ownership.get("exclusive", {})
    shared_list = ownership.get("shared", [])
    out_of_scope = ownership.get("out_of_scope", [])

    shared_lookup: dict[str, list[str]] = {}
    for item in shared_list:
        mtype = item.get("metadata_type", "")
        comp = item.get("component", "")
        shared_lookup.setdefault(mtype, []).append(comp)

    violations = []
    warnings = []

    for mtype, names in components.items():
        exclusive_patterns = exclusive.get(mtype, [])
        shared_patterns = shared_lookup.get(mtype, [])

        for name in names:
            if name == "*":
                continue

            if is_allowed(name, out_of_scope):
                violations.append(f"OUT_OF_SCOPE: {mtype}/{name}")
                continue

            if is_allowed(name, exclusive_patterns):
                continue

            if is_allowed(name, shared_patterns):
                warnings.append(f"SHARED: {mtype}/{name} — coordenar com co-owners")
                continue

            if exclusive_patterns:
                violations.append(f"VIOLATION: {mtype}/{name} não pertence a este time")

    if warnings:
        print("⚠️  Componentes compartilhados detectados:")
        for w in warnings:
            print(f"   {w}")

    if violations:
        print("\n❌ Violações de ownership detectadas:")
        for v in violations:
            print(f"   {v}")
        if fail_on_violation:
            sys.exit(1)
        return

    print(f"✅ Ownership verificado: {sum(len(v) for v in components.values())} componente(s) OK.")


def validate_config(ownership_path: str = "knowledge-base/metadata-ownership.yaml"):
    path = Path(ownership_path)
    if not path.exists():
        print(f"❌ Arquivo não encontrado: {ownership_path}")
        sys.exit(1)
    data = load_ownership(ownership_path)
    required = ["team", "exclusive", "out_of_scope"]
    missing = [k for k in required if k not in data]
    if missing:
        print(f"❌ Campos obrigatórios ausentes no ownership YAML: {missing}")
        sys.exit(1)
    print("✅ Arquivo de ownership válido.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="manifests/package-deploy.xml")
    parser.add_argument("--ownership", default="knowledge-base/metadata-ownership.yaml")
    parser.add_argument("--fail-on-violation", action="store_true")
    parser.add_argument("--validate-config", action="store_true")
    args = parser.parse_args()

    if args.validate_config:
        validate_config(args.ownership)
    else:
        check_ownership(args.manifest, args.ownership, args.fail_on_violation)
