# Implementation Plan (Interview-Optimized)

## 1) Setup and Safety
- create virtual environment
- install dependencies
- add `.env.example` for API credentials
- ensure `.gitignore` excludes `.env` and `logs/*.log`

## 2) Core Domain
- define enums: `OrderSide`, `OrderType`
- define request model with required fields
- define response model used by CLI output

## 3) Validation Rules
Validate before network call:
- side in `BUY|SELL`
- type in `MARKET|LIMIT`
- quantity > 0
- limit orders require valid price > 0
- disallow irrelevant combinations (example: MARKET with required LIMIT fields)
- symbol format sanity check and uppercase normalization

Optional stronger rule:
- query exchange info and enforce symbol filters (`stepSize`, `tickSize`, `minQty`).

## 4) Binance Client
- testnet base URL for USDT-M Futures
- signed request for order endpoint
- explicit timeout for every request
- map HTTP and Binance error payloads to typed exceptions

## 5) CLI Flow
- parse arguments
- build order request
- call validation
- place order
- print request summary and response summary in readable format

## 6) Logging
- console: concise user-friendly logs
- file: detailed request/response/error logs
- redact secrets (`api_key`, `signature`, `secret`)
- include timestamp, level, event name, symbol, side, type, quantity, price, status

## 7) Error Handling
Handle at least:
- invalid user input
- request timeout / connection failure
- API auth failure
- rate limit / service unavailable
- business-rule failure from Binance (precision, insufficient margin, etc.)

## 8) Testing (Right-Sized)
For a 60-minute assignment, target focused tests:
- validator happy path and failure path
- service flow for MARKET and LIMIT using mocked client
- one client error mapping test

## 9) Evidence for Submission
Generate and retain:
- one successful MARKET order log entry
- one successful LIMIT order log entry
- command examples used to produce both

## 10) Final Polish
- concise README with setup, usage, architecture, troubleshooting
- stable CLI help text
- no secrets in repo or logs
