from app.data.entities import Item, ItemData
from app.data.interfaces import IItemRepository


class ItemService:

    def __init__(self, repository: IItemRepository):
        self._repository = repository

    @staticmethod
    def _validate_item_data(item_data: ItemData) -> None:
        if not item_data.name or len(item_data.name.strip()) == 0:
            raise ValueError("Item name cannot be empty")

        if len(item_data.name) > 100:
            raise ValueError("Item name cannot exceed 100 characters")

        if item_data.description and len(item_data.description) > 500:
            raise ValueError("Item description cannot exceed 500 characters")

    def create_item(self, item_data: ItemData) -> Item:
        self._validate_item_data(item_data)
        return self._repository.create(item_data)

    def get_item(self, item_id: int) -> Item | None:
        return self._repository.get_by_id(item_id)

    def get_items(self) -> list[Item]:
        return self._repository.get_all()

    def search_items(self, query: str) -> list[Item]:
        all_items = self._repository.get_all()
        query_lower = query.lower().strip()

        if not query_lower:
            return all_items

        return [
            item for item in all_items
            if query_lower in item.name.lower()
            or (item.description and query_lower in item.description.lower())
        ]
