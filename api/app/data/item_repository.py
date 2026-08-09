from typing import Optional

from sqlmodel import Field, Session, SQLModel, select

from app.data.entities import Item, ItemData
from app.data.interfaces import IRepository


class ItemModel(SQLModel, table=True):
    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

    def to_entity(self) -> Item:
        return Item(
            id=self.id or 0,
            name=self.name,
            description=self.description,
        )

    @classmethod
    def from_entity(cls, item: Item) -> "ItemModel":
        return cls(
            id=item.id if item.id != 0 else None,
            name=item.name,
            description=item.description,
        )


class ItemRepository(IRepository[Item, ItemData]):

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: ItemData) -> Item:
        model = ItemModel(
            name=data.name,
            description=data.description,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model.to_entity()

    def get_by_id(self, id: int) -> Item | None:
        model = self.session.get(ItemModel, id)
        return model.to_entity() if model else None

    def get_all(self) -> list[Item]:
        statement = select(ItemModel)
        results = self.session.exec(statement)
        return [model.to_entity() for model in results]

    def delete(self, id: int) -> bool:
        model = self.session.get(ItemModel, id)
        if not model:
            return False
        self.session.delete(model)
        self.session.commit()
        return True
