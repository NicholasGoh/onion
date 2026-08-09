from abc import ABC, abstractmethod

from app.data.entities import Item, ItemData


class IItemRepository(ABC):

    @abstractmethod
    def create(self, item_data: ItemData) -> Item:
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> Item | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Item]:
        pass
