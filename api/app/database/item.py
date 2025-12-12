from typing import Optional

from sqlmodel import Field, Session, SQLModel, select

from app.entities.interfaces import IItemRepository
from app.entities.item import Item, ItemData


class ItemModel(SQLModel, table=True):
    """SQLModel schema for Item table"""

    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

    def to_entity(self) -> Item:
        """Convert database model to domain entity"""
        return Item(
            id=self.id or 0,
            name=self.name,
            description=self.description,
        )

    @classmethod
    def from_entity(cls, item: Item) -> "ItemModel":
        """Convert domain entity to database model"""
        return cls(
            id=item.id if item.id != 0 else None,
            name=item.name,
            description=item.description,
        )


class ItemRepository(IItemRepository):
    """Repository implementation using SQLModel with PostgreSQL"""

    def __init__(self, session: Session):
        self.session = session

    def create(self, item_data: ItemData) -> Item:
        """Create item in database, return entity"""
        # Create SQLModel instance
        model = ItemModel(
            name=item_data.name,
            description=item_data.description,
        )

        # Add to session and commit
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        # Convert to entity and return
        return model.to_entity()

    def get_by_id(self, item_id: int) -> Item | None:
        """Get item from database by ID, convert to entity"""
        model = self.session.get(ItemModel, item_id)
        return model.to_entity() if model else None

    def get_all(self) -> list[Item]:
        """Get all items from database, convert to entities"""
        statement = select(ItemModel)
        results = self.session.exec(statement)
        return [model.to_entity() for model in results]
