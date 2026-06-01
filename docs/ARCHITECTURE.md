# Architecture Recommendation

## Goals
- meet all assignment requirements with minimal risk
- keep code testable and maintainable
- demonstrate production-minded engineering in a small scope

## Proposed Structure
```text
trading_bot/
  src/
    cli.py
    config.py
    logger.py
    exceptions.py
    models.py
    validators.py
    binance_client.py
    order_service.py
  tests/
    test_validators.py
    test_order_service.py
    test_client_errors.py
  logs/
  README.md
  requirements.txt
  .env.example
```

## Layer Responsibilities
- `cli.py`: parse args, call service, print success/error output.
- `models.py`: order request/response models and enums.
- `validators.py`: input checks before API call.
- `binance_client.py`: signing, HTTP calls, response normalization.
- `order_service.py`: orchestration flow (validate -> submit -> map result).
- `exceptions.py`: typed errors (`ValidationError`, `APIError`, `NetworkError`).
- `logger.py`: consistent structured logging setup.

## Why This Works For Reviewers
- clear separation of concerns
- easy to unit test (service and validators independent of CLI)
- visible security posture (no secret leakage in logs)
- easy extensibility if strategy logic is added later
