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


@dataclass
class Order:
    id: int
    item_ids: list[int]
    quantity: dict[int, int]
    status: str = "pending"


@dataclass
class OrderData:
    item_ids: list[int]
    quantity: dict[int, int]


@dataclass
class Tag:
    id: int
    name: str


@dataclass
class TagData:
    name: str
