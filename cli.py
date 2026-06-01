from __future__ import annotations

import argparse
import json
import sys

from bot.client import BinanceFuturesClient
from bot.config import load_config
from bot.exceptions import (
    AuthenticationError,
    BinanceAPIError,
    ConfigurationError,
    NetworkError,
    RateLimitError,
    ValidationError,
)
from bot.logging_config import configure_logging
from bot.orders import OrderService
from bot.validators import validate_order_input


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Place MARKET or LIMIT orders on Binance Futures Testnet (USDT-M)."
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", dest="order_type", required=True, help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, default=None, help="Required for LIMIT orders")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print payload without placing an order",
    )
    return parser


def print_order_request(request_payload: dict, *, dry_run: bool) -> None:
    print("Order Request Summary")
    print(f"  dryRun: {dry_run}")
    print(f"  symbol: {request_payload.get('symbol')}")
    print(f"  side: {request_payload.get('side')}")
    print(f"  type: {request_payload.get('type')}")
    print(f"  quantity: {request_payload.get('quantity')}")
    if "price" in request_payload and request_payload.get("price") is not None:
        print(f"  price: {request_payload.get('price')}")


def print_order_response(response_payload: dict | None) -> None:
    print("Order Response Summary")
    if not response_payload:
        print("  response: None")
        return
    print(f"  orderId: {response_payload.get('orderId')}")
    print(f"  status: {response_payload.get('status')}")
    print(f"  executedQty: {response_payload.get('executedQty')}")
    avg_price = response_payload.get("avgPrice")
    if avg_price is not None:
        print(f"  avgPrice: {avg_price}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        config = load_config()
        logger = configure_logging(config.log_file, config.log_level)

        validated = validate_order_input(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )

        client = BinanceFuturesClient(
            api_key=config.api_key,
            api_secret=config.api_secret,
            base_url=config.base_url,
            timeout_seconds=config.timeout_seconds,
            recv_window_ms=config.recv_window_ms,
            logger=logger,
        )
        service = OrderService(client, logger=logger)

        result = service.submit_order(
            symbol=validated["symbol"],
            side=validated["side"],
            order_type=validated["type"],
            quantity=validated["quantity"],
            price=validated["price"],
            dry_run=args.dry_run,
        )

        print_order_request(result["request"], dry_run=bool(result["dry_run"]))
        print_order_response(result["response"])
        print(f"Result: SUCCESS - {result['message']}")
        return 0
    except ValidationError as exc:
        print(f"Result: FAILURE - Validation error: {exc}")
        return 2
    except RateLimitError as exc:
        print(f"Result: FAILURE - Rate limit error: {exc}")
        return 3
    except AuthenticationError as exc:
        print(f"Result: FAILURE - Authentication error: {exc}")
        return 4
    except NetworkError as exc:
        print(f"Result: FAILURE - Network error: {exc}")
        return 5
    except BinanceAPIError as exc:
        print(f"Result: FAILURE - Binance API error: {exc}")
        return 6
    except ConfigurationError as exc:
        print(f"Result: FAILURE - Configuration error: {exc}")
        return 7
    except Exception as exc:
        print("Result: FAILURE - Unexpected error.")
        print(json.dumps({"error": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
