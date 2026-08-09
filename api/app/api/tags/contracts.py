from app.api.base import CamelModel
from app.data.entities import Tag, TagData
from pydantic import Field


class TagCreate(CamelModel):
    name: str = Field(description="Tag name")

    def to_entity(self) -> TagData:
        return TagData(name=self.name)


class TagRead(CamelModel):
    id: int
    name: str

    @classmethod
    def from_entity(cls, tag: Tag) -> "TagRead":
        return cls(id=tag.id, name=tag.name)
