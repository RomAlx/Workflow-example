#!/usr/bin/env python3
"""Fetch weather in Moscow."""

import json
import sys
import urllib.error
import urllib.request

STAGE = "WEATHER"
BLUE = "\033[94m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

WEATHER_CODES = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "slight snow",
    73: "moderate snow",
    75: "heavy snow",
    77: "snow grains",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    85: "slight snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail",
}

def log(message: str) -> None:
    print(f"{BLUE}[{STAGE}]: {message}{RESET}", flush=True)


def log_error(message: str) -> None:
    print(f"{RED}{BOLD}[{STAGE} ERROR]: {message}{RESET}", file=sys.stderr, flush=True)


def fetch_moscow_weather() -> str:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=55.7558&longitude=37.6173"
        "&current=temperature_2m,weather_code"
        "&timezone=Europe/Moscow"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "cicd-demo/1.0"})

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"network unavailable: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("invalid API response") from exc

    current = data.get("current")
    if not current:
        raise RuntimeError("weather data is missing")

    temp = current["temperature_2m"]
    code = int(current["weather_code"])
    description = WEATHER_CODES.get(code, f"code {code}")

    return f"Moscow: {temp:+.1f}°C, {description}"


def main() -> int:
    log("started")

    try:
        weather = fetch_moscow_weather()
        log(weather)
    except RuntimeError as exc:
        log_error(str(exc))
        return 1

    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
