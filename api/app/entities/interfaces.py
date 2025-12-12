from abc import ABC, abstractmethod

from app.entities.item import Item, ItemData


class IItemRepository(ABC):
    """Interface for Item repository - works with domain entities"""

    @abstractmethod
    def create(self, item_data: ItemData) -> Item:
        """Create item, returns domain entity"""
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> Item | None:
        """Get item by ID, returns domain entity"""
        pass

    @abstractmethod
    def get_all(self) -> list[Item]:
        """Get all items, returns domain entities"""
        pass
