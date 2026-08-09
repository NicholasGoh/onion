from app.data.entities import Tag, TagData
from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    name: str = Field(description="Tag name")

    def to_entity(self) -> TagData:
        return TagData(name=self.name)


class TagRead(BaseModel):
    id: int
    name: str

    @classmethod
    def from_entity(cls, tag: Tag) -> "TagRead":
        return cls(id=tag.id, name=tag.name)
