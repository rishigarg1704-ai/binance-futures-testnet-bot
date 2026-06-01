import pytest

from bot.exceptions import ValidationError
from bot.validators import validate_order_input


def test_validate_order_input_success_market() -> None:
    result = validate_order_input(
        symbol="btcusdt",
        side="buy",
        order_type="market",
        quantity=0.001,
        price=None,
    )
    assert result["symbol"] == "BTCUSDT"
    assert result["side"] == "BUY"
    assert result["type"] == "MARKET"
    assert result["quantity"] == 0.001
    assert result["price"] is None


def test_validate_order_input_invalid_side() -> None:
    with pytest.raises(ValidationError, match="side must be BUY or SELL"):
        validate_order_input(
            symbol="BTCUSDT",
            side="HOLD",
            order_type="MARKET",
            quantity=0.001,
            price=None,
        )


def test_validate_order_input_invalid_type() -> None:
    with pytest.raises(ValidationError, match="type must be MARKET or LIMIT"):
        validate_order_input(
            symbol="BTCUSDT",
            side="BUY",
            order_type="STOP",
            quantity=0.001,
            price=None,
        )


def test_validate_order_input_invalid_quantity() -> None:
    with pytest.raises(ValidationError, match="quantity must be greater than 0"):
        validate_order_input(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity=0,
            price=None,
        )


def test_validate_order_input_invalid_limit_price() -> None:
    with pytest.raises(ValidationError, match="price must be greater than 0"):
        validate_order_input(
            symbol="BTCUSDT",
            side="SELL",
            order_type="LIMIT",
            quantity=0.001,
            price=0,
        )
