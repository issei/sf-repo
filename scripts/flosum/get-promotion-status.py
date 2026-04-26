#!/usr/bin/env python3
"""
get-promotion-status.py — Consulta status de promoção no Flosum.
Uso: python get-promotion-status.py --promotion-id <id> [--poll]
     python get-promotion-status.py --pipeline-id <id> --environment qa
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from flosum_api import FlosumClient


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--promotion-id", help="ID da promoção específica")
    group.add_argument("--pipeline-id", help="ID do pipeline para status geral")
    parser.add_argument("--environment", default="qa",
                        choices=["qa", "preprod", "prod"])
    parser.add_argument("--poll", action="store_true",
                        help="Fazer polling até conclusão")
    parser.add_argument("--interval", type=int, default=30,
                        help="Intervalo de polling em segundos")
    parser.add_argument("--max-attempts", type=int, default=40)
    args = parser.parse_args()

    if args.pipeline_id:
        os.environ["FLOSUM_PIPELINE_ID"] = args.pipeline_id

    client = FlosumClient()

    if args.promotion_id:
        if args.poll:
            print(f"🔄 Monitorando promoção {args.promotion_id}...")
            status = client.poll_promotion(
                args.promotion_id,
                max_attempts=args.max_attempts,
                interval=args.interval,
            )
            print(f"\n{'✅' if status == 'Succeeded' else '❌'} Status final: {status}")
            sys.exit(0 if status == "Succeeded" else 1)
        else:
            result = client.get_promotion_status(args.promotion_id)
            status = result.get("status", "Unknown")
            print(f"Status: {status}")
            print(f"Detalhes: {result}")
    else:
        result = client.get_pipeline_status(args.environment)
        print(f"Pipeline status ({args.environment}): {result}")


if __name__ == "__main__":
    main()
