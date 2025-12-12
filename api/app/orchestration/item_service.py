from app.business.item_domain import ItemDomain
from app.entities.interfaces import IItemRepository
from app.entities.item import Item, ItemData


class ItemService:
    """Item service orchestrating business logic and persistence"""

    def __init__(self, repository: IItemRepository, domain: ItemDomain):
        self._repository = repository
        self._domain = domain

    def create_item(self, item_data: ItemData) -> Item:
        """Create item with validation"""
        self._domain.validate_item_data(item_data)
        return self._repository.create(item_data)

    def get_item(self, item_id: int) -> Item | None:
        """Get item by ID"""
        return self._repository.get_by_id(item_id)

    def get_items(self) -> list[Item]:
        """Get all items"""
        return self._repository.get_all()

    def search_items(self, query: str) -> list[Item]:
        """Search items by name or description"""
        all_items = self._repository.get_all()
        query_lower = query.lower().strip()

        if not query_lower:
            return all_items

        return [
            item for item in all_items
            if query_lower in item.name.lower()
            or (item.description and query_lower in item.description.lower())
        ]
