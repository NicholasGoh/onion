import pytest

from app.data.entities import ItemData, OrderData
from app.service.item_service import ItemService
from app.service.order_service import OrderService
from tests.conftest import FakeItemRepository, FakeOrderRepository


@pytest.fixture
def services():
    item_repo = FakeItemRepository()
    item_service = ItemService(repository=item_repo)
    item_service.create(ItemData(name="Widget"))
    item_service.create(ItemData(name="Gadget"))
    order_repo = FakeOrderRepository()
    order_service = OrderService(repository=order_repo, item_service=item_service)
    return order_service


def test_create_order_succeeds(services):
    order = services.create(OrderData(item_ids=[1], quantity={1: 2}))
    assert order.item_ids == [1]
    assert order.quantity == {1: 2}
    assert order.status == "pending"


def test_create_order_rejects_empty_items(services):
    with pytest.raises(ValueError, match="at least one item"):
        services.create(OrderData(item_ids=[], quantity={}))


def test_create_order_rejects_missing_items(services):
    with pytest.raises(ValueError, match="Items not found"):
        services.create(OrderData(item_ids=[999], quantity={999: 1}))


def test_create_order_rejects_zero_quantity(services):
    with pytest.raises(ValueError, match="at least 1"):
        services.create(OrderData(item_ids=[1], quantity={1: 0}))


def test_create_order_with_multiple_items(services):
    order = services.create(OrderData(item_ids=[1, 2], quantity={1: 3, 2: 1}))
    assert len(order.item_ids) == 2
