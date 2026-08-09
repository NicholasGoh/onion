from typing import Optional

from sqlmodel import Field, Session, SQLModel, select

from app.data.entities import Tag, TagData
from app.data.interfaces import IRepository


class TagModel(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    def to_entity(self) -> Tag:
        return Tag(id=self.id or 0, name=self.name)


class TagRepository(IRepository[Tag, TagData]):

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: TagData) -> Tag:
        model = TagModel(name=data.name)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model.to_entity()

    def get_by_id(self, id: int) -> Tag | None:
        model = self.session.get(TagModel, id)
        return model.to_entity() if model else None

    def get_all(self) -> list[Tag]:
        statement = select(TagModel)
        results = self.session.exec(statement)
        return [model.to_entity() for model in results]

    def delete(self, id: int) -> bool:
        model = self.session.get(TagModel, id)
        if not model:
            return False
        self.session.delete(model)
        self.session.commit()
        return True
