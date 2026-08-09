from app.api.items.contracts import ItemCreate, ItemRead
from app.api.orders.contracts import OrderCreate, OrderRead
from app.data.entities import Item, Order


def test_item_read_serializes_camel_case():
    item = Item(id=1, name="Widget", description="A widget")
    read = ItemRead.from_entity(item)
    data = read.model_dump(by_alias=True)
    assert "id" in data
    assert "name" in data


def test_order_read_serializes_item_ids_as_camel():
    order = Order(id=1, item_ids=[1, 2], quantity={1: 3, 2: 1}, status="pending")
    read = OrderRead.from_entity(order)
    data = read.model_dump(by_alias=True)
    assert "itemIds" in data
    assert "item_ids" not in data


def test_order_create_accepts_camel_case_input():
    order = OrderCreate.model_validate({"itemIds": [1], "quantity": {1: 2}})
    assert order.item_ids == [1]


def test_order_create_accepts_snake_case_input():
    order = OrderCreate.model_validate({"item_ids": [1], "quantity": {1: 2}})
    assert order.item_ids == [1]


def test_item_create_to_entity():
    create = ItemCreate(name="Widget", description="A widget")
    entity = create.to_entity()
    assert entity.name == "Widget"
    assert entity.description == "A widget"


def test_order_create_to_entity():
    create = OrderCreate(item_ids=[1, 2], quantity={1: 3, 2: 1})
    entity = create.to_entity()
    assert entity.item_ids == [1, 2]
    assert entity.quantity == {1: 3, 2: 1}
