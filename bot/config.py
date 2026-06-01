"""Configuration loading for the trading bot.

Single responsibility:
- Read runtime configuration from environment variables.
- Provide a typed config object to other layers.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from bot.exceptions import ConfigurationError


DEFAULT_BASE_URL = "https://testnet.binancefuture.com"
DEFAULT_TIMEOUT_SECONDS = 10.0
DEFAULT_RECV_WINDOW_MS = 5000


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Runtime settings required by the application."""

    api_key: str
    api_secret: str
    base_url: str = DEFAULT_BASE_URL
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
    recv_window_ms: int = DEFAULT_RECV_WINDOW_MS
    log_file: str = "logs/trading_bot.log"
    log_level: str = "INFO"


def _require_env(name: str) -> str:
    """Return a required env var value or raise a clear error."""
    value = os.getenv(name, "").strip()
    if not value:
        raise ConfigurationError(f"Missing required environment variable: {name}")
    return value


def _optional_float(name: str, default: float) -> float:
    raw_value = os.getenv(name, "").strip()
    if not raw_value:
        return default
    try:
        parsed = float(raw_value)
    except ValueError as exc:
        raise ConfigurationError(f"Environment variable {name} must be a number.") from exc
    if parsed <= 0:
        raise ConfigurationError(f"Environment variable {name} must be greater than 0.")
    return parsed


def _optional_int(name: str, default: int) -> int:
    raw_value = os.getenv(name, "").strip()
    if not raw_value:
        return default
    try:
        parsed = int(raw_value)
    except ValueError as exc:
        raise ConfigurationError(f"Environment variable {name} must be an integer.") from exc
    if parsed <= 0:
        raise ConfigurationError(f"Environment variable {name} must be greater than 0.")
    return parsed


def load_config() -> AppConfig:
    """Load, validate, and return application configuration."""
    load_dotenv()

    return AppConfig(
        api_key=_require_env("BINANCE_API_KEY"),
        api_secret=_require_env("BINANCE_API_SECRET"),
        base_url=os.getenv("BINANCE_BASE_URL", DEFAULT_BASE_URL).strip()
        or DEFAULT_BASE_URL,
        timeout_seconds=_optional_float("REQUEST_TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS),
        recv_window_ms=_optional_int("RECV_WINDOW_MS", DEFAULT_RECV_WINDOW_MS),
        log_file=os.getenv("LOG_FILE", "logs/trading_bot.log").strip() or "logs/trading_bot.log",
        log_level=os.getenv("LOG_LEVEL", "INFO").strip().upper() or "INFO",
    )
