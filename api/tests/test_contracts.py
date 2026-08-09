from app.api.items.contracts import ItemCreate, ItemRead
from app.api.orders.contracts import OrderCreate, OrderRead
from app.data.entities import Item, Order


def test_item_create_to_entity():
    create = ItemCreate(name="Widget", description="A widget")
    entity = create.to_entity()
    assert entity.name == "Widget"
    assert entity.description == "A widget"


def test_item_read_from_entity():
    item = Item(id=1, name="Widget", description="A widget")
    read = ItemRead.from_entity(item)
    assert read.id == 1
    assert read.name == "Widget"
    assert read.description == "A widget"


def test_order_create_to_entity():
    create = OrderCreate(item_ids=[1, 2], quantity={1: 3, 2: 1})
    entity = create.to_entity()
    assert entity.item_ids == [1, 2]
    assert entity.quantity == {1: 3, 2: 1}


def test_order_read_from_entity():
    order = Order(id=1, item_ids=[1, 2], quantity={1: 3, 2: 1}, status="pending")
    read = OrderRead.from_entity(order)
    assert read.id == 1
    assert read.item_ids == [1, 2]
    assert read.status == "pending"
