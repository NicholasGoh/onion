from faker import Faker

from app.api_contracts.item import ItemCreate, ItemRead

fake = Faker()


class ItemFactory:
    """Factory for generating item DTOs with realistic fake data"""

    @staticmethod
    def create_item_create() -> ItemCreate:
        """Generate a fake ItemCreate DTO"""
        return ItemCreate(
            name=fake.catch_phrase(),
            description=fake.sentence(nb_words=8),
        )

    @staticmethod
    def create_item_read(item_id: int | None = None) -> ItemRead:
        """Generate a fake ItemRead DTO"""
        return ItemRead(
            id=item_id if item_id is not None else fake.random_int(min=1, max=1000),
            name=fake.catch_phrase(),
            description=fake.sentence(nb_words=8),
        )

    @staticmethod
    def create_batch_item_create(count: int = 5) -> list[ItemCreate]:
        """Generate multiple fake ItemCreate DTOs"""
        return [ItemFactory.create_item_create() for _ in range(count)]

    @staticmethod
    def create_batch_item_read(count: int = 5) -> list[ItemRead]:
        """Generate multiple fake ItemRead DTOs"""
        return [ItemFactory.create_item_read(item_id=i + 1) for i in range(count)]
