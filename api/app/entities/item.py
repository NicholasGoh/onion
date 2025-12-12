from dataclasses import dataclass


@dataclass
class Item:
    id: int
    name: str
    description: str | None = None


@dataclass
class ItemData:
    name: str
    description: str | None = None
