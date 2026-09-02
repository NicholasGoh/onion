from unittest.mock import MagicMock

import pytest
from dependency_injector import providers
from fastapi.testclient import TestClient
from sqlmodel import create_engine

from app.main import app, container


@pytest.fixture(autouse=True)
def _in_memory_db_engine():
    engine = create_engine("sqlite://")

    def get_test_engine():
        yield engine

    container.db_engine.override(providers.Resource(get_test_engine))
    yield
    container.db_engine.reset_override()
    engine.dispose()


def test_items_route_wired_to_item_service():
    mock_service = MagicMock(get_all=MagicMock(return_value=[]))
    with container.item_service.override(mock_service):
        with TestClient(app) as client:
            resp = client.get("/items/")
    assert resp.status_code == 200
    mock_service.get_all.assert_called_once()


def test_orders_route_wired_to_order_service():
    mock_service = MagicMock(get_all=MagicMock(return_value=[]))
    with container.order_service.override(mock_service):
        with TestClient(app) as client:
            resp = client.get("/orders/")
    assert resp.status_code == 200
    mock_service.get_all.assert_called_once()


def test_tags_route_wired_to_tag_service():
    mock_service = MagicMock(get_all=MagicMock(return_value=[]))
    with container.tag_service.override(mock_service):
        with TestClient(app) as client:
            resp = client.get("/tags/")
    assert resp.status_code == 200
    mock_service.get_all.assert_called_once()
