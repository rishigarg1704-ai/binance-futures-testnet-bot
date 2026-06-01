# Binance Futures Testnet Trading Bot

## Overview

This project is a Python CLI trading bot for Binance USDT-M Futures Testnet.  
It supports placing `MARKET` and `LIMIT` orders for both `BUY` and `SELL` sides using direct REST API calls.

Bonus feature included: `--dry-run`.

## Architecture

Request flow:

`cli.py -> validators.py -> orders.py -> client.py -> Binance API`

Layer responsibilities:

- `cli.py`: argument parsing, dependency wiring, user output.
- `bot/validators.py`: input validation and normalization.
- `bot/orders.py`: validation orchestration, symbol verification, dry-run logic, response normalization.
- `bot/client.py`: Binance REST calls, request signing, timeout handling, API/network error mapping.
- `bot/config.py`: environment-based configuration loading.
- `bot/logging_config.py`: file logger setup and metadata sanitization.
- `bot/exceptions.py`: custom exception hierarchy.

## Setup

### 1) Prerequisites

- Python 3.11+
- Binance Futures Testnet account and API keys

### 2) Create environment and install

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### 3) Configure environment variables

Copy `.env.example` to `.env` and fill your values:

```bash
cp .env.example .env
```

Required variables:

- `BINANCE_API_KEY`
- `BINANCE_API_SECRET`

Default base URL:

- `BINANCE_BASE_URL=https://testnet.binancefuture.com`
- If your keys were created from Binance Demo Trading UI, use:
  - `BINANCE_BASE_URL=https://demo-fapi.binance.com`

Optional:

- `REQUEST_TIMEOUT_SECONDS` (default `10`)
- `RECV_WINDOW_MS` (default `5000`)
- `LOG_FILE` (default `logs/trading_bot.log`)
- `LOG_LEVEL` (default `INFO`)

## Usage

### MARKET order

```bash
python3 cli.py \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001
```

### LIMIT order

```bash
python3 cli.py \
  --symbol BTCUSDT \
  --side SELL \
  --type LIMIT \
  --quantity 0.001 \
  --price 90000
```

### Dry run

```bash
python3 cli.py \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001 \
  --dry-run
```

Dry-run validates inputs and symbol existence, prepares payload, and prints output without sending order placement request.

## Validation Behavior

Before order placement:

- `symbol` is required
- `side` must be `BUY` or `SELL`
- `type` must be `MARKET` or `LIMIT`
- `quantity` must be greater than `0`
- `LIMIT` requires `price`
- `price` must be greater than `0`
- `symbol` must exist in Binance `exchangeInfo`

## Logging Behavior

Logs are written to `logs/trading_bot.log` by default.

Logged:

- request metadata (method, endpoint, sanitized params)
- response metadata (status code, sanitized response)
- errors with timestamps

Not logged:

- API secret
- raw signature
- raw credentials

## Testing

Run tests:

```bash
python3 -m pytest -q
```

Current tests cover:

- validation success/failure cases
- market order flow with mocked client
- limit order flow with mocked client
- dry-run behavior

## Required Submission Logs

The assignment requires log evidence for at least one successful `MARKET` order and one successful `LIMIT` order.

Recommended steps:

1. Clear previous log file:

```bash
rm -f logs/trading_bot.log
```

2. Run one MARKET order command.
3. Run one LIMIT order command.
4. Submit `logs/trading_bot.log` as evidence.

For cleaner reviewer experience, you can also provide:

- `logs/submission_orders.log` (trimmed file with just MARKET/LIMIT order request/response lines).

## Submission Artifact Checklist

Before uploading GitHub repo or ZIP, include:

- source code (`bot/`, `cli.py`, `tests/`)
- `README.md`
- `requirements.txt`
- `.env.example` (template only)
- logs:
  - `logs/submission_orders.log` (recommended)
  - `logs/trading_bot.log` (full run log, optional if large)

Do not include:

- `.env`
- `.venv/`

## Design Decisions

- Direct REST implementation instead of Binance SDK to demonstrate API-level understanding.
- `requests` chosen for clarity and reliability in a small assignment.
- strict layered flow to keep CLI, validation, service logic, and API client separated.
- custom exceptions for predictable error handling and reviewer-friendly failure output.
- mandatory timeout for all HTTP calls.

## Assumptions

- API keys are active for Binance Futures Testnet.
- account has required testnet balance/margin.
- testnet endpoint is reachable from execution environment.
- Binance may return `avgPrice` depending on order state and execution timing.

## Limitations

- No automatic retries/backoff.
- No exchange filter precision enforcement beyond assignment-required checks.
- No persistence/database.
- No advanced order types beyond `MARKET` and `LIMIT`.
