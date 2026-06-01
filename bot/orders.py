from __future__ import annotations

import logging

from bot.client import BinanceFuturesClient
from bot.logging_config import LOGGER_NAME, sanitize_for_log
from bot.validators import validate_order_input, validate_symbol_exists


class OrderService:
    def __init__(
        self,
        client: BinanceFuturesClient,
        *,
        logger: logging.Logger | None = None,
    ) -> None:
        self.client = client
        self.logger = logger or logging.getLogger(LOGGER_NAME)

    def submit_order(
        self,
        *,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float | None = None,
        dry_run: bool = False,
    ) -> dict:
        validated = validate_order_input(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        exchange_info = self.client.get_exchange_info()
        validate_symbol_exists(validated["symbol"], exchange_info)

        request_payload = {
            "symbol": validated["symbol"],
            "side": validated["side"],
            "type": validated["type"],
            "quantity": validated["quantity"],
        }
        if validated["type"] == "LIMIT":
            request_payload["price"] = validated["price"]

        self.logger.info(
            "order_prepared dry_run=%s payload=%s",
            dry_run,
            sanitize_for_log(request_payload),
        )

        if dry_run:
            return {
                "dry_run": True,
                "request": request_payload,
                "response": None,
                "message": "Dry run enabled. Validation passed and no order was sent.",
            }

        raw_response = self.client.place_order(
            symbol=validated["symbol"],
            side=validated["side"],
            order_type=validated["type"],
            quantity=validated["quantity"],
            price=validated["price"],
        )
        normalized_response = self._normalize_order_response(raw_response)

        return {
            "dry_run": False,
            "request": request_payload,
            "response": normalized_response,
            "message": "Order submitted successfully.",
        }

    def _normalize_order_response(self, response: dict) -> dict:
        return {
            "orderId": response.get("orderId"),
            "status": response.get("status"),
            "executedQty": response.get("executedQty"),
            "avgPrice": response.get("avgPrice"),
            "symbol": response.get("symbol"),
            "side": response.get("side"),
            "type": response.get("type"),
        }
