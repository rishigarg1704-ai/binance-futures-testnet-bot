class TradingBotError(Exception):
    pass


class ConfigurationError(TradingBotError):
    pass


class ValidationError(TradingBotError):
    pass


class BinanceAPIError(TradingBotError):
    def __init__(
        self,
        message: str,
        *,
        code: int | None = None,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code


class AuthenticationError(BinanceAPIError):
    pass


class NetworkError(TradingBotError):
    pass


class RateLimitError(BinanceAPIError):
    pass
