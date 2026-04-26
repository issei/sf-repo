#!/usr/bin/env python3
"""
trigger-promotion.py — Dispara promoção via API Flosum.
Uso: python trigger-promotion.py --branch-id <id> --target-environment qa
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from flosum_api import FlosumClient


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch-id", required=True, help="ID do branch Flosum")
    parser.add_argument("--target-environment", required=True,
                        choices=["qa", "preprod", "prod"])
    parser.add_argument("--pipeline-id", default="", help="Sobrescreve env var")
    args = parser.parse_args()

    if args.target_environment == "prod":
        print("🛑 Promoção para Produção requer aprovação humana explícita.")
        print("   Certifique-se de ter o comentário /approve-prod-promotion no PR.")
        approval = input("   Confirmar que aprovação humana foi obtida? [s/N]: ").strip().lower()
        if approval != "s":
            print("❌ Promoção cancelada. Obtenha aprovação humana primeiro.")
            sys.exit(1)

    if args.pipeline_id:
        os.environ["FLOSUM_PIPELINE_ID"] = args.pipeline_id

    client = FlosumClient()

    print(f"🚀 Disparando promoção...")
    print(f"   Branch: {args.branch_id}")
    print(f"   Ambiente: {args.target_environment}")

    result = client.trigger_promotion(
        branch_id=args.branch_id,
        target_environment=args.target_environment,
    )

    promotion_id = result.get("id", "")
    print(f"✅ Promoção iniciada.")
    print(f"   Promotion ID: {promotion_id}")
    print(f"\nFLOSUM_PROMOTION_ID={promotion_id}")
    print(f"\nMonitore com:")
    print(f"  python scripts/flosum/get-promotion-status.py --promotion-id {promotion_id}")


if __name__ == "__main__":
    main()
