# Binance Futures Testnet Trading Bot (Docs-First)

## Purpose
This folder contains implementation-ready documentation for a Python assignment:
Build a simplified trading bot for Binance USDT-M Futures Testnet.

This documentation is optimized for interview evaluation criteria:
- clean architecture
- input validation
- error handling
- logging quality
- security hygiene
- developer experience

## Assignment Scope
Required deliverables:
- Python 3.x project
- CLI tool for placing MARKET and LIMIT orders
- BUY and SELL support
- request/response printing
- separate client/API and CLI layers
- request/response/error logging
- robust exception handling
- `README.md` and `requirements.txt`
- log evidence for one MARKET and one LIMIT order

## Recommended Tech Choices
- CLI: `argparse` (standard library; low risk)
- HTTP: `requests`
- Validation: `pydantic` (or manual validators)
- Logging: Python `logging` with file + console handlers
- Testing: `pytest` with mocked API responses

## Project Deliverables
See:
- `ARCHITECTURE.md`
- `IMPLEMENTATION_PLAN.md`
- `SUBMISSION_CHECKLIST.md`
