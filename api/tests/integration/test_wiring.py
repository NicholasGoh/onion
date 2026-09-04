from unittest.mock import MagicMock

from app.main import container


def test_items_route_wired_to_item_service(client):
    mock_service = MagicMock(get_all=MagicMock(return_value=[]))
    with container.item_service.override(mock_service):
        resp = client.get("/items/")
    assert resp.status_code == 200
    mock_service.get_all.assert_called_once()


def test_orders_route_wired_to_order_service(client):
    mock_service = MagicMock(get_all=MagicMock(return_value=[]))
    with container.order_service.override(mock_service):
        resp = client.get("/orders/")
    assert resp.status_code == 200
    mock_service.get_all.assert_called_once()


def test_tags_route_wired_to_tag_service(client):
    mock_service = MagicMock(get_all=MagicMock(return_value=[]))
    with container.tag_service.override(mock_service):
        resp = client.get("/tags/")
    assert resp.status_code == 200
    mock_service.get_all.assert_called_once()
