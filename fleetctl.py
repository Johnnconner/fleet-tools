#!/usr/bin/env python3
"""Thin wrapper around the fleet controller REST API."""
import argparse
import os

import requests


def load_env(path=".env"):
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k, v)


def get(path, **params):
    r = requests.get(
        os.environ["FLEET_API_URL"] + path,
        headers={"Authorization": "Bearer " + os.environ["FLEET_API_TOKEN"]},
        params={k: v for k, v in params.items() if v},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def main():
    load_env()
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    robots = sub.add_parser("robots")
    robots.add_argument("--site")
    robots.add_argument("--status")
    sub.add_parser("missions")
    a = p.parse_args()
    if a.cmd == "robots":
        print(get("/robots", site=a.site, status=a.status))
    else:
        print(get("/missions"))


if __name__ == "__main__":
    main()
