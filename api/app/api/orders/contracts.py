from app.data.entities import Order, OrderData
from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    item_ids: list[int] = Field(description="List of item IDs in the order")
    quantity: dict[int, int] = Field(description="Quantity per item ID")

    def to_entity(self) -> OrderData:
        return OrderData(item_ids=self.item_ids, quantity=self.quantity)


class OrderRead(BaseModel):
    id: int
    item_ids: list[int]
    quantity: dict[int, int]
    status: str

    @classmethod
    def from_entity(cls, order: Order) -> "OrderRead":
        return cls(
            id=order.id,
            item_ids=order.item_ids,
            quantity=order.quantity,
            status=order.status,
        )
