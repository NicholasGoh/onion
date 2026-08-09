import pytest

from app.data.entities import Item, ItemData, Order, OrderData, Tag, TagData
from app.data.interfaces import IRepository


class FakeRepository(IRepository):

    def __init__(self, items=None):
        self._items: dict[int, any] = {}
        self._next_id = 1
        for item in (items or []):
            self._items[self._next_id] = item
            self._next_id += 1

    def create(self, data) -> any:
        id = self._next_id
        self._next_id += 1
        entity = self._make_entity(id, data)
        self._items[id] = entity
        return entity

    def get_by_id(self, id: int):
        return self._items.get(id)

    def get_all(self) -> list:
        return list(self._items.values())

    def delete(self, id: int) -> bool:
        if id in self._items:
            del self._items[id]
            return True
        return False

    def _make_entity(self, id, data):
        raise NotImplementedError


class FakeItemRepository(FakeRepository):

    def _make_entity(self, id, data: ItemData) -> Item:
        return Item(id=id, name=data.name, description=data.description)


class FakeOrderRepository(FakeRepository):

    def _make_entity(self, id, data: OrderData) -> Order:
        return Order(id=id, item_ids=data.item_ids, quantity=data.quantity)


class FakeTagRepository(FakeRepository):

    def _make_entity(self, id, data: TagData) -> Tag:
        return Tag(id=id, name=data.name)


@pytest.fixture
def item_repo():
    return FakeItemRepository()


@pytest.fixture
def item_repo_with_data():
    repo = FakeItemRepository()
    repo.create(ItemData(name="Bluetooth Speaker", description="Portable audio"))
    repo.create(ItemData(name="USB Cable", description="Type-C charging cable"))
    repo.create(ItemData(name="Blue Light Glasses", description="Screen filter"))
    return repo
