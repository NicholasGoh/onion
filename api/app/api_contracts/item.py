from app.entities.item import Item, ItemData
from faker import Faker
from pydantic import BaseModel, Field

fake = Faker()


class ItemCreate(BaseModel):
    name: str = Field(
        default_factory=lambda: fake.word(),
        examples=[fake.word() for _ in range(3)],
        description="Name of the item",
    )
    description: str | None = Field(
        default_factory=lambda: fake.sentence(),
        examples=[fake.sentence() for _ in range(3)],
        description="Optional description of the item",
    )

    def to_entities(self) -> ItemData:
        return ItemData(name=self.name, description=self.description)


class ItemRead(BaseModel):
    id: int = Field(
        default_factory=lambda: fake.random_int(min=1, max=1000),
        examples=[fake.random_int(min=1, max=1000) for _ in range(3)],
        description="Unique identifier"
    )
    name: str = Field(
        default_factory=lambda: fake.word(),
        examples=[fake.word() for _ in range(3)],
        description="Name of the item",
    )
    description: str | None = Field(
        default_factory=lambda: fake.sentence(),
        examples=[fake.sentence() for _ in range(3)],
        description="Optional description of the item",
    )

    @classmethod
    def from_entities(cls, item: Item) -> "ItemRead":
        return cls(id=item.id, name=item.name, description=item.description)
