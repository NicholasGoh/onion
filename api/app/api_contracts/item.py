from app.entities.item import Item, ItemData
from faker import Faker
from pydantic import BaseModel, Field

fake = Faker()


def _generate_item_name_examples() -> list[str]:
    """Generate realistic item name examples using Faker"""
    return [fake.catch_phrase() for _ in range(3)]


def _generate_item_description_examples() -> list[str]:
    """Generate realistic item description examples using Faker"""
    return [fake.sentence(nb_words=8) for _ in range(3)]


class ItemCreate(BaseModel):
    name: str = Field(
        ...,
        examples=_generate_item_name_examples(),
        description="Name of the item"
    )
    description: str | None = Field(
        None,
        examples=_generate_item_description_examples(),
        description="Optional description of the item"
    )

    def to_entities(self) -> ItemData:
        return ItemData(name=self.name, description=self.description)


class ItemRead(BaseModel):
    id: int = Field(..., examples=[1], description="Unique identifier")
    name: str = Field(
        ...,
        examples=_generate_item_name_examples(),
        description="Name of the item"
    )
    description: str | None = Field(
        None,
        examples=_generate_item_description_examples(),
        description="Optional description of the item"
    )

    @classmethod
    def from_entities(cls, item: Item) -> "ItemRead":
        return cls(id=item.id, name=item.name, description=item.description)
