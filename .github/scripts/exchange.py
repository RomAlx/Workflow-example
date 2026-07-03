#!/usr/bin/env python3
"""Fetch USDT and TON exchange rates."""

import json
import sys
import urllib.error
import urllib.request

STAGE = "EXCHANGE"
BLUE = "\033[94m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=tether,the-open-network&vs_currencies=usd"
)


def log(message: str) -> None:
    print(f"{BLUE}[{STAGE}]: {message}{RESET}", flush=True)


def log_error(message: str) -> None:
    print(f"{RED}{BOLD}[{STAGE} ERROR]: {message}{RESET}", file=sys.stderr, flush=True)


def fetch_rates() -> tuple[str, str]:
    request = urllib.request.Request(COINGECKO_URL, headers={"User-Agent": "cicd-demo/1.0"})

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"network unavailable: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("invalid API response") from exc

    usdt = data.get("tether", {}).get("usd")
    ton = data.get("the-open-network", {}).get("usd")

    if usdt is None:
        raise RuntimeError("USDT rate not found")
    if ton is None:
        raise RuntimeError("TON rate not found")

    usdt_line = f"USDT: ${usdt:.4f}"
    ton_line = f"TON: ${ton:.4f}"

    return usdt_line, ton_line


def main() -> int:
    log("started")

    try:
        usdt, ton = fetch_rates()
        log(usdt)
        log(ton)
    except RuntimeError as exc:
        log_error(str(exc))
        return 1

    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
