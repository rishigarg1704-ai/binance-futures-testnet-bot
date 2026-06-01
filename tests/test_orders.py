from unittest.mock import Mock

from bot.orders import OrderService


def _mock_exchange_info() -> dict:
    return {"symbols": [{"symbol": "BTCUSDT"}, {"symbol": "ETHUSDT"}]}


def test_market_order_flow_with_mocked_client() -> None:
    client = Mock()
    client.get_exchange_info.return_value = _mock_exchange_info()
    client.place_order.return_value = {
        "orderId": 101,
        "status": "FILLED",
        "executedQty": "0.001",
        "avgPrice": "68000.12",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "MARKET",
    }

    service = OrderService(client)
    result = service.submit_order(
        symbol="BTCUSDT",
        side="BUY",
        order_type="MARKET",
        quantity=0.001,
        price=None,
        dry_run=False,
    )

    assert result["dry_run"] is False
    assert result["request"] == {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "MARKET",
        "quantity": 0.001,
    }
    assert result["response"]["orderId"] == 101
    assert result["response"]["status"] == "FILLED"
    assert result["response"]["executedQty"] == "0.001"
    assert result["response"]["avgPrice"] == "68000.12"

    client.place_order.assert_called_once_with(
        symbol="BTCUSDT",
        side="BUY",
        order_type="MARKET",
        quantity=0.001,
        price=None,
    )


def test_limit_order_flow_with_mocked_client() -> None:
    client = Mock()
    client.get_exchange_info.return_value = _mock_exchange_info()
    client.place_order.return_value = {
        "orderId": 202,
        "status": "NEW",
        "executedQty": "0",
        "avgPrice": "0.0",
        "symbol": "BTCUSDT",
        "side": "SELL",
        "type": "LIMIT",
    }

    service = OrderService(client)
    result = service.submit_order(
        symbol="BTCUSDT",
        side="SELL",
        order_type="LIMIT",
        quantity=0.002,
        price=90000.0,
        dry_run=False,
    )

    assert result["dry_run"] is False
    assert result["request"] == {
        "symbol": "BTCUSDT",
        "side": "SELL",
        "type": "LIMIT",
        "quantity": 0.002,
        "price": 90000.0,
    }
    assert result["response"]["orderId"] == 202
    assert result["response"]["status"] == "NEW"
    assert result["response"]["executedQty"] == "0"
    assert result["response"]["avgPrice"] == "0.0"

    client.place_order.assert_called_once_with(
        symbol="BTCUSDT",
        side="SELL",
        order_type="LIMIT",
        quantity=0.002,
        price=90000.0,
    )


def test_dry_run_validates_and_does_not_place_order() -> None:
    client = Mock()
    client.get_exchange_info.return_value = _mock_exchange_info()

    service = OrderService(client)
    result = service.submit_order(
        symbol="BTCUSDT",
        side="BUY",
        order_type="MARKET",
        quantity=0.003,
        price=None,
        dry_run=True,
    )

    assert result["dry_run"] is True
    assert result["response"] is None
    assert "no order was sent" in result["message"].lower()

    client.get_exchange_info.assert_called_once()
    client.place_order.assert_not_called()
