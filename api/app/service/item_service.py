from app.data.entities import Item, ItemData
from app.data.interfaces import IRepository
from app.service.crud_service import CrudService


class ItemService(CrudService[Item, ItemData]):

    def __init__(self, repository: IRepository[Item, ItemData]):
        super().__init__(repository)

    @staticmethod
    def _validate_item_data(item_data: ItemData) -> None:
        if not item_data.name or len(item_data.name.strip()) == 0:
            raise ValueError("Item name cannot be empty")

        if len(item_data.name) > 100:
            raise ValueError("Item name cannot exceed 100 characters")

        if item_data.description and len(item_data.description) > 500:
            raise ValueError("Item description cannot exceed 500 characters")

    def create(self, data: ItemData) -> Item:
        self._validate_item_data(data)
        return super().create(data)

    def search(self, query: str) -> list[Item]:
        all_items = self._repository.get_all()
        query_lower = query.lower().strip()

        if not query_lower:
            return all_items

        return [
            item for item in all_items
            if query_lower in item.name.lower()
            or (item.description and query_lower in item.description.lower())
        ]
