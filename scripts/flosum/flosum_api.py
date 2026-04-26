#!/usr/bin/env python3
"""
flosum_api.py — Wrapper para a API REST do Flosum.
Uso: python flosum_api.py --check-connectivity
"""

import argparse
import os
import sys
import time
from typing import Any

import requests


class FlosumClient:
    def __init__(self):
        self.base_url = os.environ.get("FLOSUM_API_BASE_URL", "").rstrip("/")
        self.token = os.environ.get("FLOSUM_API_TOKEN", "")
        self.pipeline_id = os.environ.get("FLOSUM_PIPELINE_ID", "")

        if not self.base_url or not self.token:
            raise ValueError(
                "FLOSUM_API_BASE_URL e FLOSUM_API_TOKEN são obrigatórios."
            )

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        resp = requests.request(method, url, headers=self._headers, timeout=30, **kwargs)
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    def check_connectivity(self) -> bool:
        try:
            resp = requests.get(
                f"{self.base_url}/health",
                headers=self._headers,
                timeout=10
            )
            if resp.status_code in (200, 404):
                print(f"✅ Flosum API acessível (HTTP {resp.status_code})")
                return True
            print(f"⚠️  Flosum API retornou HTTP {resp.status_code}")
            return False
        except requests.RequestException as e:
            print(f"❌ Falha ao conectar ao Flosum: {e}")
            return False

    def create_branch(self, name: str, commit_sha: str = "", pr_number: str = "",
                      priority: str = "normal") -> dict[str, Any]:
        payload = {
            "name": name,
            "pipeline_id": self.pipeline_id,
            "github_commit_sha": commit_sha,
            "github_pr_number": pr_number,
            "priority": priority,
        }
        return self._request("POST", "/branches", json=payload)

    def trigger_promotion(self, branch_id: str, target_environment: str) -> dict[str, Any]:
        payload = {
            "branch_id": branch_id,
            "target_environment": target_environment,
            "pipeline_id": self.pipeline_id,
        }
        return self._request("POST", "/promotions", json=payload)

    def get_promotion_status(self, promotion_id: str) -> dict[str, Any]:
        return self._request("GET", f"/promotions/{promotion_id}")

    def get_pipeline_status(self, environment: str) -> dict[str, Any]:
        return self._request("GET", f"/pipelines/{self.pipeline_id}/status",
                              params={"environment": environment})

    def update_branch(self, branch_id: str, **fields) -> dict[str, Any]:
        return self._request("PATCH", f"/branches/{branch_id}", json=fields)

    def poll_promotion(self, promotion_id: str, max_attempts: int = 40,
                       interval: int = 30) -> str:
        for attempt in range(1, max_attempts + 1):
            status_data = self.get_promotion_status(promotion_id)
            status = status_data.get("status", "Unknown")
            print(f"   [{attempt}/{max_attempts}] Status: {status}")

            if status in ("Succeeded", "Failed", "Error"):
                return status

            time.sleep(interval)

        return "Timeout"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-connectivity", action="store_true")
    args = parser.parse_args()

    if args.check_connectivity:
        client = FlosumClient()
        ok = client.check_connectivity()
        sys.exit(0 if ok else 1)
