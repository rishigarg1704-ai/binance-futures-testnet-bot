# Submission Summary

## Assignment Status

- MARKET order support: Completed
- LIMIT order support: Completed
- BUY/SELL support: Completed
- CLI validation: Completed
- Logging + error handling: Completed
- Tests: Completed (`python3 -m pytest -q`)

## Verified Runtime Evidence

Successful sample runs:

1. MARKET BUY `BTCUSDT` `0.001`
- `orderId`: `13672733464`
- `status`: `NEW`

2. LIMIT SELL `BTCUSDT` `0.001` @ `90000`
- `orderId`: `13672734713`
- `status`: `NEW`

Evidence files:

- `logs/submission_orders.log` (trimmed, reviewer-friendly)
- `logs/trading_bot.log` (full logs)

## Security Notes

- Real credentials are stored only in local `.env`.
- `.env` is git-ignored.
- `.env.example` is provided as safe template.
