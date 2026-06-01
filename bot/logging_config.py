"""Logging configuration utilities for the trading bot.

Single responsibility:
- Configure application logging behavior.
- Provide safe metadata sanitization helpers.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any


LOGGER_NAME = "trading_bot"
SENSITIVE_KEYS = {"api_key", "x-mbx-apikey", "api_secret", "signature", "secret"}


def _mask_value(value: str) -> str:
    """Mask secret-like values while preserving tiny debug context."""
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}***{value[-4:]}"


def sanitize_for_log(payload: dict[str, Any] | None) -> dict[str, Any]:
    """Return a copy of payload with sensitive values masked."""
    if not payload:
        return {}

    sanitized: dict[str, Any] = {}
    for key, value in payload.items():
        key_lower = key.lower()
        if key_lower in SENSITIVE_KEYS:
            sanitized[key] = _mask_value(str(value))
            continue
        sanitized[key] = value
    return sanitized


def configure_logging(log_file: str, log_level: str = "INFO") -> logging.Logger:
    """Configure and return the application logger."""
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(log_level.upper())
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(log_level.upper())
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
