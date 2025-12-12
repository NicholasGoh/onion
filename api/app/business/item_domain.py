from app.entities.item import Item, ItemData


class ItemDomain:
    """Domain service for item business logic and validation"""

    @staticmethod
    def validate_item_data(item_data: ItemData) -> None:
        """Validate item data according to business rules"""
        if not item_data.name or len(item_data.name.strip()) == 0:
            raise ValueError("Item name cannot be empty")

        if len(item_data.name) > 100:
            raise ValueError("Item name cannot exceed 100 characters")

        if item_data.description and len(item_data.description) > 500:
            raise ValueError("Item description cannot exceed 500 characters")

    @staticmethod
    def validate_item(item: Item) -> None:
        """Validate complete item according to business rules"""
        if item.id < 0:
            raise ValueError("Item ID must be non-negative")

        if not item.name or len(item.name.strip()) == 0:
            raise ValueError("Item name cannot be empty")
