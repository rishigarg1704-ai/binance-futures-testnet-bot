from __future__ import annotations

from bot.exceptions import ValidationError


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def normalize_symbol(symbol: str) -> str:
    normalized = (symbol or "").strip().upper()
    if not normalized:
        raise ValidationError("symbol is required.")
    return normalized


def normalize_side(side: str) -> str:
    normalized = (side or "").strip().upper()
    if normalized not in VALID_SIDES:
        raise ValidationError("side must be BUY or SELL.")
    return normalized


def normalize_order_type(order_type: str) -> str:
    normalized = (order_type or "").strip().upper()
    if normalized not in VALID_ORDER_TYPES:
        raise ValidationError("type must be MARKET or LIMIT.")
    return normalized


def normalize_quantity(quantity: float) -> float:
    try:
        parsed = float(quantity)
    except (TypeError, ValueError) as exc:
        raise ValidationError("quantity must be a valid number.") from exc

    if parsed <= 0:
        raise ValidationError("quantity must be greater than 0.")
    return parsed


def normalize_price(price: float | None, order_type: str) -> float | None:
    if order_type == "MARKET":
        return None

    if price is None:
        raise ValidationError("price is required for LIMIT orders.")

    try:
        parsed = float(price)
    except (TypeError, ValueError) as exc:
        raise ValidationError("price must be a valid number.") from exc

    if parsed <= 0:
        raise ValidationError("price must be greater than 0.")
    return parsed


def validate_symbol_exists(symbol: str, exchange_info: dict) -> None:
    symbols = exchange_info.get("symbols", [])
    if not isinstance(symbols, list):
        raise ValidationError("Invalid exchange info response: symbols list not found.")

    available = {item.get("symbol") for item in symbols if isinstance(item, dict)}
    if symbol not in available:
        raise ValidationError(f"symbol '{symbol}' does not exist on Binance Futures Testnet.")


def validate_order_input(
    *,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None,
) -> dict:
    normalized_symbol = normalize_symbol(symbol)
    normalized_side = normalize_side(side)
    normalized_type = normalize_order_type(order_type)
    normalized_quantity = normalize_quantity(quantity)
    normalized_price = normalize_price(price, normalized_type)

    return {
        "symbol": normalized_symbol,
        "side": normalized_side,
        "type": normalized_type,
        "quantity": normalized_quantity,
        "price": normalized_price,
    }
