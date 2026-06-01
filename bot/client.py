from __future__ import annotations

import hashlib
import hmac
import logging
import time
from urllib.parse import urlencode

import requests

from bot.exceptions import (
    AuthenticationError,
    BinanceAPIError,
    ConfigurationError,
    NetworkError,
    RateLimitError,
)
from bot.logging_config import LOGGER_NAME, sanitize_for_log


class BinanceFuturesClient:
    def __init__(
        self,
        *,
        api_key: str,
        api_secret: str,
        base_url: str,
        timeout_seconds: float,
        recv_window_ms: int,
        logger: logging.Logger | None = None,
    ) -> None:
        if not api_key.strip():
            raise ConfigurationError("BINANCE_API_KEY is required.")
        if not api_secret.strip():
            raise ConfigurationError("BINANCE_API_SECRET is required.")
        if timeout_seconds <= 0:
            raise ConfigurationError("REQUEST_TIMEOUT_SECONDS must be greater than 0.")
        if recv_window_ms <= 0:
            raise ConfigurationError("RECV_WINDOW_MS must be greater than 0.")

        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.recv_window_ms = recv_window_ms
        self.logger = logger or logging.getLogger(LOGGER_NAME)
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def get_server_time(self) -> dict:
        return self._request("GET", "/fapi/v1/time", params=None, signed=False)

    def get_exchange_info(self) -> dict:
        return self._request("GET", "/fapi/v1/exchangeInfo", params=None, signed=False)

    def place_order(
        self,
        *,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float | None = None,
    ) -> dict:
        params: dict[str, str | float | int] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        if order_type == "LIMIT":
            params["timeInForce"] = "GTC"
            if price is not None:
                params["price"] = price
        return self._request("POST", "/fapi/v1/order", params=params, signed=True)

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict | None,
        signed: bool,
    ) -> dict:
        request_params = dict(params or {})
        if signed:
            request_params["recvWindow"] = self.recv_window_ms
            request_params["timestamp"] = self._timestamp_ms()
            request_params["signature"] = self._sign_query(request_params)

        log_params = dict(request_params)
        log_params.pop("signature", None)

        self.logger.info(
            "api_request method=%s path=%s params=%s",
            method,
            path,
            sanitize_for_log(log_params),
        )

        try:
            response = self.session.request(
                method=method,
                url=f"{self.base_url}{path}",
                params=request_params if request_params else None,
                timeout=self.timeout_seconds,
            )
        except requests.Timeout as exc:
            self.logger.error(
                "api_timeout method=%s path=%s error=%s",
                method,
                path,
                str(exc),
            )
            raise NetworkError("Request to Binance timed out.") from exc
        except requests.RequestException as exc:
            self.logger.error(
                "api_network_error method=%s path=%s error=%s",
                method,
                path,
                str(exc),
            )
            raise NetworkError("Network failure while calling Binance API.") from exc

        return self._handle_response(method=method, path=path, response=response)

    def _handle_response(self, *, method: str, path: str, response: requests.Response) -> dict:
        status_code = response.status_code
        try:
            data = response.json()
        except ValueError as exc:
            body_preview = response.text[:500]
            self.logger.error(
                "api_invalid_json method=%s path=%s status_code=%s body_preview=%s",
                method,
                path,
                status_code,
                body_preview,
            )
            raise BinanceAPIError(
                "Binance returned a non-JSON response.",
                status_code=status_code,
            ) from exc

        self.logger.info(
            "api_response method=%s path=%s status_code=%s response=%s",
            method,
            path,
            status_code,
            sanitize_for_log(self._summarize_response_for_log(path, data)),
        )

        if status_code in (418, 429):
            code = data.get("code") if isinstance(data, dict) else None
            message = data.get("msg", "Rate limit exceeded.") if isinstance(data, dict) else "Rate limit exceeded."
            raise RateLimitError(message, code=code, status_code=status_code)

        if status_code >= 400:
            if isinstance(data, dict):
                code = data.get("code")
                message = data.get("msg", "Binance API request failed.")
            else:
                code = None
                message = "Binance API request failed."
            if code in (-1021, -1022) or status_code in (401, 403):
                raise AuthenticationError(message, code=code, status_code=status_code)
            raise BinanceAPIError(message, code=code, status_code=status_code)

        if isinstance(data, dict) and isinstance(data.get("code"), int) and data["code"] < 0:
            code = data["code"]
            message = data.get("msg", "Binance API returned an error.")
            if code in (-1021, -1022):
                raise AuthenticationError(message, code=code, status_code=status_code)
            raise BinanceAPIError(message, code=code, status_code=status_code)

        return data

    def _timestamp_ms(self) -> int:
        return int(time.time() * 1000)

    def _sign_query(self, params: dict) -> str:
        query_string = urlencode(params, doseq=True)
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _summarize_response_for_log(self, path: str, data: dict | list | str | int | float | bool | None) -> dict:
        if path == "/fapi/v1/exchangeInfo" and isinstance(data, dict):
            symbols = data.get("symbols")
            symbols_count = len(symbols) if isinstance(symbols, list) else None
            return {
                "timezone": data.get("timezone"),
                "serverTime": data.get("serverTime"),
                "futuresType": data.get("futuresType"),
                "symbolsCount": symbols_count,
            }

        if isinstance(data, dict):
            return data

        return {"data": data}
